import json

with open('24ds3000006_ds_study_iitm_ac_in_embeddings.json', 'r') as f:
    data = json.load(f)

counts = {'paraphrase': 0, 'negation': 0, 'near_duplicate': 0}

for pair in data:
    emb_a = pair['embedding_a']
    emb_b = pair['embedding_b']
    
    sim = sum(a * b for a, b in zip(emb_a, emb_b))
    
    fail = False
    if pair['threshold_op'] == '>=':
        fail = sim < pair['threshold']
    else:
        fail = sim > pair['threshold']
        
    if fail:
        counts[pair['type']] += 1

ans = f"{counts['paraphrase']}, {counts['negation']}, {counts['near_duplicate']}"
print(ans)

with open('answer.txt', 'w') as f:
    f.write(ans)
