from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog
import re

def tesseract(filename):
    img_name = file_path
    img = Image.open(img_name)
    text = pytesseract.image_to_string(img, lang='chi_tra+eng')
    cost = re.search(r'總計\s*:\s*(\d+)', text)
    result = cost.group(0)
    return result
    
file = tk.Tk()
file.withdraw()
file_path = filedialog.askopenfilename()
# print(file_path)
txt = tesseract(file_path)

print(txt)