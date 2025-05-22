def request_transfer_to_gateway(from_user_id, to_user_id, amount):
    # 외부 금융망과 통신하는 부분 (여기서는 mock)
    print(f"External gateway 요청: {from_user_id} -> {to_user_id}, 금액: {amount}")
    return True  # 항상 성공하는 것으로 간주
