"""Import thư viện"""
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

"""Khai báo một số thông số để gửi email
Lưu ý thay đổi tên và password email, mở chức năng sử dụng email ở máy khác"""
host = "smtp.gmail.com"
port = 587
username = "vietkhoi1221@gmail.com"
password = "khoidk00"
from_email = username
to_list = ["vietkhoi1221@gmail.com"]
subject = '     '


class MessageUser():
    user_details = []
    messages = []
    email_messages = []
    base_message = """Hi {name}! 
    Vào lúc: {date} 
    Nhịp tim là: {nhiptim} và nồng độ oxi trong máu là: {oxi} %
"""
    def add_user(self, name, nhiptim, oxi, sub, email=None):
        global subject
        subject = sub
        detail = {
            "name":name,
            "nhiptim": nhiptim,
            "oxi": oxi,
        } 
        today = datetime.date.today()
        date_text = '{today.day}/{today.month}/{today.year}'.format(today=today)
        detail['date'] = date_text
        if email is not None: # if email != None
            detail["email"] = email
        self.user_details.append(detail)
    def get_details(self):
        return self.user_details
    def make_messages(self):
        if len(self.user_details) > 0:
            for detail in self.get_details():
                name = detail["name"]
                nhiptim = detail["nhiptim"]
                oxi = detail["oxi"]
                date = detail["date"]
                message = self.base_message
                new_msg = message.format(
                    name=name,
                    date=date,
                    nhiptim = nhiptim,
                    oxi = oxi
                )
                user_email = detail.get("email")
                if user_email:
                    user_data = {
                        "email": user_email,
                        "message": new_msg
                    }
                    self.email_messages.append(user_data)
                else:
                    self.messages.append(new_msg)
            return self.messages
        return []
    def send_email(self, sub= None):
        self.make_messages()
        if len(self.email_messages) > 0:
            for detail in self.email_messages:
                user_email = detail['email']
                user_message = detail['message']
                try:
                    email_conn = smtplib.SMTP(host, port)
                    email_conn.ehlo()
                    email_conn.starttls()
                    email_conn.login(username, password)
                    the_msg = MIMEMultipart("alternative")
                    the_msg['Subject'] = subject
                    the_msg["From"] = from_email
                    the_msg["To"]  = user_email
                    part_1 = MIMEText(user_message, 'plain')
                    the_msg.attach(part_1)
                    email_conn.sendmail(from_email, user_email, the_msg.as_string())
                    email_conn.quit()
                except smtplib.SMTPException:
                    print("Lỗi gửi email")
            return True
        return False


obj = MessageUser()