import os
import json
import random
from scipy.stats import pearsonr

def goi_y_kb():
  # Object A
  with open('json_api_user.json', "r") as file:
      object_A = json.load(file)

  # Object B (một danh sách các objects)
  directory = "goi_y_ket_ban"
  file_name = "json_api_get_friends.json"
  file_name_get_friends = os.path.join(directory, file_name)
  with open(file_name_get_friends, "r") as file:
      objects_B = json.load(file)
  # print(objects_B)

  def extract_year(birthday):
    if birthday:
        return birthday.split('/')[-1]
    return ''
  # Hàm tính trọng số giữa hai đối tượng dựa trên số lượng thuộc tính chung
  def calculate_weight(obj_A, obj_B):
      common_attributes = 0
      conditions_met = {}
      object_B_birth_year = 0
      # Kiểm tra xem trường "birthday" có tồn tại trong obj_B không
      if "birthday" in obj_A:
        if "birthday" in obj_B:
            birthday_parts = obj_B["birthday"].split("/")
            # Kiểm tra xem trường "birthday" có đúng định dạng không
            if len(birthday_parts) == 3:
                # Chuyển đổi năm sinh thành số nguyên
                object_B_birth_year = int(birthday_parts[2])
                if object_B_birth_year == int(obj_A["birthday"].split("/")[2]):
                    common_attributes += .2
                    conditions_met["birthday"] = .2
      
      # Kiểm tra xem trường "location" và "work" có tồn tại trong obj_B không
      if "location" in obj_A:
        if "location" in obj_B:
          if obj_B["location"]['id'] == obj_A["location"]['id']:
              common_attributes += .3
              conditions_met["location"] = .3
      if "hometown" in obj_A:
        if "hometown" in obj_B:
          if obj_B["hometown"]['id'] == obj_A["hometown"]['id']:
              common_attributes += .1
              conditions_met["hometown"] = .1
      if "work" in obj_A:
        if "work" in obj_B:
          if obj_B['work'][0]['employer']['id'] == obj_A["work"][0]['employer']['id']:
              common_attributes += .4
              conditions_met["work"] = .4
      return common_attributes, conditions_met

  def compute_jaccard_similarity(user_attr, other_attr):
    user_set = set()
    other_set = set()
    
    if user_attr.get('location'):
        user_set.add(user_attr['location']['id'])
    if other_attr.get('location'):
        other_set.add(other_attr['location']['id'])
        
    if user_attr.get('hometown'):
        user_set.add(user_attr['hometown']['id'])
    if other_attr.get('hometown'):
        other_set.add(other_attr['hometown']['id'])
    
    if user_attr.get('work'):
        user_set.update({job['employer']['id'] for job in user_attr['work']})
    if other_attr.get('work'):
        other_set.update({job['employer']['id'] for job in other_attr['work']})
    
    if extract_year(user_attr.get('birthday')):
        user_set.add(extract_year(user_attr['birthday']))
    if extract_year(other_attr.get('birthday')):
        other_set.add(extract_year(other_attr['birthday']))
    
    intersection = len(user_set.intersection(other_set))
    union = len(user_set.union(other_set))
    
    if union == 0:
        return 0
    
    return intersection / union
  
  def compute_pearson_similarity(user_attr, other_attr):
    # Chuyển đổi các thuộc tính thành dạng số
    def convert_attributes_to_vector(attr):
        vector = [
            hash(extract_year(attr.get('birthday', ''))),
            hash(attr.get('location', {}).get('id', '')),
            hash(attr.get('hometown', {}).get('id', ''))
        ]
        if 'work' in attr:
            for job in attr['work']:
                vector.append(hash(job['employer']['id']))
        return vector

    user_vector = convert_attributes_to_vector(user_attr)
    other_vector = convert_attributes_to_vector(other_attr)
    
    # Đảm bảo các vector có cùng độ dài bằng cách thêm các giá trị 0
    max_length = max(len(user_vector), len(other_vector))
    user_vector += [0] * (max_length - len(user_vector))
    other_vector += [0] * (max_length - len(other_vector))
    
    # Kiểm tra nếu vector là hằng số
    if len(set(user_vector)) == 1 or len(set(other_vector)) == 1:
        return 0

    # Tính Pearson Correlation Coefficient
    if len(user_vector) > 1 and len(other_vector) > 1:
        correlation, _ = pearsonr(user_vector, other_vector)
        return correlation
    else:
        return 0

  file_path = './json_api.json'
  # Đọc dữ liệu từ tệp JSON
  with open(file_path, 'r', encoding='utf-8') as file:
      json_data = json.load(file)


  # print(object_A.get('id') )
  for friend in json_data.get('data', []):
      # Lấy ra 'id' của bạn bè
      friend_id = friend.get('id')
      for key, value in objects_B.items():
          updated_value = []
          for item in value:
              if friend_id != item['id'] and object_A.get('id') != item['id']:
                  updated_value.append(item)
          objects_B[key] = updated_value

  # Tính toán trọng số cho mỗi đối tượng trong object B
  weights = {}
  for key, value in objects_B.items():
      for item in value:
          common_attributes, conditions_met = calculate_weight(object_A, item)
          jaccard_similarity = compute_jaccard_similarity(object_A, item)
          pearson_similarity = compute_pearson_similarity(object_A, item)
          weights[item['id']] = [{
             'weight' : common_attributes,
             'jaccard_similarity': jaccard_similarity,
             'pearson_similarity': pearson_similarity,
             'conditions_met': conditions_met,
             'link': item['link'],
             'name': item['name']
          }]


  # Sắp xếp các đối tượng trong object B theo trọng số giảm dần
  # print (weights)

  filtered_weights = {}
  for key, value in weights.items():
    for item in value:
      if item['weight'] >= 0.1:
          filtered_weights[key] = value
  max_value = 0
  if filtered_weights:
    for key, value in filtered_weights.items():
      # Lặp qua từng giá trị trong dict
      for item in value:
          # Nếu giá trị của key 'weight' lớn hơn max_value, cập nhật max_value
          if item['weight'] > max_value:
              max_value = item['weight']
    # print("Corresponding value:", max_value)
    keys_list = list(filtered_weights.keys())
    # Tạo một từ điển mới để lưu trữ các giá trị nhỏ hơn hoặc bằng max_value
    max_random_values = {}

    for _ in range(min(20, len(keys_list))):
        random_key = random.choice(keys_list)
        random_value = filtered_weights[random_key][0]['weight']
       
        if random_value <= max_value:
            max_random_values[random_key] = filtered_weights[random_key]
            # Kiểm tra nếu số lượng phần tử trong max_random_values vượt quá 20 thì thoát khỏi vòng lặp
            if len(max_random_values) >= 20:
                break
    # print(max_random_values)
    return max_random_values
  return max_random_values


# goi_y_kb()