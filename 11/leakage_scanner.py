import pandas as pd

train_file = "24ds3000006_ds_study_iitm_ac_in_train.csv"
test_file = "24ds3000006_ds_study_iitm_ac_in_test.csv"

train_df = pd.read_csv(train_file)
test_df = pd.read_csv(test_file)

feature_cols = ['age', 'income', 'education', 'hours_per_week']

# Drop duplicates from training set on feature columns to avoid matching multiple times
train_features = train_df[feature_cols].drop_duplicates()

# Merge
merged = pd.merge(test_df, train_features, on=feature_cols, how='left', indicator=True)

leaked_rows = merged[merged['_merge'] == 'both']
clean_rows = merged[merged['_merge'] == 'left_only']

leaked_count = len(leaked_rows)
leaked_accuracy = leaked_rows['is_correct'].mean() * 100
clean_accuracy = clean_rows['is_correct'].mean() * 100
inflation_pp = 79.33 - clean_accuracy

output = f"{leaked_count}, {leaked_accuracy:.2f}, {clean_accuracy:.2f}, {inflation_pp:.2f}"
print(output)

with open('result.txt', 'w') as f:
    f.write(output)
