import tkinter as tk
from tkinter import ttk
from info_user import *
from ghi_du_lieu_ban_be import *
from tinh_trong_so import *
from goi_y_ket_ban.goi_y_kb  import *
import webbrowser

# EAABwzLixnjYBO02lyFEy24GT6evLkIL1dKMunmjltbTkpYcWaS9Gv4hZAgQpn3XzJMlp5Cu3p6BiMBBfB7wJnsZApOYasMsttm3mO8bNmk9ZCToxaO5KGzliotP0GKRtdcsqSxU8oPMVSndAHvEBAcHcOUYeGDycnHHVpsuZCfnSa111TZAtAwZCq1H8jSATSuST0ZD

def run():
    get_info_user(access_token.get())
    get_info_friends_user(access_token.get())
    get_friends_of_friends(access_token.get())
    show()
def disable_buttons():
    button_run.config(state="disabled")
    button_quit.config(state="disabled")
    entry_access_token.config(state="disabled")

def open_link(link):
    webbrowser.open_new_tab(link)


def show():
    suggest_friend = goi_y_kb()
    # Tắt các nút và ô nhập liệu
    disable_buttons()
    
    # Xóa bảng nếu nó đã tồn tại
    for child in entry_frame.winfo_children():
        child.destroy()

    tree = ttk.Treeview(entry_frame)
    # Tạo Treeview
    # tree["columns"] = ("ID", "Link", "Name", "Birthday", "Location", "Hometown", "Work", "Trọng Số", "Tỉ lệ của giữa phần giao", "-	Hệ số tương quan Pearson")
    tree["columns"] = ("ID", "Link", "Name", "Thuộc tính chung", "Tỉ lệ của giữa phần giao", "-	Hệ số tương quan Pearson")
    tree.heading("#0", text="STT")
    tree.heading("ID", text="ID")
    tree.heading("Link", text="Link")
    tree.heading("Name", text="Name")
    # tree.heading("Birthday", text="Birthday")
    # tree.heading("Location", text="Location")
    # tree.heading("Hometown", text="Hometown")
    # tree.heading("Work", text="Work")
    tree.heading("Thuộc tính chung", text="Thuộc tính chung")
    tree.heading("Tỉ lệ của giữa phần giao", text="Tỉ lệ của giữa phần giao")
    tree.heading("-	Hệ số tương quan Pearson", text="-	Hệ số tương quan Pearson")
    
    # Thêm dữ liệu vào Treeview
    i = 1
    for key, values in suggest_friend.items():

        for value in values:
            jaccard_similarity = value['jaccard_similarity']
            pearson_similarity = value['pearson_similarity']
            birthday_value = value['conditions_met'].get('birthday', None)
            location_value = value['conditions_met'].get('location', None)
            hometown_value = value['conditions_met'].get('hometown', None)
            work_value = value['conditions_met'].get('work', None)
            # tree.insert("", tk.END, text=str(i), values=(key, value['link'], value['name'], birthday_value, location_value, hometown_value, work_value, value['weight'], jaccard_similarity, pearson_similarity))
            tree.insert("", tk.END, text=str(i), values=(key, value['link'], value['name'], value['weight'], jaccard_similarity, pearson_similarity))
            i += 1 
    def on_row_click(event):
      # Kiểm tra xem có dòng nào được chọn không
      selected_items = tree.selection()
      if selected_items:
          item = selected_items[0]
          # Tiếp tục xử lý dữ liệu
          link = tree.item(item, "values")[1]
          open_link(link)
      else:
          print("Không có dòng được chọn")
    # Bắt sự kiện double-click vào từng dòng
    tree.bind("<Double-1>", on_row_click)

    # Hiển thị Treeview
    tree.pack(fill="both", expand=True)
    button_run.config(state="normal")
    button_quit.config(state="normal")
    entry_access_token.config(state="normal")


root = tk.Tk()

#Var
access_token = tk.StringVar()

root.title('Facebook Graph')
root.minsize(height=800, width=800)

# Nhãn
tk.Label(root, text='Những người bạn có thể biết', fg='red', font=('cambria', 25)).grid(row=0)

# Khung chứa Entry và nút
entry_frame = tk.Frame(root)

label_access_token = tk.Label(root, text='Nhập Access Token:', font=('cambria', 16))
label_access_token.grid(row=1, column=0)

entry_access_token = tk.Entry(root, width=100, textvariable=access_token)
entry_access_token.grid(row=1, column=1)

button_run = tk.Button(root, text='Chạy', command=run)
button_run.grid(row=1, column=2, padx=5)

button_quit = tk.Button(root, text='Thoát', command=root.quit)
button_quit.grid(row=1, column=3, padx=5) 

button_run.config(state="normal")
button_quit.config(state="normal")
entry_frame.grid(row=5, column=0, columnspan=3)

root.mainloop()
