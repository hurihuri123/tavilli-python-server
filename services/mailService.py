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
        self.connection = self.smtp_connect()

    def send_email(self, destinationMail, subject, email_body, body_type="html", attempts=0):
        # Set source/destination mails
        msg = MIMEMultipart()
        msg['From'] = str('Tavilli <%s>' % (self.sourceMail))
        msg['To'] = destinationMail
        msg['Subject'] = subject

        # Set mail body
        msg.attach(MIMEText(email_body, body_type))
        text = msg.as_string()

        try:
            self.connection.sendmail(self.sourceMail, destinationMail, text)
        except Exception as e:  # replace this with the appropriate SMTPLib exception
            # Overwrite the stale connection object with a new one
            if attempts > 5:
                print("sendTo error {}".format(e))
                # TODO: logger error + alert
                return
            self.connection = self.smtp_connect()
            self.send_email(destinationMail=destinationMail,
                            subject=subject, email_body=email_body, body_type=body_type, attempts=attempts + 1)

    def smtp_connect(self):
        smtpObj = None
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', self.clientPortForServer)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(
                self.sourceMail, password=self.sourceMailPassword)
        except Exception as e:
            print("SMTP Connect failed with {}".format(e))
            # TODO: logger error + alert
        return smtpObj
