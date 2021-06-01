import pandas as pd
import os

dirname= os.getcwd()
df= pd.DataFrame()
total_comm=0
for filename in os.listdir(dirname):
    root, ext = os.path.splitext(filename)
    if root.startswith('database') and ext == '.csv':
        df1 = pd.read_csv(filename,sep=";")
        print("adding " + str(len(df1)) + " new comments")
        total_comm=total_comm+len(df1)
        df = pd.concat([df, df1], ignore_index=True)

print(total_comm)
print(len(df))

df.to_csv("full_database.csv", index=False, header=True)