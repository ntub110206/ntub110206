import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask,request

app = Flask(__name__)
#按播放鍵執行程式
@app.route("/")
def hello():
    return "Hello friend!"

@app.route("/cost",methods=['POST'])
def budgetCalculate():
    if(not len(firebase_admin._apps)):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    #取得前端資訊(uid,帳目總價)
    uid = request.values['uid']
    money = int(request.values['money'])
    # 取得資產總額
    doc_budgetRef = db.collection("users").document(uid)
    doc_snap = doc_budgetRef.get()
    budget = int(doc_snap.get('budget'))
    #計算記帳後資產
    budget -= money
    #更新資料庫
    doc = {'budget':budget}
    doc_budgetRef.update(doc)
    #回傳至前端
    return str(budget)

@app.route("/total")
def total():
    costTotal = 0
    selectTotal = 0
    if(not len(firebase_admin._apps)):
        # 引用私密金鑰
        cred = credentials.Certificate('./serviceAccount.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    #取得前端資訊(uid,交易項目)
    uid = request.values['uid']
    title = int(request.values['payType'])
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

    return [costTotal, selectTotal, proportion]

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
