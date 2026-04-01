from core_metatron import init_db
from logic import compute_coherence, compute_eff, compute_entropy

init_db()
nodes={'n1':1.0,'n2':0.9,'n3':1.1}
coherence=compute_coherence(nodes)
eff=compute_eff(10,5)
entropy=compute_entropy(list(nodes.values()))
print('Initialized',coherence,eff,entropy)
