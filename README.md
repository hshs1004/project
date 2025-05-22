# 소프트웨어공학 개인 과제
20210014 남현식

소프트웨어공학이란 사전적 의미로 컴퓨터 프로그램 및 그와 관련된 문서들을 통틀어 이르고 컴퓨터를 관리하는 시스템 프로그램과, 문제 해결에 이용되는 다양한 형태의 응용 프로그램으로 나뉩니다.
예로 윈도우, 리눅스, 유닉스와 같은 운영체제와 어셈블러, 컴파일러, 인터프리터와 같은 언어 번역 프로그램이 대표적인 시스템 소프트웨어입니다. 
대표적인 응용 소프트웨어로는 한글, 워드, 엑셀, 파워포인트, 오라클 또는 액세스와 같은 데이터베이스 관리 시스템, 포토샵, 웹 브라우저 및 FTP와 같은 통신 프로그램이 있습니다.

소프트웨어 적용 사례로는 버스정류장 모니터, 스마트폰 지도, loT(사물 인터넷), 스마트팜, 인터넷 은행, VR(가상현실) 등이 있습니다. 이 중에서 제가 주제로 선택한 사례는 인터넷 은행입니다.

다음은 Mermaid live를 활용하여 인터넷 은행 시스템을 시퀀스 다이어그램으로 작성합니다. 코드는 아래와 같습니다.


sequenceDiagram
    participant User as 사용자
    participant AppWeb as 모바일 앱/웹 브라우저
    participant AppServer as 애플리케이션 서버
    participant Database as 데이터베이스
    participant ExternalGateway as 외부 금융망/결제 게이트웨이

    User->>AppWeb: 로그인 정보 입력
    AppWeb->>AppServer: 로그인 요청
    AppServer->>Database: 사용자 정보 확인
    Database-->>AppServer: 사용자 정보 반환
    AppServer-->>AppWeb: 로그인 성공 응답
    AppWeb-->>User: 로그인 성공 화면 표시

    User->>AppWeb: 이체 정보 입력 (받는 사람, 금액 등)
    AppWeb->>AppServer: 이체 요청 (트랜잭션 시작)
    AppServer->>Database: 출금 계좌 잔액 확인
    Database-->>AppServer: 잔액 정보 반환

    alt 잔액 충분
        AppServer->>ExternalGateway: 이체 승인 요청 (외부 금융망 통신)
        ExternalGateway-->>AppServer: 이체 승인 응답
        AppServer->>Database: 출금 계좌 잔액 감소 및 이체 내역 기록
        AppServer->>Database: 입금 계좌 잔액 증가 및 이체 내역 기록
        Database-->>AppServer: DB 업데이트 완료 응답
        AppServer-->>AppWeb: 이체 성공 응답
        AppWeb-->>User: 이체 완료 화면 표시
    else 잔액 부족 또는 오류
        AppServer-->>AppWeb: 이체 실패 응답 (오류 메시지 포함)
        AppWeb-->>User: 이체 실패 화면 및 오류 메시지 표시
    end

    AppServer->>AppWeb: 트랜잭션 종료

위 코드로 시퀀스 다이어그램을 만들면 
![image](https://github.com/user-attachments/assets/f0bc0a2e-20b6-4abe-b329-392f2eee24b0)
위 사진과 같습니다.

시퀀스 다이어그램을 기반으로 코드를 만들었습니다. 

