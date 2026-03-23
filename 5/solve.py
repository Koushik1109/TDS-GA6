import pandas as pd
import numpy as np

def validate_data():
    day1 = pd.read_csv('24ds3000006_ds_study_iitm_ac_in.day1.csv')
    day2 = pd.read_csv('24ds3000006_ds_study_iitm_ac_in.day2.csv')

    bad_rows = set()
    today = pd.Timestamp.today()
    
    with open('log_output.txt', 'w', encoding='utf-8') as f:
        for col in day1.columns:
            col_flags = set()
            
            # Rule 1: 0 nulls in Day 1
            if day1[col].isnull().sum() == 0:
                null_mask = day2[col].isnull()
                flagged = day2[null_mask].index.tolist()
                col_flags.update(flagged)
                bad_rows.update(flagged)
                f.write(f"[{col}] 0-null rule flagged {len(flagged)} rows\n")

            # Type detection
            is_numeric = False
            is_date = False
            is_cat = False

            numeric_s1 = pd.to_numeric(day1[col], errors='coerce')
            if numeric_s1.notnull().mean() > 0.95:
                is_numeric = True
            else:
                date_s1 = pd.to_datetime(day1[col], errors='coerce', format='mixed')
                if date_s1.notnull().mean() > 0.90:
                    is_date = True
                else:
                    if day1[col].nunique(dropna=True) <= 20:
                        is_cat = True

            f.write(f"[{col}] Type: Numeric={is_numeric}, Date={is_date}, Cat={is_cat}\n")
            
            if is_numeric:
                s1_min = numeric_s1.min()
                s1_max = numeric_s1.max()
                numeric_s2 = pd.to_numeric(day2[col], errors='coerce')
                
                mask = (numeric_s2 < s1_min) | (numeric_s2 > s1_max)
                flagged = day2[mask].index.tolist()
                col_flags.update(flagged)
                bad_rows.update(flagged)
                f.write(f"[{col}] Numeric rule flagged {len(flagged)} rows\n")
                
            elif is_date:
                date_s2 = pd.to_datetime(day2[col], errors='coerce', format='mixed')
                mask = date_s2 > today
                flagged = day2[mask].index.tolist()
                col_flags.update(flagged)
                bad_rows.update(flagged)
                f.write(f"[{col}] Date rule flagged {len(flagged)} rows\n")
                
            elif is_cat:
                day2_not_null = day2[col].notnull()
                mask = ~day2[col].isin(day1[col].dropna()) & day2_not_null
                flagged = day2[mask].index.tolist()
                col_flags.update(flagged)
                bad_rows.update(flagged)
                f.write(f"[{col}] Categorical rule flagged {len(flagged)} rows\n")
                
        f.write(f"Total unique anomalous rows: {len(bad_rows)}\n")
        
    with open('final_answer.txt', 'w', encoding='utf-8') as f:
        f.write(str(len(bad_rows)))

if __name__ == '__main__':
    validate_data()
