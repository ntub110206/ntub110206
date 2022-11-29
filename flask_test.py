import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask,request

app = Flask(__name__)
# 按播放鍵執行程式
@app.route("/")
def hello():
    return "Hello friend!"

@app.route("/userUpdate",methods=['POST'])
def userUpdate():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    name = request.values['name']
    pro = request.values['profession']
    salary = request.values['salary']
    budget = request.values['budget']
    # 格式
    docU = {
        'budget':budget,
        'name':name,
        'profession':pro,
        'salary':salary
    }
    # 寫入
    db.collection("users").document(uid).update(docU)

    return ""

@app.route("/budgetDel",methods=['POST'])
def budgetDel():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
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

@app.route("/accountAdd",methods=['POST'])
def accountAdd():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
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
    doc_Asnap = db.collection("users").document(uid).collection("Account").add(doc)
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

@app.route("/accountUpdate",methods=['POST'])
def accountUpdate():
    money = 0

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
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
    doc_accountRef = db.collection("users").document(uid).collection("Account").document(aid)
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
    db.collection("users").document(uid).collection("Account").document(aid).set(docA)
    
    # 更新資料庫
    docB = {'budget':budget}
    doc_budgetRef.update(docB)

    # 回傳至前端
    return f'{aid},{budget}'

@app.route("/bucketAdd",methods=['POST'])
def bucketAdd():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    target = request.values['target']
    date = request.values['date']
    month = request.values['month']
    tradeType = request.values['title']
    detail = request.values['detail']
    money = int(request.values['money'])
    part = int(request.values['part'])
    # 狀態定義
    status = "執行中"
    # 格式
    doc = {
        'date':date,
        'month':month,
        'target':target,
        'tradeType':tradeType,
        'detail':detail,
        'money':money,
        'part':part,
        'status':status
    }
    # 寫入
    db.collection("users").document(uid).collection("Bucket").add(doc)
    mess = "完成"

    # 回傳至前端
    return mess

@app.route("/bucketQuit",methods=['POST'])
def bucketQuit():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向目標
    doc_Bref = db.collection("users").document(uid).collection("Bucket")
    # 查詢所有目標文件
    doc_bucketRef = doc_Bref.stream()
    # 找出"執行中"的目標id
    for doc in doc_bucketRef:
        if doc.get('status') == "執行中":
            bid = doc.id
            break
    # 將目標的狀態變更為"已完成"
    doc_Bref = db.collection("users").document(uid).collection("Bucket").document(bid)
    docS = {'status':"已放棄"}
    doc_Bref.update(docS)

    return ""

@app.route("/bucketComplete",methods=['POST'])
def bucketComplete():
    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向目標
    doc_Bref = db.collection("users").document(uid).collection("Bucket")
    # 查詢所有目標文件
    doc_bucketRef = doc_Bref.stream()
    # 找出"執行中"的目標id
    for doc in doc_bucketRef:
        if doc.get('status') == "執行中":
            bid = doc.id
            tradeType = doc.get('tradeType')
            detail = doc.get('detail')
            money = doc.get('money')
            break
    # 將目標的狀態變更
    doc_Bref = db.collection("users").document(uid).collection("Bucket").document(bid)
    docS = {'status':"已完成"}
    doc_Bref.update(docS)

    # 回傳至前端
    return f'{tradeType},{detail},{money}'

