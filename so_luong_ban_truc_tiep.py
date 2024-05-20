import facebook

def get_direct_friends(access_token):
    graph = facebook.GraphAPI(access_token)
    my_friends = graph.get_object("me/friends")
    my_friend_ids = [friend['id'] for friend in my_friends['data']]
    
    direct_friends = []
    for friend_id in my_friend_ids:
        friend_friends = graph.get_object(f"{friend_id}/friends")
        friend_friend_ids = [friend['id'] for friend in friend_friends['data']]
        for friend_friend_id in friend_friend_ids:
            if friend_friend_id in my_friend_ids:
                direct_friends.append(friend_friend_id)
    
    return len(set(direct_friends))


# Thay access_token bằng access token của bạn
access_token = 'EAABwzLixnjYBOZCBGHZAKjVxayl6MlALIIiy4z3OIlfbZATWGmAStn4XsIMz1ZCOiWHozfQnhkI2m2qxab8VRTKy8PxZCvslchqTthytlkZCyaIEZC7zMjYZBcU9QOpcuQ5SuWVov2HHKL6ODK1XkzKtxKwtLy7IqvQDZA8bwfEUo9HmX2QvqYg9xZBj3FekMGbZA4UjBUZD'
direct_friends_count = get_direct_friends(access_token)
print("Số lượng bạn trực tiếp trên Facebook của bạn là:", direct_friends_count)

