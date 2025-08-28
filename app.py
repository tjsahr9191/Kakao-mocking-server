from time import sleep

from flask import Flask, jsonify, request, render_template
import datetime
import uuid

# Flask 애플리케이션 생성
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test_page():
    return render_template('test.html')


# '/ready' 엔드포인트에 POST 요청을 처리하는 함수
@app.route('/ready', methods=['POST'])
def kakao_pay_ready_mock():

    sleep(0.005)

    """
    Java 클라이언트의 카카오페이 결제 준비(POST /ready) 요청을 받아
    KakaoPayReadyResponse 형태의 Mock JSON 데이터를 반환합니다.
    """
    # 요청 본문을 JSON으로 파싱 (디버깅이나 로깅 시 유용)
    # received_data = request.get_json()
    # print(f"[/ready] 요청 수신: {received_data}")

    # 응답으로 보낼 고유한 Mock 데이터 생성
    tid = f"T{uuid.uuid4().hex[:20]}"  # T로 시작하는 임의의 거래 ID
    mock_url_path = f"mock-payment/{uuid.uuid4().hex}"

    # KakaoPayReadyResponse DTO와 동일한 구조의 Python 딕셔너리 생성
    response_data = {
        "tid": tid,
        "next_redirect_pc_url": f"http://localhost:8000/{mock_url_path}",
        "next_redirect_mobile_url": f"http://localhost:8000/{mock_url_path}",
        "next_redirect_app_url": f"mock-app-scheme://{mock_url_path}",
        "android_app_scheme": f"mock-android-scheme://{mock_url_path}",
        "ios_app_scheme": f"mock-ios-scheme://{mock_url_path}",
        "created_at": datetime.datetime.now().isoformat()
    }

    # 딕셔너리를 JSON 형태로 변환하여 반환
    return jsonify(response_data)


# 이 스크립트가 직접 실행될 때 Flask 서버를 시작
if __name__ == '__main__':
    # host='0.0.0.0'는 외부에서도 접속 가능하게 합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)