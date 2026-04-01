import http.server, socketserver, json, os

PORT = 18792
TOKEN = "86214041b65d66668383a69368d30e38"

class RelayHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "active", "version": "RO2"}).encode())
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'{"success":true}')

print(f"🦞 Реле активно на {PORT}")
with socketserver.TCPServer(('127.0.0.1', PORT), RelayHandler) as httpd:
    httpd.serve_forever()
