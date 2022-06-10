import calendar
import datetime
import msvcrt
import mysql.connector
import pytesseract
import re
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
from locale import currency
from PIL import Image
from tkinter import messagebox, Label, filedialog

def tesseract_total():#文字辨識事件
        global result
        file = tk.Tk()
        file.withdraw()
        file_path = filedialog.askopenfilename()
        img_name = file_path
        img = Image.open(img_name)
        text = pytesseract.image_to_string(img, lang='chi_tra+eng')
        try:
                cost = re.search(r'總計\s*:\s*(\d+)', text)
                result = cost.group(1)
        except AttributeError:
                result = "not found"
        if accounts_Type == 1:
                PayMoney.insert(0,result)
        elif accounts_Type == 2:
                IncomeMoney.insert(0,result)

def Com():#儲存按鈕事件
        check = 0
        if accounts_Type == 1:   #1代表支出，2代表收入
                Pay = "支出"
                try:
                        Money = float(PayMoney.get())
                except:
                        messagebox.showwarning('警告','金額請輸入數字')
                        PayMoney.delete(0,'end')
                        check = 1
                if check == 0:
                        messagebox.showinfo('成功','已儲存一筆支出')
                        cursor.execute("insert into `account` values('"+ str(accounts_ID)           +"', '"
                                                                       + Pay                        +"', '"
                                                                       + PayItem.get()              +"', '"
                                                                       + PayTradeType.get()         + "', '"
                                                                       + str(datetime.date.today()) +"', '"
                                                                       + PayCurrency.get()          +"', "
                                                                       + str(Money)                 +", 'Amy','"
                                                                       + PayNote.get()              +"');"
                                                                       )
                        cursor.close()
                        connection.commit()
                        connection.close()
                        quit()

        elif accounts_Type == 2:
                Income = "收入"
                try:
                        Money = float(IncomeMoney.get())
                except:
                        messagebox.showwarning('警告','金額請輸入數字')
                        IncomeMoney.delete(0,'end')
                        check = 1
                if check == 0:
                        messagebox.showinfo('成功','已儲存一筆收入')
                        cursor.execute("insert into `account` values('"+ str(accounts_ID)           +"', '"
                                                                       + Income                     +"', '"
                                                                       + IncomeItem.get()           +"', '"
                                                                       + IncomeTradeType.get()      + "', '"
                                                                       + str(datetime.date.today()) +"', '"
                                                                       + IncomeCurrency.get()       +"', "
                                                                       + str(Money)                  +", 'Amy','"
                                                                       + IncomeNote.get()           +"');"
                                                                       )
                        cursor.close()
                        connection.commit()
                        connection.close()
                        quit()
        else:
                messagebox.showwarning('警告','請選擇記帳類別')
 
