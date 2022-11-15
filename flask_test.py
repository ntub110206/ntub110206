import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask,request

app = Flask(__name__)
# 按播放鍵執行程式
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

    # 取得前端資訊(uid,帳目總價,交易項目)
    uid = request.values['uid']
    money = int(request.values['money'])
    title = request.values['payType']
    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))
    # 計算記帳後資產
    if title == "額外收入":
        budget += money
    else:
        budget -= money
    # 更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)
    # 回傳至前端
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
    # 計算帳物刪除後資產
    if title == "額外收入":
        budget -= int(money)
    else:
        budget += int(money)
    # 更新資料庫
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
    # 取得前端資訊(更改後帳目金額,更改後帳目大項)
    afterMoney = int(request.values['money'])
    afterTitle = request.values['title']
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
    # 更新資料庫
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
    # 格式
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
    aid = doc_Asnap[1].id

    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))
    # 計算記帳後資產
    if tradeType == "額外收入":
        budget += money
    else:
        budget -= money
    # 更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)
    # 回傳至前端
    return f'{aid},{budget}'

@app.route("/update",methods=['POST'])
def update():
    money = 0
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊(uid,帳目資訊)
    uid = request.values['uid']
    aid = request.values['aid']
    date = request.values['date']
    year = request.values['year']
    month = request.values['month']
    data = request.values['data']
    afterTitle = request.values['title']
    detail = request.values['detail']
    afterMoney = int(request.values['money'])

# 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))

    # 取得更改前帳目金額
    doc_accountRef = db.collection("users").document(uid).collection("dataArray").document(aid)
    doc_Asnap = doc_accountRef.get()
    beforeMoney = int(doc_Asnap.get('money'))
    # 取得更改前帳目大項
    beforeTitle = doc_Asnap.get('tradeType')

    # 計算帳務變更後資產
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

    # 格式
    docA = {
        'date':date,
        'year':year,
        'month':month,
        'data':data,
        'tradeType':afterTitle,
        'detail':detail,
        'money':afterMoney,
    }
    # 寫入
    db.collection("users").document(uid).collection("dataArray").document(aid).set(docA)
    
    # 更新資料庫
    docB = {'budget':budget}
    doc_budgetRef.update(docB)
    # 回傳至前端
    return f'{aid},{budget}'

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

    # 計算支出比例
    proportion = selectTotal/costTotal*100

    # 回傳至前端
    return f'{costTotal},{selectTotal},{proportion}'

@app.route("/get",methods=['POST'])
def get():
    costTotal = 0
    salaryTotal = 0
    shoppingTotal = 0
    target = True
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊(uid)
    uid = request.values['uid']

    # 指向用戶資料
    doc_userRef = db.collection("users").document(uid).get()
    # 取得帳號
    user = doc_userRef.get('user')
    # 取得暱稱
    name = doc_userRef.get('name')
    # 取得職稱
    profession = doc_userRef.get('profession')
    # 取得資產總額
    budget = int(doc_userRef.get('budget'))

    # 指向帳務資料
    doc_accountRef = db.collection("users").document(uid).collection("dataArray")
    # 查詢所有文件
    doc_costRef = doc_accountRef.stream()
    # 取得支出，並計算該月總支出、總收入
    for doc in doc_costRef:
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costTotal += int(doc.get('money'))
        elif doc.get('tradeType') == "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            salaryTotal += int(doc.get('money'))

    # 指向願望清單

    # 取得願望清單價錢，計算欲花費之預算
    

    # 計算達成目標之剩餘金額
    targetMoney = shoppingTotal - budget

    # 回傳至前端
    return f'{user},{name},{profession},{budget},{salaryTotal},{costTotal},{shoppingTotal},{targetMoney}'

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
