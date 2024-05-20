import requests
import json
import random
import matplotlib.pyplot as plt
import concurrent.futures
# Set the size of the graph
plt.rcParams['figure.figsize'] = [10, 10]
import os
import networkx as nx
import numpy as np
import pickle
import copy 

def get_friends_of_friends(token):
  def get_friends_of_friend(arr_user_id, file_name, access_token_of_user):
      arr_data_lists = {}

      # Định nghĩa một hàm con để lấy dữ liệu từ API cho một người dùng cụ thể
      def fetch_user_friends(user_id):
          url = f"https://graph.facebook.com/{user_id}/friends"
          params = {
              'fields': 'id,link,name,gender,birthday,hometown,location,work',
              'access_token': access_token_of_user
          }
          response = requests.get(url, params=params)
          json_data = response.json()
          data_list = json_data.get('data', [])
          if data_list:
              arr_data_lists[user_id] = data_list

      # Sử dụng ThreadPoolExecutor để thực hiện các yêu cầu API đồng thời
      with concurrent.futures.ThreadPoolExecutor() as executor:
          # Gọi fetch_user_friends cho mỗi user_id trong arr_user_id và đợi kết quả trả về
          executor.map(fetch_user_friends, arr_user_id)

      # Mở tệp tin để ghi dữ liệu JSON vào
      with open(file_name, "w") as file:
          json.dump(arr_data_lists, file, indent=4)



  access_token = token
  directory = "goi_y_ket_ban"
  file_name = "json_api_get_friends.json"
  file_name_get_friends = os.path.join(directory, file_name)

  # This is your Facebook id. It can also be a number
  CENTRAL_ID = 'me'
  GRAPH_FILENAME = 'friend_graph.pickle'

  # Load the friend_graph picklefile
  with open(GRAPH_FILENAME, 'rb') as f:
      friend_graph = pickle.load(f)
  # print(friend_graph)
  # Only keep friends with at least 0 common friends
  central_friends = {}
  for k, v in friend_graph.items():
      # This contains the list number of mutual friends.
      # Doing len(v) does not work because instead of returning mutual
      # friends, Facebook returns all the person's friends
      intersection_size = len(np.intersect1d(list(friend_graph.keys()), v))
      if intersection_size >= 1:
          central_friends[k] = v

  edges = []

  nodes = [CENTRAL_ID]

  #chuyển đối tượng thành danh sách cạnh
  for k, v in central_friends.items():
      # edges.append((CENTRAL_ID, k))
      for item in v:
          if item in central_friends.keys() or item == CENTRAL_ID:
              edges.append((k, item))

  G = nx.Graph()
  G.add_nodes_from([CENTRAL_ID])

  G.add_nodes_from(central_friends.keys())

  G.add_edges_from(edges)

  pos = nx.spring_layout(G) # get the position using the spring layout algorithm

  G_f = copy.deepcopy(G)
  G_f.remove_node(CENTRAL_ID)

  pos_f = copy.deepcopy(pos)
  pos_f.pop(CENTRAL_ID, None)

  close = nx.closeness_centrality(G_f)
  # values = [close.get(node) for node in G_f.nodes()]
  high_closeness_nodes = [node for node, closeness in close.items() if closeness > 0.5]

  list_id = []
  for id in high_closeness_nodes:
      with open('uniq_urls.pickle', 'rb') as f:
        uniq_urls = pickle.load(f)
      for item in uniq_urls.items():
        key, value = item
        url = value.get('link')
        id2 = value.get('id')
        if id == id2:
          # print(url)
          list_id.append(id)
          # list_id[id2] = [{
          #    'link': url,
          # }]
  get_friends_of_friend(list_id,file_name_get_friends,access_token)
get_friends_of_friends('EAABwzLixnjYBO02lyFEy24GT6evLkIL1dKMunmjltbTkpYcWaS9Gv4hZAgQpn3XzJMlp5Cu3p6BiMBBfB7wJnsZApOYasMsttm3mO8bNmk9ZCToxaO5KGzliotP0GKRtdcsqSxU8oPMVSndAHvEBAcHcOUYeGDycnHHVpsuZCfnSa111TZAtAwZCq1H8jSATSuST0ZD')
