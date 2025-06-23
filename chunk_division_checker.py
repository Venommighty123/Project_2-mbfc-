# This codeframw was used to test the chunks created

import csv
import pandas as pd
import ast

df = pd.read_csv("claim_analysis_4.csv")

for i in range(5, 11):
    print("#"*100)
    chunks_str = df.iloc[i, 4]
    chunks = ast.literal_eval(chunks_str)
    for chunk in chunks:
        print(chunk)
        print("$"*100)
    break