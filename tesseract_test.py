from unittest import result
from PIL import Image
import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
import re

def tesseract_total(filename):
    img = cv2.imread(filename)
    rimg = cv2.resize(img, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
    text = pytesseract.image_to_string(rimg, lang='chi_tra')
    # show(rimg)
    # return text
    try:
        # cost = re.search(r'總計:\s*(\d+)', text)
        # cost = re.search(r'總計\s* \s*(\d+)', text)
        # cost = re.search(r'總\s* \s*計\s* \s*(\d+)', text)
        # cost = re.search(r'發票金額\s* \s*(\d+)', text)
        # cost = re.search(r'\$\s*(\d+)', text)
        # result = cost.group(0)
        #spec_list
        cost = re.search(r'\$\s*(\d,\s*\d+)', text)
        cut = re.search(r'(,\s*)', cost.group(0))
        cost_num = cost.group(0).split(cut.group(0))
        result = ''
        for num in cost_num:
            result += num
    except AttributeError:
        return "not found"
    return result

def show(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

file = tk.Tk()
file.withdraw()
file_path = filedialog.askopenfilename()
# print(file_path)
txt = tesseract_total(file_path)

print(txt)