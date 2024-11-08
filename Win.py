pip install requests matplotlib

import tkinter as tk
from tkinter import messagebox
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# جستجو بر اساس ISSN
def search_issn():
    issn = entry_issn.get().strip()
    if not issn:
        messagebox.showwarning("Input Error", "Please enter an ISSN.")
        return
    
    data = load_data()
    
    if not data:
        return
    
    # جستجو در داده‌ها
    result = None
    for item in data:
        if item['ISSN'].lower() == issn.lower() or item['EiSSN'].lower() == issn.lower():
            result = item
            break
    
    if result:
        display_results(result)
        plot_chart(result)
    else:
        messagebox.showinfo("No Results", "No data found for the entered ISSN.")

# نمایش نتایج در جدول
def display_results(item):
    result_frame.pack_forget()  # پاک کردن نتایج قبلی
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    table = tk.Text(result_frame, wrap=tk.WORD, height=10, width=60)
    table.insert(tk.END, f"ISSN: {item.get('ISSN', 'Not Available')}\n")
    table.insert(tk.END, f"EiSSN: {item.get('EiSSN', 'Not Available')}\n")
    table.insert(tk.END, f"Journal Name: {item.get('Journalname', 'Not Available')}\n")
    table.insert(tk.END, f"Category: {item.get('Category', 'Not Available')}\n")
    table.insert(tk.END, f"Total Citations 2023: {item.get('TotalCitations', 'Not Available')}\n")
    table.insert(tk.END, f"JIF 2023 (Impact Factor): {item.get('JIF 2023', 'Not Available')}\n")
    table.insert(tk.END, f"JIF Quartile 2023: {item.get('JIFQuartile', 'Not Available')}\n")
    table.insert(tk.END, f"JCI 2023: {item.get('JCI 2023', 'Not Available')}\n")
    table.insert(tk.END, f"% of OA Gold 2023: {item.get('% of OA Gold', 'Not Available')}\n")
    table.pack()

# رسم نمودار JIF
def plot_chart(item):
    jif_data = [
        item.get('Column_12', None),
        item.get('Column_11', None),
        item.get('Column_10', None),
        item.get('JIF 2023', None)
    ]
    
    # حذف مقادیر None از داده‌ها
    jif_data = [data for data in jif_data if data is not None]
    years = ['2020', '2021', '2022', '2023'][:len(jif_data)]
    
    if not jif_data:
        return
    
    # رسم نمودار
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(years, jif_data, marker='o', color='b', label='JIF (Impact Factor)')
    ax.set_xlabel('Years')
    ax.set_ylabel('Impact Factor')
    ax.set_title('Impact Factor over Years')
    ax.legend()
    
    # نمایش نمودار در Tkinter
    chart_canvas = FigureCanvasTkAgg(fig, master=result_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack()

# تمیز کردن ورودی‌ها
def clear_search():
    entry_issn.delete(0, tk.END)
    result_frame.pack_forget()

# راه‌اندازی رابط کاربری
root = tk.Tk()
root.title("JIF Search")

# فریم جستجو
search_frame = tk.Frame(root)
search_frame.pack(pady=20)

label_issn = tk.Label(search_frame, text="Enter ISSN:")
label_issn.grid(row=0, column=0, padx=10)

entry_issn = tk.Entry(search_frame, width=20)
entry_issn.grid(row=0, column=1, padx=10)

search_button = tk.Button(search_frame, text="Search", command=search_issn)
search_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(search_frame, text="Clear", command=clear_search)
clear_button.grid(row=0, column=3, padx=10)

# فریم نتایج
result_frame = tk.Frame(root)

root.mainloop()
