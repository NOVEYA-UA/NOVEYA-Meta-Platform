import math

def compute_coherence(nodes):
    values = list(nodes.values())
    avg = sum(values)/len(values)
    variance = sum((v-avg)**2 for v in values)/len(values)
    return 1/(1+variance)

def compute_eff(recognition, costs):
    return recognition/(costs+1)

def compute_entropy(values):
    total=sum(values)
    probs=[v/total for v in values if v>0]
    return -sum(p*math.log(p) for p in probs)
