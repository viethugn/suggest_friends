import tkinter as tk
import requests
import networkx as nx
import matplotlib.pyplot as plt

def get_facebook_friends(access_token):
    url = f"https://graph.facebook.com/me/friends?access_token={access_token}"
    response = requests.get(url)
    data = response.json()
    return data
    # if 'data' in data:
    #     friend_count = len(data['data'])
    #     return friend_count
    # else:
    #     print("Không thể lấy danh sách bạn bè.")
    #     return None

def calculate_metrics():
    # Dữ liệu mẫu về mối quan hệ bạn bè
    access_token = "EAABwzLixnjYBOZCBGHZAKjVxayl6MlALIIiy4z3OIlfbZATWGmAStn4XsIMz1ZCOiWHozfQnhkI2m2qxab8VRTKy8PxZCvslchqTthytlkZCyaIEZC7zMjYZBcU9QOpcuQ5SuWVov2HHKL6ODK1XkzKtxKwtLy7IqvQDZA8bwfEUo9HmX2QvqYg9xZBj3FekMGbZA4UjBUZD"
    relationships = get_facebook_friends(access_token)


    # Tạo đồ thị từ dữ liệu mối quan hệ
    G = nx.Graph()
    for person, friends in relationships.items():
        for friend in friends:
            G.add_edge(person, friend)

    # Tính toán các chỉ số
    num_friends = {person: len(friends) for person, friends in relationships.items()}
    num_connections = {person: G.degree(person) for person in G.nodes()}
    clustering_coefficients = nx.clustering(G)

    # Hiển thị kết quả trong giao diện
    result_text.delete('1.0', tk.END)  # Xóa kết quả trước đó
    result_text.insert(tk.END, "Số lượng bạn bè của từng người:\n")
    for person, num in num_friends.items():
        result_text.insert(tk.END, f"{person}: {num}\n")

    result_text.insert(tk.END, "\nSố lượng kết nối của từng người:\n")
    for person, num in num_connections.items():
        result_text.insert(tk.END, f"{person}: {num}\n")

    result_text.insert(tk.END, "\nChỉ số gom cụm của từng người:\n")
    for person, coefficient in clustering_coefficients.items():
        result_text.insert(tk.END, f"{person}: {coefficient}\n")

# Tạo cửa sổ chính của ứng dụng
root = tk.Tk()
root.title("Ứng dụng tính chỉ số mạng xã hội")

# Tạo nút để tính toán chỉ số
calculate_button = tk.Button(root, text="Tính toán chỉ số", command=calculate_metrics)
calculate_button.pack(pady=10)

# Tạo một ô văn bản để hiển thị kết quả
result_text = tk.Text(root, height=20, width=50)
result_text.pack()

# Bắt đầu vòng lặp chờ sự kiện
root.mainloop()
