from flask import Flask, request, jsonify, render_template
import json
import requests
from requests.exceptions import RequestException

app = Flask(__name__)

## プロキシ認証情報を設定 ローカルデバッグ時
#proxies = {
#    "http": "http://sera:Ej3AR1MH,<@172.16.1.23:15080",
#    "https": "http://sera:Ej3AR1MH,<@172.16.1.23:15080"
#}

# APIの呼び出しURL
api_url = 'https://hekchat-api-managementservice.azure-api.net/openai/'


@app.route('/', methods=['GET'])
def index():  
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # リクエストからユーザーの入力メッセージを取得
    user_message = request.json['message']
    # デバッグ
    print("user_message:", user_message, ":", str(len(user_message)) )
    request_data = {
        "user_message": user_message
    }


    headers={
        "Content-Type": "application/json"
#        "Content-Type": "text/plain"
#        "Content-Type": "application/x-www-form-urlencoded"
#      , "Host": "hekchat-api-managementservice.azure-api.net"
     ,  "Ocp-Apim-Subscription-Key": "fa27b8cb5a3249bb93efe843fca26015"
    }

    try:
        # Azure APIManagementI APIにリクエストを送信
        response = requests.post(
            api_url
          , json=request_data
#          , data=user_message
#          , data="Please teach me highest japanese mountain"
          , headers=headers
#          , proxies=proxies  # プロキシを指定 ローカルデバッグ時
        )

        # デバッグ
        print("response:",response.text)

        # レスポンスから生成されたテキストを取得
#        generated_text = json.loads(response.text)
        generated_text = response.json()["choices"][0]["message"]["content"]

        # デバッグ
        print("generated_text:",generated_text)


        # レスポンスを返す
        return jsonify({'message': generated_text})

    except RequestException as e:
        # エラーメッセージを返す
        return jsonify({'message': 'エラーが発生しました、再度 入力をしてくださいね。'})

    except Exception as e:
        # エラーメッセージを返す
        return jsonify({'message': 'エラーが発生しました、再度 入力をしてくださいよ。'})

if __name__ == '__main__':
    app.run(debug=True)
