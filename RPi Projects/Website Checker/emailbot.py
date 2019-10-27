import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(*WebsiteURL):
    sbj = 'Insert_Subject'
    # set from address
    fromaddr = 'Insert_from_address@your-email.com'
    # multiple toaddr to send multiple emails
    toaddr1 = 'Insert_to_address@their-email.com'
    toaddr2 = 'Insert_another_to_address@their-email.com'

    email_body = None
    email_body_content = ' '
    if WebsiteURL[0] is not None:
        email_body_content += ' ' + str(WebsiteURL[0])
    elif WebsiteURL[1] is not None:
        email_body_content += ' ' + str(WebsiteURL[1])

    email_body_footer = ' '
    email_body_footer = email_body_footer + '<br><br><br>Yours truly,'
    email_body_footer = email_body_footer + '<br>Insert_Your_Name<br>'

    email_body = str(email_body_content) + str(email_body_footer)

    message = MIMEMultipart('alternative')
    message['From'] = fromaddr
    message['To'] = toaddr1
    message['Subject'] = sbj
    body = email_body
    message.attach(MIMEText(body, 'html'))

    # setup the email server, for gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    content = message.as_string()
    server.starttls()
    # add account login name and password
    server.ehlo()
    server.login("Insert_from_address@your-email.com", "your_password")

    # send the email
    server.sendmail(fromaddr, toaddr1, content)
    server.sendmail(fromaddr, toaddr2, content)
    # disconnect from the server
    server.quit()
