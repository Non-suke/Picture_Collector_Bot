import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(new_items):
    #CSVを開く

    #
    smtp_host = 'smtp.gmail.com'
    smtp_port = 465
    username = input("address:")
    password = input("password:")
    from_address = username
    to_address = username

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "新着シエラカップのお知らせ" #件名を入力
    msg['From'] = from_address
    msg['To'] = to_address

    if new_items:
        msg_text = "新しく見つかったシエラカップのリンク\n"
        msg_html = """
        <html>
            <head></head>
            <body>
                <h2 style="text-align:center">新しく見つかったシエラカップ</h2>
                <h3 style="text-align:center">画像をクリックするとリンクへジャンプします</h3>
        """

        for i in range(len(new_items)):
            msg_text += new_items[i]["title"] + "\n" + new_items[i]["page_url"] + "\n\n"
            
            msg_html += "<p style='text-align:center'>" + new_items[i]["title"] + "</p>"
            
            msg_html += "<p style='text-align:cente'><a href=" + new_items[i]["page_url"] + ">"
            msg_html += "<image width = 300 src=" + new_items[i]["image_url"] + "></a></p>"
            msg_html += "<p style='text-align:center'>" + new_items[i]["page_url"] + "</p>"
            
            
            msg_html += "<br>"

        msg_html += "</body></html>"


    msg.attach(MIMEText(msg_text, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))

    smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)
    #smtp.echo()
    smtp.login(username, password)
    result = smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.quit()

    del username, password, from_address, to_address,msg

if __name__ == "__main__":

    sample_items = [{'page_url':"https://www.store-campal.co.jp/products/detail.php?product_id=1854",
                'image_url':"https://www.store-campal.co.jp/upload/save_image/07080808_5d227b684e4ba.jpg",
                'title':"サンプル１",
                'search_date':"19900101"
                },
                {'page_url':"https://www.store-campal.co.jp/products/detail.php?product_id=4058",
                'image_url':"https://www.store-campal.co.jp/upload/save_image/03251732_5e7b17014ddcd.jpg",
                'title':"サンプル２",
                'search_date':"20000101"
                }]
    send_mail(sample_items)
    print("the email has been sent.")