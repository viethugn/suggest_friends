import requests
import pandas as pd
import json
def get_info_user(token):
    def get_facebook_user(excel_file, file_name, user_id, access_token):
        url = f"https://graph.facebook.com/{user_id}"
        params = {
            'fields': 'id,link,name,gender,birthday,hometown,location,work',
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            user_data = response.json()

            # Tạo DataFrame từ dữ liệu người dùng
            df = pd.DataFrame({
                'id': [user_data.get('id')],
                'link': [user_data.get('link')],
                'name': [user_data.get('name')],
                'gender': [user_data.get('gender')],
                'birthday': [user_data.get('birthday')],
                'hometown': [user_data.get('hometown', {}).get('name', '')],
                'location': [user_data.get('location', {}).get('name', '')],
                'work': [user_data.get('work', [{}])[0].get('employer', {}).get('name', '')]
            })

            # Xử lý DataFrame và ghi ra Excel
            df.to_excel(excel_file, index=False)

            # Ghi dữ liệu JSON vào file
            with open(file_name, "w") as file:
                json.dump(user_data, file)
        else:
            print("Yêu cầu không thành công. Mã lỗi:", response.status_code)
    # Đường dẫn đến tệp JSON
    user_id = 'me'
    excel_file = "excel_data_user.xlsx"
    file_path = 'json_api_user.json'
    access_token = token

    get_facebook_user(excel_file, file_path, user_id, access_token)