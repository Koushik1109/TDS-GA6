import pandas as pd
import numpy as np

def preprocess(df, monotone_col):
    """Normalize and clean records."""
    result = df.copy()
    # Strip whitespace from string columns
    for col in result.select_dtypes(include="object").columns:
        result[col] = result[col].str.strip()
    # Scale numeric columns to 0-1
    for col in result.select_dtypes(include="number").columns:
        mn, mx = result[col].min(), result[col].max()
        if mx > mn:
            result[col] = (result[col] - mn) / (mx - mn)
        else:
            result[col] = 0.0
    # Fill nulls with 0.5
    result = result.fillna(0.5)
    return result

df = pd.read_csv('d:/IIT MADRAS/TDS/GA6/12/24ds3000006_ds_study_iitm_ac_in_records.csv')

# --- Idempotency ---
# Running it twice produces the same result as running it once: f(f(x)) == f(x) for all records. 
# Count records where any column value differs (use tolerance 1e-9 for floats).
res1 = preprocess(df, 'value_a')
res2 = preprocess(res1, 'value_a')

idemp_violations = 0
for i in range(len(df)):
    row_differs = False
    for col in df.columns:
        v1 = res1.loc[i, col]
        v2 = res2.loc[i, col]
        if pd.api.types.is_numeric_dtype(res1[col]):
            if abs(v1 - v2) > 1e-9:
                row_differs = True
                break
        else:
            if v1 != v2:
                row_differs = True
                break
    if row_differs:
        idemp_violations += 1

# --- Monotonicity ---
# For all pairs of records where record A has a strictly higher value in column value_a 
# than record B in the original data, the processed output should also maintain A > B. 
# Count the number of pairs that violate this. Skip pairs where either original value is null.
mono_violations = 0
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        orig_i = df.loc[i, 'value_a']
        orig_j = df.loc[j, 'value_a']
        
        # Skip pairs where either original value is null
        if pd.isna(orig_i) or pd.isna(orig_j):
            continue
            
        if orig_i > orig_j:
            # i should be > j in res1
            processed_i = res1.loc[i, 'value_a']
            processed_j = res1.loc[j, 'value_a']
            if not (processed_i > processed_j):
                mono_violations += 1
        elif orig_j > orig_i:
            # j should be > i in res1
            processed_i = res1.loc[i, 'value_a']
            processed_j = res1.loc[j, 'value_a']
            if not (processed_j > processed_i):
                mono_violations += 1

# --- Null Stability ---
# If a record contains no null values in the input, the output should also contain no null values. 
# Count records that violate this.
null_stab_violations = 0
for i in range(len(df)):
    orig_nulls = df.loc[i].isna().sum()
    if orig_nulls == 0:
        res1_nulls = res1.loc[i].isna().sum()
        if res1_nulls > 0:
            null_stab_violations += 1

print(f"{idemp_violations}, {mono_violations}, {null_stab_violations}")

with open('d:/IIT MADRAS/TDS/GA6/12/answer.txt', 'w') as f:
    f.write(f"{idemp_violations}, {mono_violations}, {null_stab_violations}")
