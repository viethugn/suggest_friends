from scipy.stats import pearsonr
import time
import json
import os
import numpy as np

# Dữ liệu người dùng mẫu
users = {
    'user': {"id": "100047415604756", "link": "https://www.facebook.com/profile.php?id=100047415604756", "name": "Nguyễn Hưng", "gender": "male", "birthday": "01/02/2001", "hometown": {"id": "109205905763791", "name": "Nha Trang"}, "location": {"id": "109205905763791", "name": "Nha Trang"}, "work": [{"end_date": "0000-00","employer": {"id": "905415882814945", "name": "B\u1ea3o Vi\u1ec7t Nh\u00e2n Th\u1ecd"},"location": {"id": "109205905763791","name": "Nha Trang"},"position": {"id": "108540055843663","name": "Financial Advisor"},"start_date": "0000-00","id": "100416909602151"},{"end_date": "0000-00", "employer": {"id": "486298361825151", "name": "Freelancer IT"}, "start_date": "2023-11-12"}, ]},
}
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

# def calculate_weight(obj_A, obj_B):
#       common_attributes = 0
#       conditions_met = {}
#       object_B_birth_year = 0
#       # Kiểm tra xem trường "birthday" có tồn tại trong obj_B không
#       if "birthday" in obj_A:
#         if "birthday" in obj_B:
#             birthday_parts = obj_B["birthday"].split("/")
#             # Kiểm tra xem trường "birthday" có đúng định dạng không
#             if len(birthday_parts) == 3:
#                 # Chuyển đổi năm sinh thành số nguyên
#                 object_B_birth_year = int(birthday_parts[2])
#                 if object_B_birth_year == int(obj_A["birthday"].split("/")[2]):
#                     common_attributes += .2
      
#       # Kiểm tra xem trường "location" và "work" có tồn tại trong obj_B không
#       if "location" in obj_A:
#         if "location" in obj_B:
#           if obj_B["location"]['id'] == obj_A["location"]['id']:
#               common_attributes += .3
#       if "hometown" in obj_A:
#         if "hometown" in obj_B:
#           if obj_B["hometown"]['id'] == obj_A["hometown"]['id']:
#               common_attributes += .1
#       if "work" in obj_A and "work" in obj_B:
#         work_match_found = False  # Cờ để theo dõi xem có công việc trùng khớp nào được tìm thấy hay không
#         for job_A in obj_A["work"]:
#             for job_B in obj_B["work"]:
#                 if job_A['employer']['id'] == job_B['employer']['id']:
#                     common_attributes += 0.4
#                     if not work_match_found:  # Nếu chưa tìm thấy công việc trùng khớp nào trước đó
#                         conditions_met["work"] = 0.4
#                         work_match_found = True  # Đánh dấu rằng đã tìm thấy công việc trùng khớp
#                     break  # Khi tìm thấy một công việc trùng khớp, không cần kiểm tra các công việc khác
#             if work_match_found:  # Nếu đã tìm thấy công việc trùng khớp, không cần tiếp tục vòng lặp ngoài
#                 break
#       return common_attributes

# # Đo thời gian xử lý Jaccard Similarity
# start_time = time.time()
# for value in data_list:
#     print(calculate_weight(users['user'], value))
# # similarity = calculate_weight(users['user'], data_list)
# end_time = time.time()
# # print(f"Thuộc tính chung: {similarity}")
# print(f"Thời gian xử lý calculate_weight: {((end_time - start_time) * 1000):.3f} mili giây")

# def compute_jaccard_similarity(user_attr, other_attr):
#     def convert_attributes_to_set(attr):
#         attribute_set = set()
#         attribute_set.add(attr.get('birthday', '').split('/')[-1])  # Lấy năm sinh
#         attribute_set.add(attr.get('location', {}).get('id', ''))
#         attribute_set.add(attr.get('hometown', {}).get('id', ''))
#         if 'work' in attr:
#             for job in attr['work']:
#                 attribute_set.add(job['employer']['id'])
#         return attribute_set
    
#     user_set = convert_attributes_to_set(user_attr)
#     other_set = convert_attributes_to_set(other_attr)
    
#     intersection = len(user_set & other_set)
#     union = len(user_set | other_set)

#     if union == 0:
#         return 0
    
#     return intersection / union

# # Đo thời gian xử lý Jaccard Similarity
# start_time = time.time()
# for value in data_list:
#     print(compute_jaccard_similarity(users['user'], value))
# end_time = time.time()
# print(f"Thời gian xử lý Jaccard Similarity: {((end_time - start_time) * 1000):.3f} mili giây")

def compute_pearson_similarity(user_attr, other_attr):
    def convert_attributes_to_vector(attr):
        vector = [
            hash(attr.get('birthday', '').split('/')[-1]),
            hash(attr.get('location', {}).get('id', '')),
            hash(attr.get('hometown', {}).get('id', ''))
        ]
        if 'work' in attr:
            for job in attr['work']:
                vector.append(hash(job['employer']['id']))
        return vector

    user_vector = convert_attributes_to_vector(user_attr)
    other_vector = convert_attributes_to_vector(other_attr)

    if len(user_vector) != len(other_vector):
        min_len = min(len(user_vector), len(other_vector))
        user_vector = user_vector[:min_len]
        other_vector = other_vector[:min_len]

    # Kiểm tra xem các vector có phải là hằng số không
    if np.std(user_vector) == 0 or np.std(other_vector) == 0:
        return 0  # Hoặc giá trị tương tự để biểu thị không có sự tương quan

    correlation, _ = pearsonr(user_vector, other_vector)
    return correlation
# Đo thời gian xử lý Pearson Correlation
start_time = time.time()
for value in data_list:
  print(compute_pearson_similarity(users['user'], value))

end_time = time.time()

print(f"Thời gian xử lý Pearson Correlation: {((end_time - start_time) * 1000):.3f} mili giây")