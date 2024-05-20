# import networkx as nx
# import matplotlib.pyplot as plt
# import community

# # Tạo đồ thị
# G = nx.Graph()
# G.add_node(1, name="Alice", birthday="01/01/1990", location="Hanoi", work="Company A")
# G.add_node(2, name="Bob", birthday="02/02/1990", location="Hanoi", work="Company B")
# G.add_node(3, name="Charlie", birthday="03/03/1992", location="HCMC", work="Company A")
# G.add_node(4, name="David", birthday="04/04/1993", location="Danang", work="Company C")
# G.add_edges_from([(1, 2), (2, 3), (3, 4)])

# # Tính toán Degree Centrality
# degree_centrality = nx.degree_centrality(G)
# print("Degree Centrality:", degree_centrality)

# # Tính toán Closeness Centrality
# closeness_centrality = nx.closeness_centrality(G)
# print("Closeness Centrality:", closeness_centrality)

# # Tính toán Betweenness Centrality
# betweenness_centrality = nx.betweenness_centrality(G)
# print("Betweenness Centrality:", betweenness_centrality)

# # Tính toán Common Neighbors
# common_neighbors = [(u, v, len(list(nx.common_neighbors(G, u, v)))) for u, v in nx.non_edges(G)]
# print("Common Neighbors:", common_neighbors)

# # Tính toán Jaccard Coefficient
# jaccard_coeff = list(nx.jaccard_coefficient(G))
# print("Jaccard Coefficient:", jaccard_coeff)

# # Tính toán Adamic/Adar Index
# adamic_adar = list(nx.adamic_adar_index(G))
# print("Adamic/Adar Index:", adamic_adar)

# # Vẽ đồ thị
# pos = nx.spring_layout(G)
# part = community.best_partition(G)
# values = [part.get(node) for node in G.nodes()]
# plt.figure(figsize=(10, 10))
# nx.draw_networkx(G, pos=pos, cmap=plt.get_cmap('jet'), node_color=values, node_size=500, with_labels=True)
# plt.show()


# -----------------------------------------------------------------------------------
# import networkx as nx

# # Tạo đồ thị mạng xã hội
# G = nx.Graph()

# # Thêm các cạnh (edges) và đỉnh (nodes) vào đồ thị
# G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])

# # Hàm gợi ý kết bạn dựa trên Common Neighbors
# def recommend_common_neighbors(G, user):
#     neighbors = list(G.neighbors(user))
#     recommended_users = []
#     for neighbor in neighbors:
#         recommended_users.extend(list(G.neighbors(neighbor)))
#     recommended_users = list(set(recommended_users) - set(neighbors) - set([user]))
#     return recommended_users

# # Hàm gợi ý kết bạn dựa trên Friend-of-Friend (FoF) Recommendation
# def recommend_fof(G, user):
#     friends = list(G.neighbors(user))
#     fof_recommendations = []
#     for friend in friends:
#         fof_recommendations.extend(list(G.neighbors(friend)))
#     fof_recommendations = list(set(fof_recommendations) - set(friends) - set([user]))
#     return fof_recommendations

# # Sử dụng hàm gợi ý kết bạn cho một người dùng cụ thể (ví dụ: người dùng có ID là 1)
# user_id = 1
# common_neighbors_recommendations = recommend_common_neighbors(G, user_id)
# fof_recommendations = recommend_fof(G, user_id)

# print("Common Neighbors Recommendations for User", user_id, ":", common_neighbors_recommendations)
# print("FoF Recommendations for User", user_id, ":", fof_recommendations)
# --------------------------------------------------------
# import networkx as nx
# import pickle
# import numpy as np
# import json
# import os

# edges = []
# CENTRAL_ID = 'me'
# nodes = [CENTRAL_ID]
# GRAPH_FILENAME = 'friend_graph.pickle'

# # Thêm các cạnh (edges)
# def calculate_weight(obj_A, obj_B):
#       common_attributes = 0
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
#       if "work" in obj_A:
#         if "work" in obj_B:
#           if obj_B['work'][0]['employer']['id'] == obj_A["work"][0]['employer']['id']:
#               common_attributes += .4
#         return common_attributes


# file_path = './json_api.json'
# # Đọc dữ liệu từ tệp JSON
# with open(file_path, 'r', encoding='utf-8') as file:
#     json_data = json.load(file)
# with open('json_api_user.json', "r") as file:
#       object_A = json.load(file)

