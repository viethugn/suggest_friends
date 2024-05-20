import facebook
import networkx as nx

def get_clustering_coefficient(access_token):
    graph = facebook.GraphAPI(access_token)
    friends = graph.get_object("me/friends")
    friend_ids = [friend['id'] for friend in friends['data']]
    
    G = nx.Graph()
    for friend_id in friend_ids:
        friend_friends = graph.get_object(f"{friend_id}/friends")
        friend_friend_ids = [friend['id'] for friend in friend_friends['data']]
        for friend_friend_id in friend_friend_ids:
            if friend_friend_id in friend_ids:
                G.add_edge(friend_id, friend_friend_id)
    
    clustering_coefficients = nx.clustering(G)
    
    return clustering_coefficients

def main():
    access_token = 'EAABwzLixnjYBOZCBGHZAKjVxayl6MlALIIiy4z3OIlfbZATWGmAStn4XsIMz1ZCOiWHozfQnhkI2m2qxab8VRTKy8PxZCvslchqTthytlkZCyaIEZC7zMjYZBcU9QOpcuQ5SuWVov2HHKL6ODK1XkzKtxKwtLy7IqvQDZA8bwfEUo9HmX2QvqYg9xZBj3FekMGbZA4UjBUZD'
    clustering_coefficients = get_clustering_coefficient(access_token)
    print("Chỉ số gom cụm của từng người bạn:")
    for node, clustering_coefficient in clustering_coefficients.items():
        print(f"{node}: {clustering_coefficient}")

if __name__ == "__main__":
    main()
