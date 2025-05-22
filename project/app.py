from flask import Flask, request, jsonify
from database import *
from external_gateway import request_transfer_to_gateway

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = find_user_by_credentials(data['username'], data['password'])
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    from_user = data['from_user']
    to_user = data['to_user']
    amount = data['amount']

    balance = get_account_balance(from_user)
    if balance is None or balance < amount:
        return jsonify({"status": "fail", "message": "잔액 부족"}), 400

    # 외부 금융망 승인 요청
    if not request_transfer_to_gateway(from_user, to_user, amount):
        return jsonify({"status": "fail", "message": "외부 금융망 오류"}), 500

    # DB 트랜잭션
    success = update_balances_and_log_transfer(from_user, to_user, amount)
    if success:
        return jsonify({"status": "success", "message": "이체 완료"})
    else:
        return jsonify({"status": "fail", "message": "DB 처리 오류"}), 500

if __name__ == '__main__':
    app.run(debug=True)