@app.route("/getInfo",methods=['POST'])
def getInfo():
    check = 0
    costTotal = 0
    salaryTotal = 0
    sarplus = 0
    status = False

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
    doc_accountRef = db.collection("users").document(uid).collection("Account")
    # 查詢所有帳務
    doc_costRef = doc_accountRef.stream()
    # 取得支出，並計算該月總支出、總收入
    for doc in doc_costRef:
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costTotal += int(doc.get('money'))
        elif doc.get('tradeType') == "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            salaryTotal += int(doc.get('money'))
    # 計算盈餘
    sarplus = salaryTotal - costTotal
    # 指向目標
    doc_Bref = db.collection("users").document(uid).collection("Bucket")
    # 取得願望清單價錢，計算欲花費之預算
    # 查詢所有目標文件
    doc_bucketRef = doc_Bref.stream()
    # 找出"執行中"的目標
    for doc in doc_bucketRef:
        if doc.get('status') == "執行中":
            money = int(doc.get('money'))
            part = int(doc.get('part'))
            # 計算當月目標
            tarMoney = int(money / part)
            check += 1
            status = True
            break
    # 若無"執行中"的目標，回傳空值
    if check == 0:
        tarMoney = 0
    # 計算達成目標之剩餘金額
    targetMoney = tarMoney - sarplus

    # 回傳至前端
    return f'{user},{name},{profession},{budget},{salaryTotal},{costTotal},{tarMoney},{targetMoney},{status}'

@app.route("/getBucket",methods=['POST'])
def getBucket():
    costTotal = 0
    salaryTotal = 0
    check = 0
    remain = 0
    month = 0
    part = 0
    status = False

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向目標
    doc_Bref = db.collection("users").document(uid).collection("Bucket")
    # 查詢所有目標文件
    doc_bucketRef = doc_Bref.stream()
    # 找出"執行中"的目標
    for doc in doc_bucketRef:
        if doc.get('status') == "執行中":
            target = doc.get('target')
            money = int(doc.get('money'))
            part = int(doc.get('part'))
            month = int(doc.get('month'))
            # 計算當月目標
            tarMoney = int(money / part)
            check += 1
            status = True
            break

    # 計算並更新剩餘期數
    remain = part - (datetime.datetime.now().month - month)
    # 指向帳務資料
    doc_Aref = db.collection("users").document(uid).collection("Account")
    # 查詢所有帳務
    doc_costRef = doc_Aref.stream()
    # 取得帳務金額，並計算該月總支出、總收入
    for doc in doc_costRef:
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costTotal += int(doc.get('money'))
        elif doc.get('tradeType') == "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            salaryTotal += int(doc.get('money'))
    # 計算該月盈餘
    surplus = salaryTotal - costTotal
    if surplus < 0:
        surplus = 0
    # 若無"執行中"的目標，回傳空值
    if check == 0:
        target = ""
        tarMoney = 0
        surplus = 0
        remain = 0

    # 回傳至前端
    return f'{target},{tarMoney},{surplus},{status},{remain}'

# 1.當月與前一個月的總支出比較，看有沒有節省支出
@app.route("/result1",methods=['POST'])
def result1():
    result1 = False
    costThisTotal = 0
    costLastTotal = 0
    lastMonth = 0

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向帳務資料
    doc_Aref = db.collection("users").document(uid).collection("Account")
    # 查詢所有帳務
    doc_costRef = doc_Aref.stream()
    
    # 取得帳務金額
    for doc in doc_costRef:
        # 計算該月總支出
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costThisTotal += int(doc.get('money'))
            
        # 計算上個月總支出
        elif doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month - 1:
            costLastTotal += int(doc.get('money'))
            lastMonth += 1
    # 檢查上個月是否有紀錄
    if lastMonth > 0:
        # 比對是否有省到錢
        if costThisTotal > costLastTotal:
            result1 = True

    # 回傳至前端
    return f'{result1}'

