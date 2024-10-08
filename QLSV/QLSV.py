from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ Thống Quản Lý Sinh Viên")
#root.state('zoomed')


root.geometry("1400x800")
# # Kết nối tới db
conn = sqlite3.connect('QLSV.db')
c = conn.cursor()

# # Tao bang de luu tru
c.execute('''
    CREATE TABLE addresses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mssv text,
        first_name text,
        last_name text,
        class_id text,
        yearEnroll text,
        average interger

    )
'''
)

def them():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    # Lấy dữ liệu đã nhập
    mssv_value = mssv.get()
    firstname_value = f_name.get()
    lastName_value = l_name.get()
    class_value = class_id.get()
    yearEnroll_value = yearEnroll.get()
    average_value = average.get()
    # Thực hiện câu lệnh để thêm
    c.execute('''
        INSERT INTO 
        addresses (mssv, first_name, last_name, class_id, yearEnroll, average)
        VALUES 
        (:mssv, :first_name, :last_name, :class_id,:yearEnroll, :average)
    ''', {
        'mssv': mssv_value,
        'first_name': firstname_value,
        'last_name': lastName_value,
        'class_id': class_value,
        'yearEnroll': yearEnroll_value,
        'average': average_value,

    }
              )
    conn.commit()
    conn.close()

    # Reset form
    mssv.delete(0, END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    class_id.delete(0, END)
    yearEnroll.delete(0, END)
    average.delete(0, END)

    # Hien thi lai du lieu
    truy_van()


def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    c.execute('''DELETE FROM
                        addresses 
                      WHERE id=:id''',
              {'id': delete_box.get()})
    delete_box.delete(0, END)
    conn.commit()
    conn.close()
    # Hiên thi thong bao
    messagebox.showinfo("Thông báo", "Đã xóa!")
    # Hiển thị lại dữ liệu
    truy_van()


def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    c.execute("SELECT * FROM addresses")
    records = c.fetchall()

    # Hien thi du lieu
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

    # Ngat ket noi
    conn.close()


def cap_nhat():
    global record_id
    # Kiểm tra nếu ID bị thay đổi
    if f_id_editor.get() != record_id:
        messagebox.showerror("Lỗi", "Không được phép sửa ID")
        return
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    record_id = f_id_editor.get()

    c.execute("""UPDATE addresses bb SET
           mssv =:mssv,
    first_name = :first,
               last_name = :last,
               class_id = :class_id,
               yearEnroll = :yearEnroll,
               average = :average
               WHERE id = :id""",
              {
                  'mssv': f_mssv_editor.get(),
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'class_id': class_id_editor.get(),
                  'yearEnroll': yearEnroll_editor.get(),
                  'average': average_editor.get(),
                  'id': record_id
              })

    conn.commit()
    conn.close()
    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Sửa thành công")
    editor.destroy()

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()


def chinh_sua():
    global editor, record_id
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("800x600")

    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    global f_id_editor, f_mssv_editor, f_name_editor, l_name_editor, class_id_editor, yearEnroll_editor, average_editor

    f_id_editor = Entry(editor, width=30)
    f_id_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    f_mssv_editor = Entry(editor, width=30)
    f_mssv_editor.grid(row=1, column=1, padx=20)
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=2, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=3, column=1)
    class_id_editor = Entry(editor, width=30)
    class_id_editor.grid(row=4, column=1)
    yearEnroll_editor = Entry(editor, width=30)
    yearEnroll_editor.grid(row=5, column=1)
    average_editor = Entry(editor, width=30)
    average_editor.grid(row=6, column=1)

    f_id_label = Label(editor, text="ID")
    f_id_label.grid(row=0, column=0, pady=(10, 0))
    f_mssv_label = Label(editor, text="MSSV")
    f_mssv_label.grid(row=1, column=0)
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=2, column=0)
    l_name_label = Label(editor, text="Tên")
    l_name_label.grid(row=3, column=0)
    class_id_label = Label(editor, text="Mã Lớp")
    class_id_label.grid(row=4, column=0)
    yearEnroll_label = Label(editor, text="Năm Nhập Học")
    yearEnroll_label.grid(row=5, column=0)
    average_label = Label(editor, text="Điểm Trung Bình")
    average_label.grid(row=6, column=0)

    for record in records:
        f_id_editor.insert(0, record[0])
        f_mssv_editor.insert(0, record[1])
        f_name_editor.insert(0, record[2])
        l_name_editor.insert(0, record[3])
        class_id_editor.insert(0, record[4])
        yearEnroll_editor.insert(0, record[5])
        average_editor.insert(0, record[6])
    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


