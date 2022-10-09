import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask,request

app = Flask(__name__)
#按播放鍵執行程式
@app.route("/")
def hello():
    return "Hello friend!"

@app.route("/cost",methods=['POST'])
def get_user():
    # 引用私密金鑰
    cred = credentials.Certificate('./serviceAccount.json')
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    #取得uid
    data = request.get_json()
    uid = data.get('uid')
    aid = data.get('aid')
    # 取得帳目總價
    doc_moneyRef = db.collection("users").document(uid).collection("dataArray").document(aid)
    doc_snap = doc_moneyRef.get()
    #doc_snap.get('欄位名稱')
    Data = doc_snap.get('cost')
    print(Data)
    return Data

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
