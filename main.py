import keyring
from google_API_credential import get_credential
from google_custum_search_API import search_image,find_new_image_and_update
from gmail_API import create_html_format,create_message,send_message

def main():
    NAMESPACE = "Picture_Collector_Bot"
    GOOGLE_API_CREDS = get_credential()
    CUSTOM_SEARCH_ENGINE_ID = keyring.get_password(NAMESPACE,"CUSTOM_SEARCH_ENGINE_ID")
    MY_MAIL_ADDRESS = keyring.get_password(NAMESPACE,"MY_MAIL_ADDRESS")
    RECEIVER_MAIL_ADDRESS = keyring.get_password(NAMESPACE,"RECEIVER_MAIL_ADDRESS")

    search_words = ['sierra cup','シエラカップ',"シェラカップ"]
    mail_subject = "新着シエラカップのお知らせ"

    search_result = []
    for q in search_words:
        search_result += search_image(q,GOOGLE_API_CREDS,CUSTOM_SEARCH_ENGINE_ID,page_limit = 10)

    new_items = find_new_image_and_update(search_result)

    if new_items:
        message = create_message(MY_MAIL_ADDRESS,RECEIVER_MAIL_ADDRESS,mail_subject,new_items)
        send_message(MY_MAIL_ADDRESS,message,GOOGLE_API_CREDS)
        print("The email has been sent.")
    else:
        print("No new items found.")

    del GOOGLE_API_CREDS,CUSTOM_SEARCH_ENGINE_ID,MY_MAIL_ADDRESS,RECEIVER_MAIL_ADDRESS


if __name__ == '__main__':
    main()


    

