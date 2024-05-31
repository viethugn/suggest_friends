# # Setting for plotting graph in the Jupyter Notebook

import matplotlib.pyplot as plt
import plotly.offline as py

# Set the size of the graph
plt.rcParams['figure.figsize'] = [10, 10]
from community import community_louvain
import community
import networkx as nx
import colorlover as cl
import numpy as np
import pickle
import copy 
import pandas as pd
import scipy as sp

# This is your Facebook id. It can also be a number
CENTRAL_ID = '100047415604756'

# This is the pickle file containing the raw graph data
GRAPH_FILENAME = 'friend_graph.pickle'

# Load the friend_graph picklefile
with open(GRAPH_FILENAME, 'rb') as f:
    friend_graph = pickle.load(f)

with open(GRAPH_FILENAME, 'rb') as f:
        for i, l in enumerate(f):
            pass
print('Total of ' + str(i+1) + ' friends.')   

# Only keep friends with at least 0 common friends
central_friends = {}
for k, v in friend_graph.items():
    # This contains the list number of mutual friends.
    # Doing len(v) does not work because instead of returning mutual
    # friends, Facebook returns all the person's friends
    intersection_size = len(np.intersect1d(list(friend_graph.keys()), v))
    # intersection_size = len(v)
    if intersection_size >= 1:
        central_friends[k] = v

print('Firtered out {} items'.format(len(friend_graph.keys()) - len(central_friends.keys())))
print(f'{len(central_friends)}')
# Extract edges from graph

edges = []
nodes = [CENTRAL_ID]
# print(f'{nodes}')

for k, v in central_friends.items():
    # edges.append((CENTRAL_ID, k))
    for item in v:
        if item in central_friends.keys():
            edges.append((k, item))

# print(f'{edges}')
G = nx.Graph()
# G.add_nodes_from([CENTRAL_ID])

G.add_nodes_from(central_friends.keys())

G.add_edges_from(edges)
# G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])
# --------------------------------------------------

# --------------------------------------------

print("G.number_of_edges(): ", G.number_of_edges())
print("G.number_of_nodes(): ", G.number_of_nodes())
print('Added {} edges'.format(len(edges) ))
print("Number of connected components: %d" % nx.number_connected_components(G))

# def compare_centrality(G):
#     degree_centrality = nx.degree_centrality(G)
#     closeness_centrality = nx.closeness_centrality(G)
#     betweenness_centrality = nx.betweenness_centrality(G)

#     plt.figure(figsize=(18, 6))

#     plt.subplot(131)
#     plt.hist(degree_centrality.values(), bins=25)
#     plt.title("Degree Centrality Histogram")
#     plt.xlabel("Degree Centrality")
#     plt.ylabel("Frequency")

#     plt.subplot(132)
#     plt.hist(closeness_centrality.values(), bins=25)
#     plt.title("Closeness Centrality Histogram")
#     plt.xlabel("Closeness Centrality")
#     plt.ylabel("Frequency")

#     plt.subplot(133)
#     plt.hist(betweenness_centrality.values(), bins=25)
#     plt.title("Betweenness Centrality Histogram")
#     plt.xlabel("Betweenness Centrality")
#     plt.ylabel("Frequency")

#     plt.show()

# compare_centrality(G)


#---------------------------------- Tính hệ số gom cụm của từng nút
# clustering_coefficients = nx.clustering(G)

# # Tạo một DataFrame từ dữ liệu hệ số gom cụm
# df = pd.DataFrame(list(clustering_coefficients.items()), columns=['Node', 'Clustering Coefficient'])

# # Xuất DataFrame ra tệp Excel
# df.to_excel('clustering_coefficients.xlsx', index=False)

# print("Kết quả đã được ghi vào tệp 'clustering_coefficients.xlsx'")

pos = nx.spring_layout(G) # get the position using the spring layout algorithm
# Calculate the number of direct friends for each node in the diagram
direct_friends = {node: G.degree(node) for node in G.nodes()}
# print(direct_friends)

# --------------------------------------------------------------------------Phát hiện cộng đồng

# part = community.best_partition(G)
# values = [part.get(node) for node in G.nodes()]
# # # In ra chỉ số gom cụm của từng đỉnh
# # for node, cluster in part.items():
# #     print(f"số node có links tới node {node}: ", G.degree(node))

# plt.rcParams['figure.figsize'] = [10, 10]
# nx.draw_networkx(G, pos = pos, 
#                  cmap = plt.get_cmap('jet'), node_color = values,
#                  node_size=50, width=0.5, edge_color='grey', with_labels=True, font_size=8)
# limits=plt.axis('off') 
# plt.show()
# End Phát hiện cộng đồng

# --------------------------------------------------------------------------Phát hiện cộng đồng 2

# louvain = community.best_partition(G)
# values = [louvain.get(node) for node in G.nodes()]

# plt.rcParams['figure.figsize'] = [10, 10]
# nx.draw_networkx(G, pos = pos, 
#                  cmap = plt.get_cmap('jet'), node_color = values,
#                  node_size=20, width=0.4, edge_color='grey', with_labels=False, font_size=8)
# limits=plt.axis('off') 

