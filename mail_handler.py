import smtplib

def send_mail():
    #CSVを開く

    #
    smtp_host = 'smtp.gmail.com'
    smtp_port = 465
    username = input("adress")
    password = input("pass")
    from_address = username
    to_address = username
    subject = 'test subject'
    body = 'test body'
    message = ("From: %srnTo: %srnSubject: %srnrn%s" % (from_address, to_address, subject, body))

    smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)
    smtp.login(username, password)
    result = smtp.sendmail(from_address, to_address, message)
    print(result)

send_mail()
print("Hello World")