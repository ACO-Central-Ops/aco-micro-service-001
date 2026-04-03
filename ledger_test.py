import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

# 1. 認証情報の読み込み (GitHub Secretsから)
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# GitHub Secretsに登録したJSONを読み込む
service_account_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
gc = gspread.authorize(creds)

# 2. スプレッドシートの操作
# 【重要】ここにスプレッドシートのIDを貼り付けてください
SPREADSHEET_ID = '1H3SkOr4hO_13Xyf0LTcOO1AVKWMddQW-sG5ng0geX1g'

def write_test_log():
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.get_range('A1').sheet # 最初のシートを選択
        
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        
        # 3. テストデータの書き込み (日時, 内容)
        row = [now, "GitHub Actionsからの自律記帳テスト成功", "0.01", "TEST_TX_ID"]
        worksheet.append_row(row)
        
        print(f"Successfully wrote to spreadsheet at {now}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    write_test_log()
