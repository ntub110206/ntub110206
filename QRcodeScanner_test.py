import cv2
import numpy
import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog

def decodeDisplay(image1):
    #灰階轉換
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)

    for barcode in barcodes:
        #將條碼資料轉換成字串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        #輸出
        print("掃描結果==》 類別： {0} 內容： {1}".format(barcodeType, barcodeData))

file = tk.Tk()
file.withdraw()
file_path = filedialog.askopenfilename()
# print(file_path)
cv2.namedWindow("camera",cv2.WINDOW_NORMAL)
img = cv2.imread(file_path)
# print(type(img))
decodeDisplay(img)