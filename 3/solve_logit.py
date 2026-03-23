import math

fragments = [
    {'id': 1, 'wc': 5, 'o': 1.0, '41': -0.01, '41m': 0.75, '5m': 0.52},
    {'id': 2, 'wc': 7, 'o': -0.16, '41': 0.51, '41m': -0.31, '5m': -0.83},
    {'id': 3, 'wc': 11, 'o': 0.96, '41': 0.99, '41m': -0.09, '5m': -0.42},
    {'id': 4, 'wc': 8, 'o': 0.98, '41': 1.32, '41m': 0.66, '5m': -0.14},
    {'id': 5, 'wc': 13, 'o': -0.21, '41': 0.02, '41m': 0.18, '5m': -0.32},
    {'id': 6, 'wc': 7, 'o': -0.06, '41': 0.57, '41m': 0.2, '5m': 0.53},
    {'id': 7, 'wc': 10, 'o': 1.2, '41': 0.36, '41m': 1.11, '5m': 1.0},
    {'id': 8, 'wc': 9, 'o': 0.38, '41': 0.56, '41m': 0.37, '5m': -0.23},
    {'id': 9, 'wc': 16, 'o': 1.28, '41': 0.24, '41m': 0.05, '5m': -0.12},
    {'id': 10, 'wc': 11, 'o': 0.76, '41': 0.08, '41m': 0.84, '5m': 1.02},
    {'id': 11, 'wc': 11, 'o': 0.82, '41': 0.35, '41m': 0.84, '5m': 1.33},
    {'id': 12, 'wc': 17, 'o': 0.77, '41': 0.31, '41m': 0.73, '5m': 0.06},
    {'id': 13, 'wc': 13, 'o': 0.87, '41': 0.26, '41m': 0.73, '5m': 0.87},
    {'id': 14, 'wc': 16, 'o': 0.48, '41': 1.29, '41m': 1.03, '5m': 1.18},
    {'id': 15, 'wc': 14, 'o': -0.1, '41': 0.33, '41m': 0.25, '5m': 1.3},
    {'id': 16, 'wc': 11, 'o': -0.05, '41': 1.34, '41m': 1.11, '5m': 1.11},
    {'id': 17, 'wc': 15, 'o': 1.31, '41': 0.58, '41m': 0.47, '5m': 1.06},
    {'id': 18, 'wc': 16, 'o': 0.56, '41': 0.02, '41m': 1.64, '5m': 0.15},
    {'id': 19, 'wc': 13, 'o': 1.22, '41': 0.75, '41m': 1.4, '5m': 0.76},
    {'id': 20, 'wc': 5, 'o': -0.35, '41': 0.61, '41m': 0.85, '5m': 0.23},
    {'id': 21, 'wc': 9, 'o': -0.17, '41': 0.64, '41m': 0.63, '5m': 0.93},
]

pairs = {
    (14,15): 0.64, (5,16): 0.21, (2,8): -0.64, (3,7): 0.29,
    (4,10): -0.53, (4,7): -0.66, (1,2): -0.1, (1,12): -0.05,
    (2,21): 0.45, (3,21): 0.51, (17,20): 0.43, (2,5): -0.25,
    (1,13): -0.05, (5,10): 0.32, (5,8): -0.25, (14,19): -0.12,
    (15,19): 0.21, (9,12): -0.31, (10,16): 0.2, (7,10): 0.21,
    (11,12): 0.67, (8,17): 0.64, (1,6): 0.38, (4,15): -0.12,
    (12,21): -0.34, (9,18): -0.3, (7,19): 0.62, (11,15): 0.19,
    (4,17): -0.54, (10,19): 0.53, (13,17): 0.69, (6,19): 0.67,
    (7,9): -0.21, (16,21): -0.45, (14,20): 0.43, (16,20): 0.05,
    (12,14): -0.18, (6,8): 0.16, (7,8): 0.61, (9,14): -0.62,
    (1,3): 0.02, (17,18): 0.16,
}

base_o = -2.15
base_41 = -0.63
base_41m = -2.66
base_5m = -0.46

def logit_to_prob(logit):
    return 100.0 / (1.0 + math.exp(-logit))

best_wc = 999
best_sol = None

def search(idx, current_wc, o, f41, f41m, f5m, selected):
    global best_wc, best_sol
    
    if current_wc >= best_wc:
        return
        
    p_o = logit_to_prob(o)
    p_41 = logit_to_prob(f41)
    p_41m = logit_to_prob(f41m)
    p_5m = logit_to_prob(f5m)
    
    mean = (p_o + p_41 + p_41m + p_5m) / 4.0
    floor = min(p_o, p_41, p_41m, p_5m)
    
    # Check if validity is met
    if mean >= 97.0 and floor >= 92.0:
        if current_wc < best_wc:
            best_wc = current_wc
            best_sol = (list(selected), mean, floor)
            
    if idx == 21:
        return
        
    f = fragments[idx]
    
    # Try including
    fid = f['id']
    new_o = o + f['o']
    new_41 = f41 + f['41']
    new_41m = f41m + f['41m']
    new_5m = f5m + f['5m']
    
    for p, v in pairs.items():
        if fid == p[0] and p[1] in selected:
            new_o += v; new_41 += v; new_41m += v; new_5m += v
        elif fid == p[1] and p[0] in selected:
            new_o += v; new_41 += v; new_41m += v; new_5m += v
            
    selected.add(fid)
    search(idx + 1, current_wc + f['wc'], new_o, new_41, new_41m, new_5m, selected)
    selected.remove(fid)
    
    # Try excluding
    search(idx + 1, current_wc, o, f41, f41m, f5m, selected)

search(0, 0, base_o, base_41, base_41m, base_5m, set())

if best_sol:
    comb, mean_prob, floor_prob = best_sol
    comb.sort()
    print("Best Comb:", comb)
    print("WC:", best_wc)
    print("Mean%:", round(mean_prob, 2))
    print("Floor%:", round(floor_prob, 2))
else:
    print("No solution found!")

