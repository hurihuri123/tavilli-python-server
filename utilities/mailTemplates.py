NEW_RELEVENT_MAIL_TITLE = "בקשות חדשות עבורך"


def new_relevent_template(url):
    return u"""\
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
