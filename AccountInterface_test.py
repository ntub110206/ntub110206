import tkinter as tk
#from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import messagebox
import datetime
import time
import calendar



def com():
    buffer = 0
    try:
        Money = float(money.get())
    except:
        messagebox.showwarning('警告','金額請輸入數字')
        buffer = 1
    if buffer == 0:
        messagebox.showinfo('成功','已儲存一筆支出')   

        

def pay_event():  
    camera = tk.Button(#開啟文字識別
             window,
             text = '文字識別',
             bg = '#00EC00',
             fg = 'black',
             font = ('Arial', 12),
             width = 10,
             height = 1
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
    global money
    money = tk.Entry(#輸入金額
                window,
                width = 10
        )
    money.grid(column=3, row=3)
    
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
                    '其他'],
            width = 10,
            state = 'readonly'
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

    TradeType = ttk.Combobox(#選擇交易方式
            window,
            values = [
                    '現金',
                    '信用卡',
                    '轉帳'],
            width = 10,
            state = 'readonly'
    )
    TradeType.current(0)#將交易方式預設為現金
    TradeType.grid(column=3, row=5)

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

    currency = ttk.Combobox(#選擇貨幣
            window,
            values = [
                    '新台幣',
                    '美金',
                    '人民幣',
                    '日圓',
                    '歐元'],
            width = 10,
            state = 'readonly'
    )
    currency.current(0)#將貨幣預設為新台幣
    currency.grid(column=3, row=6)

    blank2 = tk.Label(#間隔
            window,
            width = 40,
            height = 2
    )
    blank2.grid(column=0, row=7, columnspan=4)

    Notelbl = tk.Label(#備註標籤
            window,
            text = '備註',
            bg = 'white',
            fg = 'black',
            font = ('Arial', 12),
            width = 10,
            height = 2
    )
    Notelbl.grid(column=0, row=8)

    note = tk.Entry(window, width = 20)
    note.grid(column=1, row=8, columnspan=2)

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
        height = 2
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
        height = 2
)
income.grid(column=2, row=0)

save = tk.Button(#儲存鍵
        window,
        text = '儲存',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command = com
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
print(datetime.date.today())
blank1 = tk.Label(#間隔
            window,
            width = 40,
            height = 2
)
blank1.grid(column=0, row=2, columnspan=4)

window.mainloop()