# # Object B (một danh sách các objects)
# directory = "goi_y_ket_ban"
# file_name = "json_api_get_friends.json"
# file_name_get_friends = os.path.join(directory, file_name)
# with open(file_name_get_friends, "r") as file:
#     objects_B = json.load(file)
# # print(object_A.get('id') )
# for friend in json_data.get('data', []):
#     # Lấy ra 'id' của bạn bè
#     friend_id = friend.get('id')
#     for key, value in objects_B.items():
#         updated_value = []
#         for item in value:
#             if friend_id != item['id'] and object_A.get('id') != item['id']:
#                 updated_value.append(item)
#         objects_B[key] = updated_value

# import matplotlib.pyplot as plt
# import community
# # Tính toán trọng số cho mỗi đối tượng trong object B
# friends_of_friends = {}
# weights = {}
# for key, value in objects_B.items():
#     for item in value:
#         common_attributes = calculate_weight(object_A, item)
#         friends_of_friends[item['id']] = item['id']
# # print(friends_of_friends)

# #chuyển đối tượng thành danh sách cạnh
# for k, v in friends_of_friends.items():
#     edges.append((CENTRAL_ID, k))
# # print(edges)

# G = nx.Graph()
# G.add_nodes_from([CENTRAL_ID])

# G.add_nodes_from(friends_of_friends.keys())

# G.add_edges_from(edges)

# pos = nx.spring_layout(G)

# part = community.best_partition(G)
# values = [part.get(node) for node in G.nodes()]

# plt.figure(figsize=(10, 10))
# nx.draw_networkx(G, pos=pos, cmap=plt.get_cmap('jet'), node_color=values, node_size=10, edge_color='grey', with_labels=False, font_size=10)
# plt.title("Friendship Graph with Common Attributes")
# plt.show()

# Tính các biện pháp centrality
# degree_centrality = nx.degree_centrality(G)
# closeness_centrality = nx.closeness_centrality(G)
# betweenness_centrality = nx.betweenness_centrality(G)
# print(closeness_centrality)
# # Gợi ý bạn bè dựa trên thuộc tính chung
# def suggest_friends(user, G):
#     user_attributes = G.nodes[user]
#     suggestions = []
    
#     for other in G.nodes:
#         print(other)
#         if other != user and not G.has_edge(user, other):
#             # common_attributes = 0
#             # So sánh từng thuộc tính
#             # if 'location' in user_attributes and 'location' in G.nodes[other] and user_attributes['location'] == G.nodes[other]['location']:
#             #     common_attributes += 1
#             # if 'work' in user_attributes and 'work' in G.nodes[other] and user_attributes['work'] == G.nodes[other]['work']:
#             #     common_attributes += 1
#             # if 'birthday' in user_attributes and 'birthday' in G.nodes[other] and user_attributes['birthday'] == G.nodes[other]['birthday']:
#             #     common_attributes += 1
            
#             # Thêm các thuộc tính khác nếu cần
            
#             # if common_attributes > 0:
#                 # Gộp các thuộc tính và biện pháp centrality để xếp hạng
#                 score = (common_attributes, 
#                          degree_centrality[other], 
#                          closeness_centrality[other], 
#                          betweenness_centrality[other])
#                 suggestions.append((other, score))
    
#     # Sắp xếp theo số lượng thuộc tính chung, sau đó theo centrality
#     suggestions.sort(key=lambda x: (-x[1][0], -x[1][1], -x[1][2], -x[1][3]))
#     return suggestions

# # Gợi ý bạn bè cho người dùng 1 (Alice)
# suggestions = suggest_friends('me', G)
# print("Gợi ý bạn bè cho Alice:", suggestions)

# ------------------------------------------------------------
from scipy.stats import pearsonr

