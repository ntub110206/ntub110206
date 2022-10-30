import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask,request

app = Flask(__name__)
#按播放鍵執行程式
@app.route("/")
def hello():
    return "Hello friend!"

@app.route("/budgetAdd",methods=['POST'])
def budgetAdd():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()

    #取得前端資訊(uid,帳目總價,交易項目)
    uid = request.values['uid']
    money = int(request.values['money'])
    title = request.values['payType']
    print(title)
    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))
    #計算記帳後資產
    if title == "額外收入":
        budget += money
    else:
        budget -= money
    #更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)
    #回傳至前端
    return str(budget)

@app.route("/budgetDel",methods=['POST'])
def budgetDel():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊(uid,帳目金額,帳目大項)
    uid = request.values['uid']
    money = request.values['money']
    title = request.values['title']
    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_Bsnap = doc_budgetRef.get()
    budget = int(doc_Bsnap.get('budget'))
    #計算帳物刪除後資產
    if title == "額外收入":
        budget -= int(money)
    else:
        budget += int(money)
    #更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)

    return ""

@app.route("/budgetUpdate",methods=['POST'])
def budgetUpdate():
    money = 0
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊(uid,aid)
    uid = request.values['uid']
    aid = request.values['aid']
    # 取得更改前帳目金額
    doc_accountRef = db.collection("users").document(uid).collection("dataArray").document(aid)
    doc_Asnap = doc_accountRef.get()
    beforeMoney = int(doc_Asnap.get('money'))
    # 取得更改前帳目大項
    beforeTitle = doc_Asnap.get('tradeType')
    print(beforeTitle)
    # 取得前端資訊(更改後帳目金額,更改後帳目大項)
    afterMoney = int(request.values['money'])
    afterTitle = request.values['title']
    print(afterTitle)
    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_Bsnap = doc_budgetRef.get()
    budget = int(doc_Bsnap.get('budget'))
    if beforeTitle != "額外收入" and afterTitle == "額外收入":
        money = beforeMoney + afterMoney
        budget += money
    elif beforeTitle == "額外收入" and afterTitle != "額外收入":
        money = beforeMoney + afterMoney
        budget -= money
    elif beforeTitle == "額外收入" and afterTitle == "額外收入":
        if beforeMoney > afterMoney:
            money = int(beforeMoney) - afterMoney
            budget -= money
        elif beforeMoney < afterMoney:
            money = afterMoney - int(beforeMoney)
            budget += money
    else:
        if beforeMoney > afterMoney:
            money = beforeMoney - afterMoney
            budget += money
        elif beforeMoney < afterMoney:
            money = afterMoney - beforeMoney
            budget -= money
    #更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)

    return ""

@app.route("/add",methods=['POST'])
def add():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊(uid,帳目資訊)
    uid = request.values['uid']
    date = request.values['date']
    year = request.values['year']
    month = request.values['month']
    data = request.values['data']
    tradeType = request.values['title']
    detail = request.values['detail']
    money = int(request.values['money'])
    #格式
    doc = {
        'date':date,
        'year':year,
        'month':month,
        'data':data,
        'tradeType':tradeType,
        'detail':detail,
        'money':money,
    }
    # 寫入
    doc_Asnap = db.collection("users").document(uid).collection("dataArray").add(doc)

    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))
    #計算記帳後資產
    if tradeType == "額外收入":
        budget += money
    else:
        budget -= money
    #更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)
    #回傳至前端
    return f'{doc_Asnap[1].id},{budget}'

@app.route("/total",methods=['POST'])
def total():
    costTotal = 0
    selectTotal = 0
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    #取得前端資訊(uid,交易項目)
    uid = request.values['uid']
    title = request.values['payType']
    # 指向
    doc_ref = db.collection("users").document(uid).collection("dataArray")

    # 查詢所有文件
    doc_costRef = doc_ref.stream()
    # 計算該月總支出
    for doc in doc_costRef:
        if doc.get('tradeType') == "支出" and doc.get('month') == datetime.datetime.now().month:
            costTotal += doc.get('money')

    
    # 查詢特定內容文件
    doc_selectRef = doc_ref.where("payType","==",title).stream()
    # 計算該月特定項目總支出
    for doc in doc_selectRef:
        if doc.get('month') == datetime.datetime.now().month:
            selectTotal += doc.to_dict().get('money')

    #計算支出比例
    proportion = selectTotal/costTotal*100

    #回傳至前端
    return f'{costTotal},{selectTotal},{proportion}'

@app.route("/get",methods=['POST'])
def get():
    costTotal = 0
    incomeTotal = 0
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    #取得前端資訊(uid)
    uid = request.values['uid']

    # 指向
    doc_budgetRef = db.collection("users").document(uid)
    # 取得資產總額
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))

    # 指向
    doc_ref = db.collection("users").document(uid).collection("dataArray")
    # 查詢所有文件
    doc_costRef = doc_ref.stream()
    # 取得支出，並計算該月總支出
    for doc in doc_costRef:
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costTotal += int(doc.get('money'))
        elif doc.get('tradeType') == "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            incomeTotal += int(doc.get('money'))
    
    #回傳至前端
    return f'{budget},{incomeTotal},{costTotal}'

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
