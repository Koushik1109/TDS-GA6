import json
import urllib.request
import os

os.makedirs('d:/IIT MADRAS/TDS/GA6/9', exist_ok=True)
url = 'https://exam.sanand.workers.dev/761421b1-ef55-46e1-84bc-e5e1a72b835e'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

counts = {'paraphrase': 0, 'negation': 0, 'near_duplicate': 0}

for pair in data:
    emb_a = pair.get('embedding_a', [])
    emb_b = pair.get('embedding_b', [])
    if not emb_a or not emb_b:
        continue
        
    sim = sum(a * b for a, b in zip(emb_a, emb_b))
    
    threshold = pair['threshold']
    op = pair.get('threshold_op', '')
    
    fails = False
    if op == '>=':
        fails = sim < threshold
    elif op == '<=':
        fails = sim > threshold
    elif op == '>':
        fails = sim <= threshold
    elif op == '<':
        fails = sim >= threshold
    
    if fails:
        counts[pair['type']] += 1

ans = f"{counts['paraphrase']}, {counts['negation']}, {counts['near_duplicate']}"
print(ans)
with open('d:/IIT MADRAS/TDS/GA6/9/answer.txt', 'w') as f:
    f.write(ans)
