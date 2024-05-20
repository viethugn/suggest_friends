import pickle
import pandas as pd
GRAPH_FILENAME = 'friend_graph.pickle'

# Load the friend_graph picklefile
with open(GRAPH_FILENAME, 'rb') as f:
    friend_graph = pickle.load(f)

# Chuyển đổi friend_graph thành DataFrame
df = pd.DataFrame(friend_graph.items(), columns=['User', 'Friends'])

# Ghi DataFrame vào file Excel
excel_file = 'friend_mutual_graph.xlsx'
df.to_excel(excel_file, index=False)
print(friend_graph)