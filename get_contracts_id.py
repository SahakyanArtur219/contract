import pandas as pd
import json



df = pd.read_excel("C:\\Users\\artur.sahakyan\\source\\repos\\contracts\\contracts\\data.xlsx")

contract_ids = df['Պայմանագրի ծածկագիրը'].tolist()

print(contract_ids)


with open('data_list.json', 'w') as file:
    json.dump(contract_ids, file)

