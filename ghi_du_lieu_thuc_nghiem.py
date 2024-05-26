import pandas as pd
import json
import requests
import os

def get_facebook_friends(excel_file):
    directory = "goi_y_ket_ban"
    json_api_get_friends = "json_api_get_friends.json"
    file_json_api_get_friends = os.path.join(directory, json_api_get_friends)
    with open(file_json_api_get_friends, 'r', encoding='utf-8') as file:
        get_data_thuc_nghiem = json.load(file)
    data_list =[]
    for key, value in get_data_thuc_nghiem.items():
      if(key == '100014210508821'):
        print(key)
        for item in value:
            data_list.append(item)
      # break
    
    df = pd.DataFrame(data_list, columns=['id', 'link', 'name', 'gender', 'birthday', 'hometown', 'location', 'work'])
    # Xử lý các trường hometown, location, và work
    df['hometown'] = df['hometown'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
    df['location'] = df['location'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
    df['work'] = df['work'].apply(lambda x: x[0]['employer']['name'] if isinstance(x, list) and x else '')
    
    df.to_excel(excel_file, index=False)


# Đường dẫn đến tệp JSON chứa danh sách bạn bè
excel_file = "excel_data_thuc_nghiem.xlsx"

get_facebook_friends(excel_file)
