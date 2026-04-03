import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

# 認証スコープ
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# スプレッドシートID
SPREADSHEET_ID = '1H3SkOr4hO_13Xyf0LTcOO1AVKWMddQW-sG5ng0geX1g'

def write_test_log():
    try:
        print("1. 認証を開始します...")
        creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_json:
            print("エラー: Secretが見つかりません。")
            return
            
        service_account_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        gc = gspread.authorize(creds)
        print("2. 認証成功。")

        print(f"3. スプレッドシートを開きます...")
        sh = gc.open_by_key(SPREADSHEET_ID)
        
        # 【修正ポイント】最初のワークシートを正しく取得
        worksheet = sh.get_worksheet(0)
        print(f"4. シート '{worksheet.title}' を捕捉しました。")
        
        # 日本時間で記録
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        row = [now, "GitHub Actionsからの自律記帳テスト成功", "0.01", "SUCCESS"]
        
        print(f"5. データを書き込みます: {row}")
        # 【修正ポイント】append_row メソッドを使用
        worksheet.append_row(row)
        print(f"6. 書き込み完了！ 日時: {now}")

    except Exception as e:
        print(f"❌ エラー発生詳細: {e}")
        raise e

if __name__ == "__main__":
    write_test_log()
