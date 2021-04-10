import os

with open(os.path.dirname(os.path.abspath(input())) + '\data.tsv', 'r', encoding='utf-8') as file:
    for i in range(500):
        line = next(file).strip()
        print(line)

