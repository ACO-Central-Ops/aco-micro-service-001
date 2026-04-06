import os
import gspread
from google.oauth2.service_account import Credentials
import json

# 権限の設定（ここが修正ポイントです）
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    print("CFO: 記帳業務を開始します...")
    
    # 環境変数から認証情報を取得
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_json:
        print("エラー: 認証情報（GOOGLE_APPLICATION_CREDENTIALS）が見つかりません。")
        return

    try:
        # JSON文字列を辞書形式に変換して認証
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        client = gspread.authorize(creds)

        # スプレッドシートを開く（名前が「ACO_Ledger」であることを想定）
        # もし名前が違う場合は、ここを書き換えてください
        sheet = client.open("ACO_Ledger").sheet1
        
        # テスト記帳
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([now, "ACO System Check", "Success", "0"])
        
        print(f"CFO: 記帳完了（{now}）")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
