import tkinter as tk
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import messagebox

def button_event():#判斷金額欄的輸入值是否正確
    print(money.get())
    if money.get() == '':
        tk.messagebox.showerror('message', '請輸入金額')
    else:
        tk.messagebox.showinfo('message', '已新增一筆帳目')

def validate(P):
    print(P)
    if str.isdigit(P) or P == '':
        return True
    else:
        return False

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
pay = tk.Button(#支出鍵
        window,
        text = '支出',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2
)
income = tk.Button(#收入鍵
        window,
        text = '收入',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2
)
save = tk.Button(#儲存鍵
        window,
        text = '儲存',
        bg = '#59deff',
        fg = 'white',
        font = ('Arial', 12),
        width = 10,
        height = 2,
        command = button_event
)
AccountingWay = ttk.Combobox(#選擇記帳方式
        window,
        values = [
                '手動輸入',
                '文字辨識輸入']
)
AccountingWay.current(0)#選擇記帳方式預設為手動輸入
date = tk.Entry(window, width = 20)#選擇的日期，尚未完成
Moneylbl = tk.Label(#金額標籤
        window,
        text = '金額',
        bg = 'white',
        fg = 'black',
        font = ('Arial', 12),
        width = 30,
        height = 2
)
Moneycmd = (window.register(validate), '%P')
money = tk.Entry(#輸入金額
        window,
        validate ='key',
        validatecommand = Moneycmd,
        width = 10
)
ItemTypelbl = tk.Label(#類別標籤
        window,
        text = '類別',
        bg = 'white',
        fg = 'black',
        font = ('Arial', 12),
        width = 30,
        height = 2
)
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
        width = 10
)
PayItem.current(0)#將支出類別預設為飲食
blank = tk.Label(#間隔
        window,
        width = 40,
        height = 2
)
Notelbl = tk.Label(#備註標籤
        window,
        text = '備註',
        bg = 'white',
        fg = 'black',
        font = ('Arial', 12),
        width = 10,
        height = 2
)
note = tk.Entry(window, width = 30)




cancel.grid(column=0, row=0)
pay.grid(column=1, row=0)
income.grid(column=2, row=0)
save.grid(column=3, row=0)
AccountingWay.grid(column=1, row=1, columnspan=2)
date.grid(column=0, row=2, columnspan=4)
Moneylbl.grid(column=0, row=3, columnspan=3)
money.grid(column=3, row=3)
ItemTypelbl.grid(column=0, row=4, columnspan=3)
PayItem.grid(column=3, row=4)
blank.grid(column=0, row=5, columnspan=4)
Notelbl.grid(column=0, row=6)
note.grid(column=1, row=6, columnspan=3)

window.mainloop()