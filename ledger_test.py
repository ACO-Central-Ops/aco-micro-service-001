import os
import gspread
from google.oauth2.service_account import Credentials
import json
import datetime

# 権限の設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    print("CFO: 記帳業務を開始します...")
    
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_json:
        print("エラー: 認証情報（GOOGLE_APPLICATION_CREDENTIALS）が見つかりません。")
        return

    try:
        # 認証情報の読み込み
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        client = gspread.authorize(creds)

        # 【重要】スプレッドシートを開く
        # 名前が「ACO_Ledger」であることを確認してください
        spreadsheet_name = "ACO_Ledger"
        
        # 名前で開く（ここがエラーの温床でした）
        sh = client.open(spreadsheet_name)
        sheet = sh.get_worksheet(0) # 最初のシートを選択
        
        # 記帳内容の作成
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [now, "ACO System Check", "Operational", "Success"]
        
        # データの追加
        sheet.append_row(row)
        
        print(f"CFO: 記帳完了（{now}）- シート名: {spreadsheet_name}")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"エラー: '{spreadsheet_name}' という名前のスプレッドシートが見つかりません。")
        print("Googleドライブ上で名前が正しいか、サービスアカウントに共有されているか確認してください。")
    except Exception as e:
        print(f"実行中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
