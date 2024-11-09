pip install requests matplotlib

pip install pyperclip

import tkinter as tk
from tkinter import messagebox
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyperclip  # برای دسترسی به کلیپ‌بورد
from matplotlib.ticker import MaxNLocator  # برای تنظیم مرتب مقادیر محور Y

# URL فایل JSON
file_url = "https://raw.githubusercontent.com/saberafshar93/JIF/refs/heads/main/Total.json"

# دانلود داده‌ها از URL
def load_data():
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Error", "Failed to load data.")
            return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

# جستجو بر اساس پست
def search_post():
    post = entry_post.get().strip()
    if not post:
        messagebox.showwarning("Input Error", "Please enter a post.")
        return
    
    data = load_data()
    
    if not data:
        return
    
    # جستجو در داده‌ها
    result = None
    for item in data:
        if item['ISSN'].lower() == post.lower() or item['EiSSN'].lower() == post.lower():
            result = item
            break
    
    if result:
        display_results(result)
        plot_chart(result)
    else:
        messagebox.showinfo("No Results", "No data found for the entered post.")

# نمایش نتایج در جدول
def display_results(item):
    result_frame.pack_forget()  # پاک کردن نتایج قبلی
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    table = tk.Text(result_frame, wrap=tk.WORD, height=15, width=80)  # بزرگتر کردن جدول
    table.insert(tk.END, f"ISSN: {item.get('ISSN', 'Not Available')}\n")
    table.insert(tk.END, f"EiSSN: {item.get('EiSSN', 'Not Available')}\n")
    table.insert(tk.END, f"Journal Name: {item.get('Journalname', 'Not Available')}\n")
    table.insert(tk.END, f"Category: {item.get('Category', 'Not Available')}\n")
    table.insert(tk.END, f"Total Citations 2023: {item.get('TotalCitations', 'Not Available')}\n")
    table.insert(tk.END, f"JIF 2023 (Impact Factor): {item.get('JIF 2023', 'Not Available')}\n")
    table.insert(tk.END, f"JIF Quartile 2023: {item.get('JIFQuartile', 'Not Available')}\n")
    table.insert(tk.END, f"JCI 2023: {item.get('JCI 2023', 'Not Available')}\n")
    table.insert(tk.END, f"% of OA Gold 2023: {item.get('% of OA Gold', 'Not Available')}\n")
    
    # اضافه کردن JIF های سال‌های 2020 تا 2022
    table.insert(tk.END, f"JIF 2022: {item.get('Column_10', 'Not Available')}\n")
    table.insert(tk.END, f"JIF 2021: {item.get('Column_11', 'Not Available')}\n")
    table.insert(tk.END, f"JIF 2020: {item.get('Column_12', 'Not Available')}\n")
    
    table.pack()

# رسم نمودار JIF به صورت میله‌ای
def plot_chart(item):
    # داده‌های JIF از سال 2020 تا 2023
    jif_data = [
        {'year': 2020, 'jif': item.get('Column_12', None)},  # JIF 2020
        {'year': 2021, 'jif': item.get('Column_11', None)},  # JIF 2021
        {'year': 2022, 'jif': item.get('Column_10', None)},  # JIF 2022
        {'year': 2023, 'jif': item.get('JIF 2023', None)}    # JIF 2023
    ]
    
    # فیلتر کردن داده‌ها برای حذف None و مرتب‌سازی بر اساس سال
    jif_data = [data for data in jif_data if data['jif'] is not None]
    jif_data.sort(key=lambda x: x['year'])  # مرتب‌سازی بر اساس سال

    # استخراج مقادیر برای رسم نمودار
    years = [str(data['year']) for data in jif_data]
    jif_values = [data['jif'] for data in jif_data]
    
    if not jif_values:
        return
    
    # رسم نمودار میله‌ای
    fig, ax = plt.subplots(figsize=(6, 5))  # افزایش اندازه نمودار
    ax.bar(years, jif_values, color='skyblue', edgecolor='blue', label='JIF (Impact Factor)', zorder=5)  # استفاده از bar برای نمودار میله‌ای
    
    # اضافه کردن برچسب‌های محور X و Y
    ax.set_xlabel('Years')
    ax.set_ylabel('Impact Factor')
    ax.set_title('Impact Factor over Years')
    
    # تنظیم ترتیب مقادیر محور Y
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # اطمینان از اینکه مقادیر محور Y به صورت صحیح و شمارشی باشند
    
    # نمایش نمودار در Tkinter
    chart_canvas = FigureCanvasTkAgg(fig, master=result_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack()

# تابع برای قرار دادن متن از کلیپ‌بورد در ورودی
def paste_text():
    post_from_clipboard = pyperclip.paste()  # گرفتن محتویات کلیپ‌بورد
    entry_post.delete(0, tk.END)  # پاک کردن ورودی فعلی
    entry_post.insert(tk.END, post_from_clipboard)  # قرار دادن متن در ورودی

# تمیز کردن ورودی‌ها
def clear_search():
    entry_post.delete(0, tk.END)
    result_frame.pack_forget()

# راه‌اندازی رابط کاربری
root = tk.Tk()
root.title("Post Search")
root.geometry("700x600")  # افزایش اندازه صفحه

# فریم جستجو
search_frame = tk.Frame(root)
search_frame.pack(pady=20)

label_post = tk.Label(search_frame, text="Enter Post:")
label_post.grid(row=0, column=0, padx=10)

entry_post = tk.Entry(search_frame, width=30)  # کمی بزرگتر کردن عرض ورودی
entry_post.grid(row=0, column=1, padx=10)

search_button = tk.Button(search_frame, text="Search", command=search_post)
search_button.grid(row=0, column=2, padx=10)

paste_button = tk.Button(search_frame, text="Paste", command=paste_text)  # دکمه Paste اضافه شده
paste_button.grid(row=0, column=3, padx=10)

clear_button = tk.Button(search_frame, text="Clear", command=clear_search)
clear_button.grid(row=0, column=4, padx=10)

# فریم نتایج
result_frame = tk.Frame(root)

root.mainloop()
$$$$$$$$$$$$$$$$$$$$$$$$$
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ایجاد مرورگر داخلی
        self.browser = QWebEngineView()
        
        # بارگذاری وب‌سایت
        self.browser.setUrl(QUrl('https://saberafshar93.github.io/JIF/'))  # آدرس وب‌سایت شما به QUrl تبدیل شده
        
        # تنظیمات پنجره
        self.setCentralWidget(self.browser)
        self.setWindowTitle('Journal Impact Factor')
        self.setGeometry(100, 100, 1024, 768)

if __name__ == '__main__':
    # ایجاد اپلیکیشن و پنجره
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
