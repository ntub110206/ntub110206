from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import Label, filedialog, ttk
import re
import sys
import msvcrt

def tesseract_total(filename):
    img_name = file_path
    img = Image.open(img_name)
    text = pytesseract.image_to_string(img, lang='chi_tra+eng')
    try:
        cost = re.search(r'總計\s*:\s*(\d+)', text)
        result = cost.group(0)
    except AttributeError:
        return "not found"
    return result

accountUI = tk.Tk()
accountUI.title('記帳表單')
accountUI.geometry('400x600')

file = tk.Tk()
file.withdraw()
file_path = filedialog.askopenfilename()
txt = tesseract_total(file_path)
tk.Label(accountUI, bg='blue', fg='white', text=txt, font=('Arial', 18), width="30", height="5").pack()
tk.Button(accountUI, text="退出", font=('Arial', 18), width="30", height="5", command=quit).pack()

accountUI.mainloop()