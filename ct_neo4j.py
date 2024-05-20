from neo4j import GraphDatabase
import csv

# Kết nối đến cơ sở dữ liệu Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Đọc tệp CSV và lấy danh sách tên
names = []
with open('excel_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        names.append(row[0])

# Tạo mối quan hệ bạn bè trong Neo4j
with driver.session() as session:
    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names):
            if i < j:
                session.run(
                    "MATCH (p1:Person {name: $name1}), (p2:Person {name: $name2}) "
                    "CREATE (p1)-[:Friend]->(p2), (p2)-[:Friend]->(p1)",
                    name1=name1,
                    name2=name2
                )