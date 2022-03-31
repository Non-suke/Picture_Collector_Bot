import os.path
import base64
import re
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import urllib.error
import urllib.request

def create_html_format(new_items):
    """Create html mail format
    Args:
        new_items:
        Return value of google_custum_search_API.find_new_image_and_update.
        List of dictionary.Each dict has 4 keys(page_url,image_url,title,search_date).

    Returns:
        string of html mail format.
    """
    
    msg_html = """
        <html>
            <head></head>
            <body>
                <h2 style="text-align:center">新しく見つかったシエラカップ</h2>
                <h3 style="text-align:center">画像をクリックすると掲載ページへジャンプします</h3>
        """

    for i in range(len(new_items)):
        #msg_text += new_items[i]["title"] + "\n" + new_items[i]["page_url"] + "\n\n"
        
        msg_html += "<p style='text-align:center'>" + new_items[i]["title"] + "</p>"
        
        msg_html += "<div style='text-align:cente'><a href=" + new_items[i]["page_url"] + ">"
        msg_html += "<p><image width = 300 src='cid:image" + str(i+1) + "'></p></a></div>"
        msg_html += "<p style='text-align:center'>" + new_items[i]["page_url"] + "</p>"
        
        
        msg_html += "<br>"

    msg_html += "</body></html>"
    
    return msg_html

def create_message(sender, to, subject, new_items):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        new_items:
        Return value of google_custum_search_API.find_new_image_and_update.
        List of dictionary.Each dict has 4 keys(page_url,image_url,title,search_date).

    Returns:
        An object containing a base64url encoded email object.
    """

    #create html format
    msg_html = """
        <html>
            <head></head>
            <body>
                <h2 style="text-align:center">新しく見つかったシエラカップ</h2>
                <h3 style="text-align:center">画像をクリックすると掲載ページへジャンプします</h3>
        """

    for i in range(len(new_items)):
        #msg_text += new_items[i]["title"] + "\n" + new_items[i]["page_url"] + "\n\n"
        
        msg_html += "<p style='text-align:center'>" + new_items[i]["title"] + "</p>"
        
        msg_html += "<div style='text-align:center'><a href=" + new_items[i]["page_url"] + ">"
        msg_html += "<p><img width = 300 src= cid:image" + str(i+1) + "></p></a></div>"
        msg_html += "<p style='text-align:center'>" + new_items[i]["page_url"] + "</p>"
        
        
        msg_html += "<br>"

    msg_html += "</body></html>"

    #create MIME object
    message = MIMEMultipart("related")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    message.attach(MIMEText(msg_html,"html"))

    for i in range(len(new_items)):
        _, ext = os.path.splitext(new_items[i]["image_url"])
        if re.search("jpeg|jpg|jpe|png",ext):
            try:
                with urllib.request.urlopen(new_items[i]["image_url"]) as web_file:
                    image_data = web_file.read()
            except urllib.error.URLError as e:
                print(e)
                with open("picture_not_found.jpg","rb") as f:
                    image_data = f.read()
        else:
            with open("picture_not_found.jpg","rb") as f:
                image_data = f.read()

        #TO DO:例外の処理が美しくない
        try:
            img = MIMEImage(image_data,_subtype = "jpeg")
        except:
            print('MIMEImage(image_data,_subtype = "jpeg"でエラー発生')
            print("image_urlは\n",new_items[i]["image_url"])

            #代わりの画像を用意
            with open("picture_not_found.jpg","rb") as f:
                image_data = f.read()
            img = MIMEImage(image_data,_subtype = "jpeg")

        img.add_header('Content-Id', '<image'+str(i+1)+'>')
        img.add_header('X-Attachment-Id', 'image'+str(i+1))
        img.add_header("Content-Disposition", "inline",filename = 'image'+str(i+1))
        img.add_header("Content-Transfer-Encoding","base64")
        message.attach(img)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(user_id, message,creds):
  """Send an email message.

  Args:
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    creds:GOOGLE_API_CREDS

  Returns:
    Sent Message.
  """
  try:
    service = build('gmail', 'v1', credentials=creds,cache_discovery=False)
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except HttpError as error:
    print ('An error occurred: %s' % error)