# Dữ liệu người dùng mẫu
users = {
    'user': {"id": "100047415604756", "link": "https://www.facebook.com/profile.php?id=100047415604756", "name": "Nguyễn Hưng", "gender": "male", "birthday": "01/02/2001", "hometown": {"id": "109205905763791", "name": "Nha Trang"}, "location": {"id": "109205905763791", "name": "Nha Trang"}, "work": [{"end_date": "0000-00", "employer": {"id": "486298361825151", "name": "Freelancer IT"}, "start_date": "2023-11-12"}]},
    '100022280481195': [
        {"id": "61551707062001", "link": "https://www.facebook.com/truongthidiemphuc", "name": "Trương Thị Diễm Phúc", "gender": "male", "birthday": "01/02/2001", "hometown": {"id": "109205905763791", "name": "Nha Trang"}, "location": {"id": "109205905763791", "name": "Nha Trang"}, "work": [{"end_date": "0000-00", "employer": {"id": "486298361825151", "name": "Freelancer IT"}, "start_date": "2023-11-12"}, {
                    "end_date": "0000-00",
                    "employer": {
                        "id": "905415882814945",
                        "name": "B\u1ea3o Vi\u1ec7t Nh\u00e2n Th\u1ecd"
                    },
                    "location": {
                        "id": "109205905763791",
                        "name": "Nha Trang"
                    },
                    "position": {
                        "id": "108540055843663",
                        "name": "Financial Advisor"
                    },
                    "start_date": "0000-00",
                    "id": "100416909602151"
                },  {
                    "end_date": "0000-00",
                    "employer": {
                        "id": "405756550159735",
                        "name": "Thaco Bus"
                    },
                    "location": {
                        "id": "105773999462846",
                        "name": "Tam K\u1ef3"
                    },
                    "position": {
                        "id": "634512476694954",
                        "name": "Electrical Engineer"
                    },
                    "start_date": "0000-00",
                    "id": "100409616269547"
                }]},
        {"id": "61556987754070", "link": "https://www.facebook.com/profile.php?id=61556987754070", "name": "Quỳnh Quỳnh", "gender": "female", "birthday": "01/01/2000", "location": {"id": "109205905763791", "name": "Nha Trang"}},
        {"id": "61557253190333", "link": "https://www.facebook.com/profile.php?id=61557253190333", "name": "Vinh Tran", "gender": "male", "birthday": "03/06/2003", "hometown": {"id": "110100332345949", "name": "Ninh Hòa"}}
    ]
}


import time

def calculate_weight(obj_A, obj_B):
      common_attributes = 0
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
      
      # Kiểm tra xem trường "location" và "work" có tồn tại trong obj_B không
      if "location" in obj_A:
        if "location" in obj_B:
          if obj_B["location"]['id'] == obj_A["location"]['id']:
              common_attributes += .3
      if "hometown" in obj_A:
        if "hometown" in obj_B:
          if obj_B["hometown"]['id'] == obj_A["hometown"]['id']:
              common_attributes += .1
      if "work" in obj_A:
        if "work" in obj_B:
          if obj_B['work'][0]['employer']['id'] == obj_A["work"][0]['employer']['id']:
              common_attributes += .4
      return common_attributes

# Đo thời gian xử lý Jaccard Similarity
start_time = time.time()
similarity = calculate_weight(users['user'], users['100022280481195'][0])
end_time = time.time()

print(f"Thuộc tính chung: {similarity}")
print(f"Thời gian xử lý calculate_weight: {end_time - start_time} giây")


def compute_jaccard_similarity(user_attr, other_attr):
    def convert_attributes_to_set(attr):
        attribute_set = set()
        attribute_set.add(attr.get('birthday', '').split('/')[-1])  # Lấy năm sinh
        attribute_set.add(attr.get('location', {}).get('id', ''))
        attribute_set.add(attr.get('hometown', {}).get('id', ''))
        if 'work' in attr:
            for job in attr['work']:
                attribute_set.add(job['employer']['id'])
        return attribute_set
    
    user_set = convert_attributes_to_set(user_attr)
    other_set = convert_attributes_to_set(other_attr)
    
    intersection = len(user_set & other_set)
    union = len(user_set | other_set)

    if union == 0:
        return 0
    
    return intersection / union

# Đo thời gian xử lý Jaccard Similarity
start_time = time.time()
similarity = compute_jaccard_similarity(users['user'], users['100022280481195'][0])
end_time = time.time()

print(f"Jaccard Similarity: {similarity}")
print(f"Thời gian xử lý Jaccard Similarity: {end_time - start_time} giây")

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

    correlation, _ = pearsonr(user_vector, other_vector)
    return correlation

# Đo thời gian xử lý Pearson Correlation
start_time = time.time()
similarity = compute_pearson_similarity(users['user'], users['100022280481195'][0])
end_time = time.time()

print(f"Pearson Correlation Coefficient: {similarity}")
print(f"Thời gian xử lý Pearson Correlation: {end_time - start_time} giây")

