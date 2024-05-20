import pandas as pd
import json
import requests
def get_info_friends_user(token):
    def get_facebook_friends(excel_file, file_name, access_token):
        url = f"https://graph.facebook.com/me/friends"
        params = {
            'fields': 'id,link,name,gender,birthday,hometown,location,work',
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        json_data  = response.json()
        data_list = json_data.get('data', [])
        df = pd.DataFrame(data_list, columns=['id', 'link', 'name', 'gender', 'birthday', 'hometown', 'location', 'work'])
        # Xử lý các trường hometown, location, và work
        df['hometown'] = df['hometown'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
        df['location'] = df['location'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
        df['work'] = df['work'].apply(lambda x: x[0]['employer']['name'] if isinstance(x, list) and x else '')
        
        df.to_excel(excel_file, index=False)

        # Mở tệp tin để ghi dữ liệu JSON vào
        with open(file_name, "w") as file:
            # Ghi dữ liệu JSON vào tệp tin
            json.dump(json_data, file)

    # Đường dẫn đến tệp JSON chứa danh sách bạn bè
    excel_file = "excel_data.xlsx"
    file_path = './json_api.json'
    access_token = token

    get_facebook_friends(excel_file, file_path, access_token)
