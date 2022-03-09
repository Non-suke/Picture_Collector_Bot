import os.path
import base64
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        
        msg_html += "<p style='text-align:cente'><a href=" + new_items[i]["page_url"] + ">"
        msg_html += "<image width = 300 src=" + new_items[i]["image_url"] + "></a></p>"
        msg_html += "<p style='text-align:center'>" + new_items[i]["page_url"] + "</p>"
        
        
        msg_html += "<br>"

    msg_html += "</body></html>"
    
    return msg_html

def create_message(sender, to, subject, msg_html):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        msg_html:The html of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    
    message = MIMEText(msg_html,"html")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
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

