
'''
import pandas as pd
import json



df = pd.read_excel("C:\\Users\\artur.sahakyan\\source\\repos\\contracts\\contracts\\data.xlsx")

contract_ids = df['Պայմանագրի ծածկագիրը'].tolist()

print(contract_ids)


with open('data_list.json', 'w') as file:
    json.dump(contract_ids, file)

'''


import pandas as pd
import json


df = pd.read_excel("C:\\Users\\artur.sahakyan\\source\\repos\\contracts\\contracts\\data.xlsx")

print("Columns in the DataFrame:", df.columns)

df.columns = df.columns.str.strip()


if 'Պատվիրատուի անվանումը' in df.columns:

    grouped_data = df.groupby('Պատվիրատուի անվանումը')['Պայմանագրի ծածկագիրը'].apply(list).to_dict()

    # Write the grouped data to a JSON file
    with open('grouped_data.json', 'w', encoding='utf-8') as file:
        json.dump(grouped_data, file, ensure_ascii=False, indent=4)

    print("JSON ֆայլը հաջողությամբ պահվել է։")
else:
    print("Column 'Պատվիրատուի անվանումը' not found in the DataFrame.")





with open('grouped_data.json', 'r', encoding='utf-8') as file:
    grouped_data = json.load(file)

# Print the loaded data to check
print(grouped_data)