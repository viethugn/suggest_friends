
import facebook
import requests

def total_count_facebook_friends(access_token):
    graph = facebook.GraphAPI(access_token)
    friends = graph.get_connections("me", "friends")
    return friends['summary']['total_count']

def get_all_facebook_friends(access_token):
    graph = facebook.GraphAPI(access_token)
    friend_list = []
    friends = graph.get_connections("me", "friends")
    friend_list.extend(friends['data'])

    # Phân trang để lấy toàn bộ danh sách bạn bè
    try:
        while 'next' in friends['paging']:
            friends = graph.get_connections("me", "friends", after=friends['paging']['cursors']['after'])
            friend_list.extend(friends['data'])
    except KeyError:
        pass

    return friend_list

# Thay access_token bằng access token của bạn
access_token = "EAABwzLixnjYBOZCBGHZAKjVxayl6MlALIIiy4z3OIlfbZATWGmAStn4XsIMz1ZCOiWHozfQnhkI2m2qxab8VRTKy8PxZCvslchqTthytlkZCyaIEZC7zMjYZBcU9QOpcuQ5SuWVov2HHKL6ODK1XkzKtxKwtLy7IqvQDZA8bwfEUo9HmX2QvqYg9xZBj3FekMGbZA4UjBUZD"
num_friends = total_count_facebook_friends(access_token)
print(f"Số lượng bạn bè của bạn: {num_friends}")

all_friends = get_all_facebook_friends(access_token)
friend_count = len(all_friends)
print(f"Bạn bè của bạn: {friend_count}")



# import requests
# import networkx as nx
# import matplotlib.pyplot as plt
# import itertools

# def analyze_facebook_friends(access_token):
#     # Tạo đồ thị
#     G = nx.Graph()

#     # Lấy danh sách bạn bè từ Graph API
#     url = f"https://graph.facebook.com/me/friends?access_token={access_token}"
#     response = requests.get(url)
#     data = response.json()

#     # Thêm các cạnh vào đồ thị
#     if 'data' in data:
#         for friend in data['data']:
#             G.add_edge('me', friend['id'])

#     # Tính chỉ số gom cụm
#     clustering_coefficient = nx.average_clustering(G)

#     # Vẽ đồ thị (tuỳ chọn)
#     nx.draw(G, with_labels=True)
#     plt.show()

#     return clustering_coefficient

# # Thay access_token bằng access token của bạn
# access_token = "EAABwzLixnjYBOymUhw6OZBZB0CfWLe6apL6oZC96pJBJw36V19z7bKuwZBitowvUCYo8oZBPiTKIoBJCVWBGTWqOu3HYhEahpuN2FowVMIcnMCbdmzwHNmBZBWJ4UZCZABbr9CY2TDe6ZAUHp0Bp6bis59ZCsDOJprV72DkAWBvDmqWsagXY5qwxZCxHIwS4Ou07HiBvNcZD"

# # Phân tích mối quan hệ bạn bè và tính chỉ số gom cụm
# clustering_coefficient = analyze_facebook_friends(access_token)
# print("Chỉ số gom cụm:", clustering_coefficient)



