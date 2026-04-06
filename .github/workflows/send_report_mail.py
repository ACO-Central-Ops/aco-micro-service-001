import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(content):
    # GitHub Secretsから認証情報を取得
    sender_email = os.environ.get('MAIL_ADDRESS')
    sender_password = os.environ.get('MAIL_PASSWORD')
    receiver_email = "cliaraiz23@gmail.com"

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header('【ACO定例報告】システム稼働状況', 'utf-8')
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ メール送信に成功しました。")
    except Exception as e:
        print(f"❌ メール送信エラー: {e}")

if __name__ == "__main__":
    # 前段のレポート生成と連携
    from aco_ops_manager import generate_coo_report
    report_text = generate_coo_report()
    send_email(report_text)
