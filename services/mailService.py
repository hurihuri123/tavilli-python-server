import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class MailService:
    def __init__(self, sourceMail, sourceMailPassword):
        self.sourceMail = sourceMail
        self.sourceMailPassword = sourceMailPassword
        self.clientPortForServer = 587

    def send_mail(self, server, destinationMail, subject, mailBody, body_type):
        # Set source/destination mails
        msg = MIMEMultipart()
        msg['From'] = str('Tavilli <%s>' % (self.sourceMail))
        msg['To'] = destinationMail

        msg['Subject'] = subject

        # Set mail body
        msg.attach(MIMEText(mailBody, body_type))

        # Send the mail
        text = msg.as_string()

        server.sendmail(self.sourceMail, destinationMail, text)
        print("Mail was successfully sent to %s" % destinationMail)

    def send_mail_relevant_request(self, destinationMails, url):
        server = smtplib.SMTP('smtp.gmail.com', self.clientPortForServer)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sourceMail, self.sourceMailPassword)
        html = u"""\
				<html>
				  <head></head>
				  <body dir="rtl">
					<p>היי !<br>
					   מאז התחברותך האחרונה התפרסמו בקשות חדשות אשר רלוונטיות עבורך.  <br>
					לחצ/י על <a href="%s">הקישור</a> הנ"ל לצפייה.
					</p>
				  </body>
				</html>
				""" % (url)
        for mail in destinationMails:
            self.send_mail(server, mail, "בקשות חדשות עבורך", html, "html")
        server.quit()
