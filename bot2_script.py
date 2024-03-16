import requests
import time
from telethon.sync import TelegramClient
import schedule

api_id = '26007220'
api_hash = '9e6b2de7da03127d66a199986afdd42b'

last_message = ""  # تتبع أخر رسالة تم إرسالها

def is_internet_available():
    try:
        r = requests.get("http://www.google.com", timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def send_latest_message():
    global last_message

    client = TelegramClient('session_name', api_id, api_hash)

    try:
        client.start()
        print("Connected to Telegram")

        phone_number = '213771282025'  # قم بتعيين رقم الهاتف الصحيح
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            code = input('Enter the code: ')
            client.sign_in(phone_number, code)

            # بمجرد أن تطلب منك كلمة المرور، قم بتوفيرها هنا
            password = input('Enter your password: ')
            client.sign_in(phone_number, code, password=password)

        # قم بتعيين هوية المستخدم الصحيحة بدلاً من "981635516"
        user_id = '@Agartha1200'
        channel_username = '@BLsAlerts'

        if is_internet_available():
            try:
                # احصل على رسائل القناة
                messages = client.get_messages(channel_username, limit=1)
                for message in messages:
                    # قارن الرسالة الجديدة بالرسالة الأخيرة
                    if message.text != last_message:
                        # إذا كانت مختلفة، قم بإرسالها وتحديث الرسالة الأخيرة
                        client.send_message(user_id, message.text)
                        last_message = message.text

            except Exception as e:
                print(f"Error: {e}")
        else:
            print("No internet connection. Skipping message sending.")

        client.disconnect()

    except Exception as e:
        print(f"Error: {e}")

def job():
    send_latest_message()

def main():
    # قم بتجدول تنفيذ الوظيفة كل عشر دقائق
    schedule.every(10).minutes.do(job)

    while True:
        schedule.run_pending()
        if not is_internet_available():
            print("No internet connection. Retrying in 1 minute.")
            time.sleep(60)
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()