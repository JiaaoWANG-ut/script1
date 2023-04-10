import smtplib
from email.header import Header
from email.mime.text import MIMEText


def email(text):
    # 发送方设置
    mail_host = "smtp.exmail.qq.com"
    mail_user = "shenglin@aleeqaq.cc"
    mail_pass = "89JZCRp6XA4RQsBz"
    # 接收方账号
    receiver_mail = 'wangjiaao0720@utexas.edu'
    # 从msg文件读取内容：只读取第一行！！！
    raw_text = text
    # 邮件内容设置
    msg = MIMEText(raw_text, 'plain', 'utf-8')
    msg['From'] = Header('Shenglin,Xu')
    msg['To'] = Header('Xu,Shenglin')
    msg['Subject'] = Header('Longstar6 Service')
    # 建立连接并发送
    server = smtplib.SMTP_SSL(mail_host)
    server.connect(mail_host, 465)
    server.login(mail_user, mail_pass)
    server.sendmail(mail_user, receiver_mail, msg.as_string())
    server.quit()

email("fuck")