# def cap_nhat():
#     # Kiểm tra nếu ID bị thay đổi
#     if f_id_editor.get() != record_id:
#         messagebox.showerror("Lỗi", "Không được phép sửa ID")
#         return
#     conn = sqlite3.connect('QLSV.db')
#     c = conn.cursor()
#     record_id = f_id_editor.get()

#     c.execute("""UPDATE addresses SET
#            mssv =:mssv,
#            first_name = :first,
#            last_name = :last,
#            class_id = :class_id,
#            yearEnroll = :yearEnroll,
#            average = :average
#            WHERE id = :id""",
#               {
#                   'mssv': f_mssv_editor.get(),
#                   'first': f_name_editor.get(),
#                   'last': l_name_editor.get(),
#                   'class_id': class_id_editor.get(),
#                   'yearEnroll': yearEnroll_editor.get(),
#                   'average': average_editor.get(),
#                   'id': record_id
#               })

#     conn.commit()
#     conn.close()

#     editor.destroy()

#     # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
#     truy_van()

def chon(event):
    # Lấy thông tin bản ghi được chọn
    ID_object = tree.focus()  # lấy ID của hàng (đây là ID của hệ thống không phải ID của mình)
    ID_value = tree.item(ID_object,
                         'values')  # lấy tất cả giá trị của hàng dựa vào ID của hàng gồm: ID của mình, Họ , Tên, TP

    # Cập nhật ID của bản ghi vào delete_box
    if ID_value:
        delete_box.delete(0, END)  # tạo lại form
        delete_box.insert(0, ID_value[0])  # ID nằm ở đầu vì mình thiết kế vậy chứ không có bắt buộc


# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho cửa sổ chính
mssv = Entry(input_frame, width=30)
mssv.grid(row=0, column=1, padx=20, pady=(10, 0))
f_name = Entry(input_frame, width=30)
f_name.grid(row=1, column=1)
l_name = Entry(input_frame, width=30)
l_name.grid(row=2, column=1)
class_id = Entry(input_frame, width=30)
class_id.grid(row=3, column=1)
yearEnroll = Entry(input_frame, width=30)
yearEnroll.grid(row=4, column=1)
average = Entry(input_frame, width=30)
average.grid(row=5, column=1)

# Các nhãn
mssv_label = Label(input_frame, text="MSSV")
mssv_label.grid(row=0, column=0, pady=(10, 0))
f_name_label = Label(input_frame, text="Họ")
f_name_label.grid(row=1, column=0, pady=(10, 0))
l_name_label = Label(input_frame, text="Tên")
l_name_label.grid(row=2, column=0)
class_id_label = Label(input_frame, text="Mã Lớp")
class_id_label.grid(row=3, column=0)
yearEnroll_label = Label(input_frame, text="Năm Nhập Học")
yearEnroll_label.grid(row=4, column=0)
average_label = Label(input_frame, text="Điểm Trung Bình")
average_label.grid(row=5, column=0)
# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn ID")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("ID","MSSV", "Họ", "Tên", "Mã Lớp", "Năm Nhập Học", "Điểm Trung Bình")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER) # This will center text in rows
    tree.heading(column, text=column)
tree.pack()
# Gọi hàm này khi người dùng chọn bản ghi trong Treeview
tree.bind("<<TreeviewSelect>>", chon)
# Định nghĩa tiêu đề cho các cột
for col in columns:
    tree.heading(col, text=col)

# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()