export default {
  async fetch(request, env, ctx) {
    // Handle HTTP requests (e.g., Telegram/WhatsApp webhooks)
    if (request.method !== 'POST') {
      return new Response('OK');
    }
    const { message } = await request.json();
    if (!message || !message.text) {
      return new Response('No message');
    }
    const chatId = message.chat.id;
    const text = message.text.trim();

    // Helper to send a message back via Telegram
    async function sendTelegramMessage(msg) {
      const url = `https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/sendMessage`;
      await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text: msg })
      });
    }

    if (text.startsWith('/now')) {
      // Trigger an immediate run of the scheduled job
      try {
        const result = await runOrientation(env);
        await sendTelegramMessage(`✅ Orientation updated with ${result.length} channels.`);
      } catch (err) {
        await sendTelegramMessage(`⚠️ Failed to run orientation: ${err.message}`);
      }
      return new Response('OK');
    } else if (text.startsWith('/ask')) {
      // Respond with latest orientation facts (from GitHub)
      const query = text.slice(4).trim();
      try {
        const facts = await getLatestFacts(env);
        let answer = '';
        if (!query) {
          // if no query, list available sources
          const sources = facts.map(f => f.source).join(', ');
          answer = `Available sources: ${sources}\nUse /ask <keyword> to search in latest facts.`;
        } else {
          // filter facts by query (case-insensitive)
          const matches = facts.filter(f => f.text.toLowerCase().includes(query.toLowerCase()));
          if (matches.length === 0) {
            answer = `No facts found for “${query}” in the latest orientation.`;
          } else {
            answer = matches.map(f => `• [${f.source}] ${f.text}`).join('\n');
          }
        }
        await sendTelegramMessage(answer);
      } catch (err) {
        await sendTelegramMessage(`⚠️ Failed to retrieve facts: ${err.message}`);
      }
      return new Response('OK');
    } else {
      // Unknown command
      await sendTelegramMessage('Commands:\n/now – update orientation now\n/ask <keyword> – search latest orientation facts.');
      return new Response('OK');
    }
  },

  async scheduled(event, env, ctx) {
    await runOrientation(env);
  }
};

// Helper to fetch and process posts from channels
async function runOrientation(env) {
  const channels = JSON.parse(env.CHANNELS_JSON || '[]');
  const results = [];
  for (const chan of channels) {
    const handle = chan.handle;
    const id = chan.id;
    try {
      const res = await fetch(`https://t.me/s/${handle}`);
      const html = await res.text();
      const posts = parsePosts(html);
      for (const p of posts) {
        results.push({
          source: handle,
          text: p
        });
      }
    } catch (err) {
      // ignore errors per channel
    }
  }
  // Persist results to GitHub
  await persistToGitHub(results, env);
  return results;
}

// Very naive parser: extract plain text from Telegram channel HTML
function parsePosts(html) {
  const matches = [...html.matchAll(/<div class="tgme_widget_message_text"[^>]*>([\s\S]*?)<\/div>/g)];
  const posts = matches.map(m => {
    // Remove HTML tags and decode entities
    const tmp = m[1]
      .replace(/<[^>]+>/g, ' ')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&amp;/g, '&');
    return tmp.trim().replace(/\s+/g, ' ');
  });
  return posts;
}

// Persist orientation facts to GitHub repository as a JSON file dated by today
async function persistToGitHub(results, env) {
  const date = new Date().toISOString().split('T')[0];
  const path = `${env.GITHUB_PATH_PREFIX || 'orientation'}/${date}.json`;
  const body = JSON.stringify(results, null, 2);
  const content = Buffer.from(body).toString('base64');
  const url = `https://api.github.com/repos/${env.GITHUB_REPO}/contents/${path}`;

  // Check if file exists to include sha
  let sha = undefined;
  try {
    const resp = await fetch(url, {
      headers: { 'Authorization': `Bearer ${env.GITHUB_TOKEN}` }
    });
    if (resp.ok) {
      const data = await resp.json();
      sha = data.sha;
    }
  } catch (err) {
    // ignore
  }

  const payload = {
    message: `Orientation update for ${date}`,
    content: content,
    encoding: 'base64'
  };
  if (sha) payload.sha = sha;

  await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
}

// Retrieve latest orientation facts file from GitHub
async function getLatestFacts(env) {
  const prefix = env.GITHUB_PATH_PREFIX || 'orientation';
  const url = `https://api.github.com/repos/${env.GITHUB_REPO}/contents/${prefix}`;
  const resp = await fetch(url, {
    headers: { 'Authorization': `Bearer ${env.GITHUB_TOKEN}` }
  });
  if (!resp.ok) throw new Error('Cannot list repo');
  const list = await resp.json();
  // Find the latest dated file (ISO format) by sorting names descending
  const files = list.filter(item => item.type === 'file' && item.name.endsWith('.json'))
    .sort((a, b) => b.name.localeCompare(a.name));
  if (files.length === 0) throw new Error('No orientation files found');
  const latest = files[0];
  const res = await fetch(latest.download_url, {
    headers: { 'Authorization': `Bearer ${env.GITHUB_TOKEN}` }
  });
  const content = await res.text();
  return JSON.parse(content);
}
