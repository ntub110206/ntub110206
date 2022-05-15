from PIL import Image
import pytesseract
import tkinter as tk

ui = tk.Tk()
ui.title('test')

img_name = './images/test02.png'
img = Image.open(img_name)
text = pytesseract.image_to_string(img, lang='chi_tra+eng')
line = text.split('\n')
str = line[10].split(':')
print(str[1])