def pay_event():#支出按鈕事件
        global camera, PayMoney, PayItem, PayTradeType, PayCurrency, PayNote, accounts_Type
        accounts_Type = 1
        camera = tk.Button(#開啟文字識別
                window,
                text = '文字識別',
                bg = '#00EC00',
                fg = 'black',
                font = ('Arial', 12),
                width = 10,
                height = 1,
                command = tesseract_total
        )
        camera.grid(column=1, row=2, columnspan=2)

        Moneylbl = tk.Label(#金額標籤
                window,
                text = '金額',
                bg = 'orange',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        Moneylbl.grid(column=0, row=3, columnspan=3)
        
        PayMoney = tk.Entry(#輸入金額
                window,
                width = 10
        )
        PayMoney.grid(column=3, row=3)
    
        ItemTypelbl = tk.Label(#類別標籤
                window,
                text = '類別',
                bg = '#59deff',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        ItemTypelbl.grid(column=0, row=4, columnspan=3)

        PayItem = ttk.Combobox(#選擇支出類別
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '飲食',
                          '日常用品',
                          '交通',
                          '電信',
                          '服飾',
                          '娛樂',
                          '文具用品',
                          '醫療保健',
                          '旅遊',
                          '其他']
        )
        PayItem.current(0)#將支出類別預設為飲食
        PayItem.grid(column=3, row=4)

        TradeTypelbl = tk.Label(#交易方式標籤
                window,
                text = '交易方式',
                bg = 'orange',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        TradeTypelbl.grid(column=0, row=5, columnspan=3)

        PayTradeType = ttk.Combobox(#選擇交易方式
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '現金',
                          '信用卡',
                          '轉帳']
        )
        PayTradeType.current(0)#將交易方式預設為現金
        PayTradeType.grid(column=3, row=5)

        Currencylbl = tk.Label(#貨幣標籤
                window,
                text = '貨幣',
                bg = '#59deff',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        Currencylbl.grid(column=0, row=6, columnspan=3)

        PayCurrency = ttk.Combobox(#選擇貨幣
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '新台幣',
                          '美金',
                          '人民幣',
                          '日圓',
                          '歐元']
        )
        PayCurrency.current(0)#將貨幣預設為新台幣
        PayCurrency.grid(column=3, row=6)

        blank2 = tk.Label(#間隔
                window,
                width = 40,
                height = 2
        )
        blank2.grid(column=0, row=7, columnspan=4)

        Notelbl = tk.Label(#記帳備註標籤
                window,
                text = '備註',
                bg = 'white',
                fg = 'black',
                font = ('Arial', 12),
                width = 10,
                height = 2
        )
        Notelbl.grid(column=0, row=8)

        PayNote = tk.Entry(window, width = 20)#撰寫記帳備註
        PayNote.grid(column=1, row=8, columnspan=2)

def income_event():#收入按鈕事件
        global IncomeMoney, IncomeItem, IncomeTradeType, IncomeCurrency, IncomeNote, accounts_Type
        accounts_Type = 2
        blank3 = tk.Label(#開啟文字識別
                window,
                width = 40,
                height = 2
        )
        blank3.grid(column=1, row=2, columnspan=4)

        Moneylbl = tk.Label(#金額標籤
                window,
                text = '金額',
                bg = 'orange',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        Moneylbl.grid(column=0, row=3, columnspan=3)
        
        IncomeMoney = tk.Entry(#輸入金額
                window,
                width = 10
        )
        IncomeMoney.grid(column=3, row=3)
    
        ItemTypelbl = tk.Label(#類別標籤
                window,
                text = '類別',
                bg = '#59deff',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        ItemTypelbl.grid(column=0, row=4, columnspan=3)

        IncomeItem = ttk.Combobox(#選擇收入類別
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '工資',
                          '獎金',
                          '投資',
                          '其他']
        )
        IncomeItem.current(0)#將收入類別預設為工資
        IncomeItem.grid(column=3, row=4)

        TradeTypelbl = tk.Label(#交易方式標籤
                window,
                text = '交易方式',
                bg = 'orange',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        TradeTypelbl.grid(column=0, row=5, columnspan=3)

        IncomeTradeType = ttk.Combobox(#選擇交易方式
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '現金',
                          '轉帳']
        )
        IncomeTradeType.current(0)#將交易方式預設為現金
        IncomeTradeType.grid(column=3, row=5)

        Currencylbl = tk.Label(#貨幣標籤
                window,
                text = '貨幣',
                bg = '#59deff',
                fg = 'black',
                font = ('Arial', 12),
                width = 30,
                height = 2
        )
        Currencylbl.grid(column=0, row=6, columnspan=3)

        IncomeCurrency = ttk.Combobox(#選擇貨幣
                window,
                width = 10,
                state = 'readonly',
                values = [
                          '新台幣',
                          '美金',
                          '人民幣',
                          '日圓',
                          '歐元']
        )
        IncomeCurrency.current(0)#將貨幣預設為新台幣
        IncomeCurrency.grid(column=3, row=6)

        blank2 = tk.Label(#間隔
                window,
                width = 40,
                height = 2
        )
        blank2.grid(column=0, row=7, columnspan=4)

        Notelbl = tk.Label(#記帳備註標籤
                window,
                text = '備註',
                bg = 'white',
                fg = 'black',
                font = ('Arial', 12),
                width = 10,
                height = 2
        )
        Notelbl.grid(column=0, row=8)

        IncomeNote = tk.Entry(window, width = 20)#撰寫記帳備註
        IncomeNote.grid(column=1, row=8, columnspan=2)        


##################################################################

connection = mysql.connector.connect(
             host = '140.131.114.242',
             port = '3306',
             user = 'MyFinGrasper',
             password = 'FGDB_Pass@111',
             database ='111- MyFinGrasperDB'
)
cursor = connection.cursor()

cursor.execute('SELECT COUNT(*) FROM `account`;')
records = cursor.fetchall()         #[(0,)]
countList = str(records).split('(') #['[','0,)]']
count = countList[1].split(',')     #['0',')]']
#print(count[0])                     # 0

accounts_ID = int(count[0])  
accounts_ID += 1

accounts_Type = 0 #初值設定

##################################################################

window = tk.Tk()
window.title('記帳表單')
window.geometry('400x600')
cancel = tk.Button(#取消鍵
        window,
        text = '取消',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command=quit
)
cancel.grid(column=0, row=0)#column為直欄，row為橫列

pay = tk.Button(#支出鍵
        window,
        text = '支出',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command = pay_event
)
pay.grid(column=1, row=0)

income = tk.Button(#收入鍵
        window,
        text = '收入',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command = income_event
)#camera.grid_forget():在記錄收入時隱藏文字識別按鈕
income.grid(column=2, row=0)

save = tk.Button(#儲存鍵
        window,
        text = '儲存',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command = Com #IncomeCom()
)
save.grid(column=3, row=0)

datelbl = tk.Label(#日期標籤
        window,
        text = '日期',
        bg = 'white',
        fg = 'black',
        font = ('Arial', 12),
        width = 10,
        height = 1
)
datelbl.grid(column=0, row=1, columnspan=1)

date = tk.Entry(#選擇的日期
        window, 
        width = 20,
)
date.insert(0,datetime.date.today())
date.config(state = 'readonly')
date.grid(column=0, row=1, columnspan=4)
#print(datetime.date.today())
blank1 = tk.Label(#間隔
        window,
        width = 40,
        height = 2
)
blank1.grid(column=0, row=2, columnspan=4)

window.mainloop()