from pandas import read_csv

df = read_csv('captured.csv',sep=';')


for char in df['characteristic'].unique():
    with open(f"./data/{char}-overnight.txt", 'w') as file:
        file.write('\n'.join(df[df['characteristic'] == char]['data'].unique().tolist()).strip())