class Database:
 def init(self):
# 사용자 데이터: 사용자명: {password: 암호, balance: 잔액, history: 거래내역 리스트}
  self.users = {
"alice": {"password": "alice123", "balance": 1000, "history": []},
"bob": {"password": "bob123", "balance": 500, "history": []},
}

# 사용자 로그인 정보 확인
def verify_user_credentials(self, username, password):
    # 사용자 존재 여부 및 비밀번호 매칭 확인
    if username in self.users and self.users[username]["password"] == password:
        return True
    return False

# 계좌 잔액 반환
def get_balance(self, username):
    if username in self.users:
        return self.users[username]["balance"]
    return None

# 계좌 잔액 업데이트
def update_balance(self, username, new_balance):
    if username in self.users:
        self.users[username]["balance"] = new_balance
        return True
    return False

# 거래 내역 기록 (출금 및 입금 내역 기록)
def record_transaction(self, from_user, to_user, amount):
    # 출금 내역 기록
    if from_user in self.users:
        self.users[from_user]["history"].append({
            "type": "debit",
            "amount": amount,
            "to": to_user,
            "timestamp": time.time()
        })
    # 입금 내역 기록
    if to_user in self.users:
        self.users[to_user]["history"].append({
            "type": "credit",
            "amount": amount,
            "from": from_user,
            "timestamp": time.time()
        })
