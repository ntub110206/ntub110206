import re
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

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
