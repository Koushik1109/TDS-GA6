import csv
import re
import sys

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = text.strip()
    if not text:
        return []
    return [w for w in re.split(r'\s+', text) if len(w) > 0]

def ngrams(tokens, n):
    s = set()
    for i in range(len(tokens) - n + 1):
        s.add(" ".join(tokens[i:i+n]))
    return s

def overlap_score(question, corpus_ngrams, n=8):
    qt = tokenize(question)
    if len(qt) < n:
        return 0
    qg = ngrams(qt, n)
    hits = 0
    for g in qg:
        if g in corpus_ngrams:
            hits += 1
    return hits / len(qg) if len(qg) > 0 else 0

def main():
    questions_file = "d:/IIT MADRAS/TDS/GA6/10/24ds3000006_ds_study_iitm_ac_in_questions.csv"
    corpus_file = "d:/IIT MADRAS/TDS/GA6/10/24ds3000006_ds_study_iitm_ac_in_corpus.txt"

    with open(corpus_file, 'r', encoding='utf-8') as f:
        corpus_text = f.read()

    corpus_tokens = tokenize(corpus_text)
    corpus_ngrams_set = ngrams(corpus_tokens, 8)

    total_questions = 0
    correct_all = 0
    contaminated_count = 0
    non_contam_questions = 0
    correct_non_contam = 0
    
    with open(questions_file, 'r', encoding='utf-8') as f:
        # Detect if there's a BOM and remove it if so
        content = f.read()
        if content.startswith('\ufeff'):
            content = content[1:]
        
        reader = csv.DictReader(content.splitlines())
        
        for row in reader:
            q_text = row['question']
            is_correct = int(row['is_correct'])
            
            total_questions += 1
            correct_all += is_correct
            
            score = overlap_score(q_text, corpus_ngrams_set, 8)
            
            if score > 0.4:
                contaminated_count += 1
            else:
                non_contam_questions += 1
                correct_non_contam += is_correct

    reported_accuracy = (correct_all / total_questions * 100) if total_questions > 0 else 0
    adjusted_accuracy = (correct_non_contam / non_contam_questions * 100) if non_contam_questions > 0 else 0

    ans = f"{contaminated_count}, {reported_accuracy:.2f}, {adjusted_accuracy:.2f}"
    print(ans)
    
    with open("d:/IIT MADRAS/TDS/GA6/10/answer.txt", "w", encoding="utf-8") as f:
        f.write(ans)

if __name__ == '__main__':
    main()
