import math
import json

coverage_data = {
  "executed_lines": [
    1, 3, 6, 7, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 22, 23, 25, 26, 27, 29, 30, 32, 39, 44, 46, 48, 49, 50, 53, 54, 55, 60, 61, 65, 67, 73, 76, 77, 78, 81, 84, 85, 86, 87, 114, 115, 116, 118, 119, 120, 123, 125, 126, 127, 128, 129, 132, 135, 136, 139, 142, 143, 144, 145, 146, 147, 150, 151, 153, 154, 155, 156, 158, 159
  ],
  "missing_lines": [
    5, 15, 17, 21, 24, 28, 31, 33, 34, 35, 36, 40, 43, 47, 52, 57, 63, 64, 70, 75, 79, 83, 88, 89, 91, 92, 95, 96, 98, 99, 100, 101, 102, 103, 105, 108, 110, 111, 121, 122, 124, 130, 133, 140, 141, 152
  ],
  "branches": {
    "[57, 61]": True,
    "[17, 18]": True,
    "[101, 103]": True,
    "[83, 87]": True,
    "[87, 92]": True,
    "[26, 31]": True,
    "[143, 147]": True,
    "[102, 103]": True,
    "[155, 156]": True,
    "[88, 93]": True,
    "[84, 85]": True,
    "[76, 77]": True,
    "[147, 149]": True,
    "[95, 97]": True,
    "[10, 12]": True,
    "[32, 33]": True,
    "[54, 59]": True,
    "[77, 82]": True,
    "[21, 23]": True,
    "[33, 38]": True,
    "[73, 74]": True,
    "[40, 41]": True,
    "[158, 159]": True,
    "[92, 94]": False,
    "[130, 131]": False,
    "[61, 63]": False,
    "[115, 120]": False,
    "[77, 78]": False,
    "[14, 17]": False,
    "[128, 132]": False,
    "[9, 13]": False,
    "[132, 137]": False,
    "[111, 114]": False,
    "[39, 44]": False,
    "[40, 45]": False,
    "[143, 148]": False,
    "[44, 48]": False,
    "[63, 64]": False,
    "[78, 82]": False,
    "[3, 8]": False,
    "[140, 143]": False,
    "[64, 66]": False,
    "[34, 36]": False,
    "[105, 108]": False,
    "[143, 145]": False,
    "[49, 53]": False,
    "[40, 44]": False,
    "[3, 6]": False
  },
  "total_statements": 120,
  "total_branches": 50
}

# 1. line_coverage_pct
executed_lines = coverage_data["executed_lines"]
total_statements = coverage_data["total_statements"]
line_coverage_pct = round(len(executed_lines) / total_statements * 100, 2)

# 2. branch_coverage_pct
branches = coverage_data["branches"]
executed_branches = sum(1 for v in branches.values() if v)
total_branches = coverage_data["total_branches"]
branch_coverage_pct = round(executed_branches / total_branches * 100, 2)

# Group missing lines
missing_lines = sorted(coverage_data["missing_lines"])
groups = []
if missing_lines:
    current_group = [missing_lines[0]]
    for line in missing_lines[1:]:
        if line == current_group[-1] + 1:
            current_group.append(line)
        else:
            groups.append(current_group)
            current_group = [line]
    groups.append(current_group)

# 3. missing_line_runs
missing_line_runs = sum(math.ceil(len(g) / 3) for g in groups)

# 4. critical_missing
critical_missing = max(len(g) for g in groups) if groups else 0

ans = f"{line_coverage_pct:.2f}, {branch_coverage_pct:.2f}, {missing_line_runs}, {critical_missing}"
print(ans)

with open("d:/IIT MADRAS/TDS/GA6/15/answer.txt", "w") as f:
    f.write(ans)
