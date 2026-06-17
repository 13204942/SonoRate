import os
import numpy as np
import pandas as pd

DATA_ROOT = '../data/rank'

DATA_LABEL = 'hc18'
SAVED_CSV = DATA_ROOT + '/hc18_rank.csv'
# DATA_LABEL = 'estt'
# SAVED_CSV = DATA_ROOT + '/estt_rank.csv'

DOC_A = DATA_ROOT + f'/doc_a_shi/{DATA_LABEL}'
DOC_A_J = DATA_ROOT + f'/doc_a_junior/{DATA_LABEL}'
DOC_C = DATA_ROOT + f'/doc_c_yu/{DATA_LABEL}'
DOC_D = DATA_ROOT + f'/doc_d_huang/{DATA_LABEL}'
DOC_E = DATA_ROOT + f'/non_doc_fang/{DATA_LABEL}'
DOC_F = DATA_ROOT + f'/non_doc_modan/{DATA_LABEL}'

df = pd.DataFrame(columns=['img', 'doctor', 'M1', 'M2', 'M3', 'M4', 'M5'])

i = 0

for file in os.listdir(DOC_A):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_A + '/' + filename, sep=" ", header=None)
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_A", m1_rank, m2_rank, m3_rank, m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor A ranking!')

for file in os.listdir(DOC_A_J):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_A_J + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_B", m1_rank, m2_rank, m3_rank,
                           m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor B ranking!')

for file in os.listdir(DOC_C):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_C + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_C", m1_rank, m2_rank, m3_rank,
                           m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor C ranking!')

for file in os.listdir(DOC_D):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_D + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_D", m1_rank, m2_rank, m3_rank,
                           m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor D ranking!')

for file in os.listdir(DOC_E):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_E + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_E", m1_rank, m2_rank, m3_rank,
                           m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor E ranking!')

for file in os.listdir(DOC_F):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_F + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        m1 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay1")][0].values[0]
        m1_rank = m1.split(',')[1]
        m2 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay2")][0].values[0]
        m2_rank = m2.split(',')[1]
        m3 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay3")][0].values[0]
        m3_rank = m3.split(',')[1]
        m4 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay4")][0].values[0]
        m4_rank = m4.split(',')[1]
        m5 = tmp_df[tmp_df.iloc[:, 0].str.contains("overlay5")][0].values[0]
        m5_rank = m5.split(',')[1]

        df.loc[len(df)] = [img_name, "Doc_F", m1_rank, m2_rank, m3_rank,
                           m4_rank, m5_rank]

        i += 1
print(f'Finished Doctor F ranking!')

# Fill out AI's ranking
for file in os.listdir(DOC_A):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        tmp_df = pd.read_csv(DOC_A + '/' + filename, sep=" ", header=None)
        # continue
        img_name = tmp_df.iloc[2, 0].replace(',', '')
        # M1 < M2 < M3 < M4 < M5
        df.loc[len(df)] = [img_name, "AI", 1, 2, 3, 4, 5]

        i += 1
print(f'Finished AI ranking!')

# save the dataframe as a csv file
print(f'Dataframe shape: {df.shape}')
df.to_csv(SAVED_CSV)

print(f'Finished All Doctors'' rankings!')