# print(max(louvain.values())-min(louvain.values())+1)
# plt.show()
# End Phát hiện cộng đồng


# -------------------------------------------------------------------Degree Centrality
# # # remove myself from the graph
# G_f = copy.deepcopy(G)
# G_f.remove_node(CENTRAL_ID)

# # keep the position
# pos_f = copy.deepcopy(pos)
# pos_f.pop(CENTRAL_ID, None)

# Degree centrality
# degree = nx.degree_centrality(G_f)
# values = [degree.get(node)*500 for node in G_f.nodes()]
# degree_centrality = nx.centrality.degree_centrality(G_f)
# print((sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True))[:8])
# print((sorted(G_f.degree, key=lambda item: item[1], reverse=True))[:8])
# print(degree_centrality.values())
# degree_centrality = nx.centrality.degree_centrality(G_f)
# plt.figure(figsize=(15, 8))
# plt.hist(degree_centrality.values(), bins=25)
# plt.xticks(ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])  # set the x axis ticks
# plt.title("Degree Centrality Histogram ", fontdict={"size": 35}, loc="center")
# plt.xlabel("Degree Centrality", fontdict={"size": 20})
# plt.ylabel("Counts", fontdict={"size": 20})


# nx.draw_networkx(G_f, pos =pos_f,
#                  cmap = plt.get_cmap('Accent'),
#                  node_color = values, node_size=values,
#                  width=0.2, edge_color='grey', with_labels=True)
# limits=plt.axis('off') # turn of axisb

# plt.show()
# -------------------------------------------------------------------End Degree Centrality


# --------------------------------------------------------------------Closeness Centrality
# G_f = copy.deepcopy(G)
# G_f.remove_node(CENTRAL_ID)

# pos_f = copy.deepcopy(pos)
# pos_f.pop(CENTRAL_ID, None)

# close = nx.closeness_centrality(G_f)
# values = [close.get(node) for node in G_f.nodes()]

# print (len(values))
# print (values)

# valuess = [close.get(node)*100 for node in G_f.nodes()]
# nx.draw_networkx(G_f, pos = pos_f,
#                  cmap = plt.get_cmap('Accent'),
#                  node_color = valuess, node_size=valuess,
#                  width=0.2, edge_color='grey', with_labels=True, font_size=7)

# limits=plt.axis('off')
# plt.show()
# closeness_centrality = nx.centrality.closeness_centrality(G_f)
# print((sorted(closeness_centrality.items(), key=lambda item: item[1], reverse=True))[:8])
# plt.figure(figsize=(15, 8))
# plt.hist(closeness_centrality.values(), bins=60)
# plt.title("Closeness Centrality Histogram ", fontdict={"size": 35}, loc="center")
# plt.xlabel("Closeness Centrality", fontdict={"size": 20})
# plt.ylabel("Counts", fontdict={"size": 20})

# plt.show()
# --------------------------------------------------------------------End Closeness Centrality

#-----------------------------------------------------------------------  Betweenness centrality
# G_f = copy.deepcopy(G)
# G_f.remove_node(CENTRAL_ID)

# pos_f = copy.deepcopy(pos)
# pos_f.pop(CENTRAL_ID, None)

# between = nx.betweenness_centrality(G_f)
# values = [between.get(node)*500 for node in G_f.nodes()]

# betweenness_centrality = nx.centrality.betweenness_centrality(G_f)
# print((sorted(betweenness_centrality.items(), key=lambda item: item[1], reverse=True))[:8])

# plt.figure(figsize=(15, 8))
# plt.hist(betweenness_centrality.values(), bins=100)
# # plt.xticks(ticks=[0, 0.02, 0.1, 0.2, 0.3, 0.4, 0.5])  # set the x axis ticks
# plt.title("Betweenness Centrality Histogram ", fontdict={"size": 35}, loc="center")
# plt.xlabel("Betweenness Centrality", fontdict={"size": 20})
# plt.ylabel("Counts", fontdict={"size": 20})
# nx.draw_networkx(G_f, pos = pos_f,
#                  cmap = plt.get_cmap('jet'),
#                  node_color = values, node_size=values,
#                  width=0.2, edge_color='grey', with_labels=True, font_size=7)

# limits=plt.axis('off') # turn of axisb

# plt.show()


# ------------------------------------------------------------------------------------

#-----------------------------------------------------------------------  page rank
# G_f = copy.deepcopy(G)
# G_f.remove_node(CENTRAL_ID)

# pos_f = copy.deepcopy(pos)
# pos_f.pop(CENTRAL_ID, None)
# G = nx.complete_graph(5)
# preds = nx.jaccard_coefficient(G, G.edges())
# for u, v, p in preds:
#     print(f"({u}, {v}) -> {p:.8f}")
# def recommend_friends_common_neighbors(G, user, k=5):
#     neighbors = set(G.neighbors(user))
#     scores = {}
#     for other in G.nodes():
#         if other != user and other not in neighbors:
#             common_neighbors = len(neighbors & set(G.neighbors(other)))
#             scores[other] = common_neighbors
#     sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     return sorted_scores[:k]

# recommendations = recommend_friends_common_neighbors(G, 100014448523676)
# print(recommendations)