import json
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
def main_handler(event, context):

    send_key = os.environ.get('send_key') # 设置的send_key
    my_sender = os.environ.get('my_sender')  # 发件人邮箱账号
    my_pass = os.environ.get('my_pass')  # 发件人邮箱密码
    my_user = os.environ.get('my_user')  # 收件人邮箱账号，我这边发送给自己
    mail_subject = event.get('queryString', {}).get('subject')  # 邮件的主题，也可以说是标题
    mail_body = event.get('body') # 邮件的正文
    get_send_key = event.get('queryString', {}).get('send_key')  # 请求的send_key

    print(event)

    def mail():
        ret = True
        try:
            msg = MIMEText(mail_body, 'plain', 'utf-8')
            msg['From'] = formataddr(["", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = mail_subject  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.mapxn.ml", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    # 验证send_key
    if get_send_key == send_key:
        ret = mail()
    else:
        ret = False
        print("send_key ERROR!")
    
    if ret:
        data = [ { 'responds' : "短信发送成功", '短信内容' : mail_subject, '邮件正文' : mail_body} ]
        body = json.dumps(data)
        print("Sms send success!")
        resp = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type":"application/json"},
            "body": body
        }
        return(resp)
        
    else:
        data = [ { 'responds' : "短信发送失败", '短信内容' : mail_subject, '邮件正文' : mail_body} ]
        body = json.dumps(data)
        resp = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type":"application/json"},
            "body": body
        }
        return(resp)
