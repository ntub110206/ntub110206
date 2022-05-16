from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog

ui = tk.Tk()
ui.title('test')

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
print(file_path)

img_name = file_path
img = Image.open(img_name)
text = pytesseract.image_to_string(img, lang='chi_tra+eng')
line = text.split('\n')
print(line)