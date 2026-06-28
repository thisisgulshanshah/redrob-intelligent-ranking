import pandas as pd
df = pd.read_csv("submissions/submission.csv")
df.to_excel("submissions/submission.xlsx", index=False)
print("Wrote submissions/submission.xlsx")
