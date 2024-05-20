from html.parser import HTMLParser
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from tqdm import tqdm
import pickle
import getpass
import json
import requests

def get_fb_page(url):
    time.sleep(5)
    driver.get(url)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
        
    # html_source = driver.page_source
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]')
    html_source = element.get_attribute('outerHTML')
    return html_source

def find_friend_from_url(url):
    if re.search('.com\/profile.php\?id=\d+\&', url) is not None:
        m = re.search(r'profile\.php\?id=\d+', url)
        friend = m.group(0)
    else:
        # m = re.search('com\/(.*)\?', url)
        m = re.search('.com\/(.*)', url)
        friend = m.group(1)
    return friend


class MyHTMLParser(HTMLParser):
    urls = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, print it.
                if name == "href":
                    if re.search('com/(.*)', value) is not None:
                        self.urls.append(value)
                    # if re.search('\?href|&href|hc_loca|\?fref', value) is not None:
                    #     if re.search('.com/profile.php', value):
                    #         self.urls.append(value)

file_path = './json_api.json'
# Đọc dữ liệu từ tệp JSON
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)
# friend_list = [friend.get('link') for friend in json_data.get('data', [])]
friend_list={}
for friend in json_data.get('data', []):
    # Lấy ra 'id' của bạn bè
    friend_id = friend.get('id')
    # Tạo một khóa mới với giá trị là một từ điển rỗng
    friend_list[friend_id] = {
      'id' : friend_id,
      'link' : friend.get('link'),
      'location' : friend.get('location'),
      'hometown' : friend.get('hometown'),
      'birthday' : friend.get('birthday'),
    }

# print(f"list: {len(friend_list)}")
# print(friend_list)

username = input("Facebook username:") or 'viethung0500@gmail.com'
password = getpass.getpass('Password:') or 'mk:0794574218aA.'

chrome_options = webdriver.ChromeOptions()
options = Options()

driver = webdriver.Chrome(options=options)
driver.get('http://www.facebook.com/') 

# authenticate to facebook account
elem = driver.find_element("id", "email")
elem.send_keys(username)
elem = driver.find_element("id", "pass")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
time.sleep(5)

print("Successfully logged in Facebook!")

SCROLL_PAUSE_TIME = 2

# my_url = 'https://www.facebook.com/friends/list'

UNIQ_FILENAME = 'uniq_urls.pickle'
if os.path.isfile(UNIQ_FILENAME):
    with open(UNIQ_FILENAME, 'rb') as f:
        uniq_urls = pickle.load(f)
    print('We loaded {} uniq friends'.format(len(uniq_urls)))
else:
    uniq_urls = friend_list
    print('We found {} friends, saving it'.format(len(uniq_urls)))
    with open(UNIQ_FILENAME, 'wb') as f:
        pickle.dump(uniq_urls, f)

friend_graph = {}
GRAPH_FILENAME = 'friend_graph.pickle'

if os.path.isfile(GRAPH_FILENAME):
    with open(GRAPH_FILENAME, 'rb') as f:
        friend_graph = pickle.load(f)
    print('Loaded existing graph, found {} keys'.format(len(friend_graph.keys())))
    print(len(friend_graph.keys()))

count = 0
# print(uniq_urls)
for item in tqdm(uniq_urls.items()):
    key, value = item
    url = value.get('link')
    id = value.get('id')
    # print(f"url: {url}")
    count += 1

    if count % 100 == 0:
        print ("Too many queries, pause for a while...")
        time.sleep(1800)

    friend_username = find_friend_from_url(url)

    # if (friend_username in friend_graph.keys()) and (len(friend_graph[friend_username]) > 1):
    #     continue
    
    print(f"test: {friend_username}; url: {url}; id: {id}")
    friend_graph[id] = []
    print(f"test2: {friend_graph[id]}; url: {url}; id: {id}")

    if friend_username.find("profile.php?id=") != -1:
        # Chuỗi chứa "profile.php?id="
        mutual_url = 'https://www.facebook.com/{}&sk=friends_mutual'.format(friend_username)
    else:
      # Chuỗi không chứa "profile.php?id="
      mutual_url = 'https://www.facebook.com/{}/friends_mutual'.format(friend_username)

    # mutual_url = 'https://www.facebook.com/{}/friends_mutual'.format(friend_username)
    mutual_page = get_fb_page(mutual_url)

    parser = MyHTMLParser()
    parser.urls = []
    parser.feed(mutual_page)
    mutual_friends_urls = set(parser.urls)

    urls_without_mutual_friends = mutual_friends_urls.copy()  # Creates a copy of the original collection
    for url in mutual_friends_urls:
        if 'friends_mutual' in url:
            urls_without_mutual_friends.remove(url)

    print('Found {} urls'.format(len(urls_without_mutual_friends)))
    print(list(urls_without_mutual_friends))
    # print(mutual_friends_urls)
    # if count == 1:
    #   break
    
    for mutual_url in urls_without_mutual_friends:
      for key, value in uniq_urls.items():
        if value.get('link') and mutual_url in value.get('link'):
          print(key)
          friend_graph[id].append(key)

    with open(GRAPH_FILENAME, 'wb') as f:
        pickle.dump(friend_graph, f)

    time.sleep(3)