# 2.比對本月跟上個月的各類支出，看哪些項目超標
@app.route("/result2",methods=['POST'])
def result2():
    result2 = ""
    result = []
    # 檢查項目定義
    tradeType = ['食','衣','行','育','樂','月結']
    tradeCode = [1,2,3,4,5,6]

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向帳務資料
    doc_Aref = db.collection("users").document(uid).collection("Account")

    # 逐次檢查項目
    for i in range(len(tradeType)):
        costThisTotal = 0
        costLastTotal = 0
        lastMonth = 0
        # 查詢所有帳務
        doc_costRef = doc_Aref.stream()
        # 取得帳務金額
        for doc in doc_costRef:
            # 計算該月項目總支出
            if doc.get('tradeType') == str(tradeType[i]) and int(doc.get('month')) == datetime.datetime.now().month:
                costThisTotal += int(doc.get('money'))
            # 計算上個月項目總支出
            elif doc.get('tradeType') == str(tradeType[i]) and int(doc.get('month')) == datetime.datetime.now().month - 1:
                costLastTotal += int(doc.get('money'))
                lastMonth += 1
        # 檢查上個月是否有項目紀錄
        if lastMonth > 0:
            result.append(costThisTotal-costLastTotal)
        else:
            result.append(0)

    # 利用氣泡排序找出最大的支出項目
    n = len(result)
    while n > 1:
        n -= 1
        for i in range(n):
            if result[i] < result[i+1]:
                result[i], result[i+1] = result[i+1], result[i]
                tradeType[i], tradeType[i+1] = tradeType[i+1], tradeType[i]
                tradeCode[i], tradeCode[i+1] = tradeCode[i+1], tradeCode[i]
    result2 = tradeCode[0]

    # 回傳至前端
    return f'{result2}'

# 3.比對本月的總支出比例，看哪一類的支出居多
@app.route("/result3",methods=['POST'])
def result():
    result3 = ""
    result = []
    # 檢查項目定義
    tradeType = ['食','衣','行','育','樂','月結']
    tradeCode = [1,2,3,4,5,6]

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向帳務資料
    doc_Aref = db.collection("users").document(uid).collection("Account")

    # 逐次檢查項目
    for i in range(len(tradeType)):
        costTotal = 0
        # 查詢所有帳務
        doc_costRef = doc_Aref.stream()
        # 取得帳務金額
        for doc in doc_costRef:
            # 計算該月項目總支出
            if doc.get('tradeType') == str(tradeType[i]) and int(doc.get('month')) == datetime.datetime.now().month:
                costTotal += int(doc.get('money'))
        result.append(str(costTotal))

    # 利用氣泡排序找出最大的支出項目
    n = len(result)
    while n > 1:
        n -= 1
        for i in range(n):
            if result[i] < result[i+1]:
                result[i], result[i+1] = result[i+1], result[i]
                tradeType[i], tradeType[i+1] = tradeType[i+1], tradeType[i]
                tradeCode[i], tradeCode[i+1] = tradeCode[i+1], tradeCode[i]
    result3 = tradeCode[0]

    # 回傳至前端
    return f'{result3}'

# 4.該月目標是否達標
@app.route("/result4",methods=['POST'])
def result4():
    result4 = ""
    costTotal = 0
    salaryTotal = 0
    check = 0
    remain = 0
    month = 0
    part = 0
    tarMoney = 0

    if not len(firebase_admin._apps):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    # 取得前端資訊
    uid = request.values['uid']
    # 指向目標
    doc_Bref = db.collection("users").document(uid).collection("Bucket")
    # 查詢所有目標文件
    doc_bucketRef = doc_Bref.stream()
    # 找出"執行中"的目標
    for doc in doc_bucketRef:
        if doc.get('status') == "執行中":
            money = int(doc.get('money'))
            part = int(doc.get('part'))
            month = int(doc.get('month'))
            # 計算當月目標
            tarMoney = int(money / part)
            check += 1
            status = True
            break

    # 計算並更新剩餘期數
    remain = part - (datetime.datetime.now().month - month)
    # 指向帳務資料
    doc_Aref = db.collection("users").document(uid).collection("Account")
    # 查詢所有帳務
    doc_costRef = doc_Aref.stream()
    # 取得帳務金額，並計算該月總支出、總收入
    for doc in doc_costRef:
        if doc.get('tradeType') != "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            costTotal += int(doc.get('money'))
        elif doc.get('tradeType') == "額外收入" and int(doc.get('month')) == datetime.datetime.now().month:
            salaryTotal += int(doc.get('money'))
    # 計算該月盈餘
    surplus = salaryTotal - costTotal
    if surplus < 0:
        surplus = 0
    # 計算是否達到目標
    if surplus >= tarMoney:
        status = 1
    else:
        status = 2
    # 若無"執行中"的目標，回傳空值
    if check == 0:
        status = 0

    # 回傳至前端
    return f'{status}'

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
