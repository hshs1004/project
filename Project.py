import time

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

class ExternalGateway:
    # 이체 승인 요청을 시뮬레이션하는 메서드 
             def approve_transfer(self, transfer_details):
    # 외부 통신의 지연을 시뮬레이션 (여기에서는 1초 지연)
              time.sleep(1)
    # 여기서 추가적인 검증 로직을 넣을 수 있음. 간단히 승인 응답 반환.
              return True

class AppServer:
     def init(self, database, external_gateway):
      self.database = database
      self.external_gateway = external_gateway

    # 로그인 요청 처리
     def login(self, username, password):
        # 데이터베이스에 사용자 검증 요청
        if self.database.verify_user_credentials(username, password):
            return {"status": "success", "message": "로그인 성공"}
        else:
            return {"status": "failure", "message": "사용자 이름 또는 비밀번호 오류"}

    # 이체 요청 처리 - 트랜잭션 시뮬레이션 포함
     def transfer_funds(self, sender, recipient, amount):
        print("트랜잭션 시작")
        # 금액이 숫자이고 양수인지 확인
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("이체 금액은 양수여야 합니다.")
        except ValueError as e:
            return {"status": "failure", "message": f"잘못된 금액: {e}"}

        # 수취인 존재 확인
        if recipient not in self.database.users:
            return {"status": "failure", "message": "받는 사람 계좌가 존재하지 않습니다."}

        # 보내는 사람의 잔액 확인
        sender_balance = self.database.get_balance(sender)
        if sender_balance is None:
            return {"status": "failure", "message": "보내는 사람 계좌가 존재하지 않습니다."}

        if sender_balance < amount:
            return {"status": "failure", "message": "잔액 부족"}

        # 외부 금융망으로 이체 승인 요청
        transfer_details = {"from": sender, "to": recipient, "amount": amount}
        approval = self.external_gateway.approve_transfer(transfer_details)
        
        if approval:
            # 승인된 경우 금액 차감 및 추가
            new_sender_balance = sender_balance - amount
            recipient_balance = self.database.get_balance(recipient)
            new_recipient_balance = recipient_balance + amount

            # 데이터베이스 업데이트 (동시에 두 계좌의 거래 기록을 남김)
            self.database.update_balance(sender, new_sender_balance)
            self.database.update_balance(recipient, new_recipient_balance)
            self.database.record_transaction(sender, recipient, amount)

            print("트랜잭션 종료")
            return {"status": "success", "message": "이체 성공"}
        else:
            print("트랜잭션 종료")
            return {"status": "failure", "message": "외부 금융망 이체 승인 실패"}

class AppWeb:
     def init(self, app_server):
      self.app_server = app_server

    # 로그인 화면 처리
     def login_screen(self, username, password):
        response = self.app_server.login(username, password)
        if response["status"] == "success":
            print("로그인 성공 화면 표시")
        else:
            print("로그인 실패: ", response["message"])
        return response

    # 이체 화면 처리
     def transfer_screen(self, sender, recipient, amount):
        response = self.app_server.transfer_funds(sender, recipient, amount)
        if response["status"] == "success":
            print("이체 완료 화면 표시")
        else:
            print("이체 실패: ", response["message"])
        return response

     def main():
    # 데이터베이스, 외부 금융망, 애플리케이션 서버 인스턴스 생성
      database = Database()
      external_gateway = ExternalGateway()
      app_server = AppServer(database, external_gateway)
      app_web = AppWeb(app_server)

