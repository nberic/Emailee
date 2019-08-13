import smtplib, ssl
import sys, os

def send_email(email_properties):
	#smtp_host, smtp_port, sender_address, receiver_address, title
	try:
		smtp_host = email_properties["smtp_host"]
		smtp_port = int(email_properties["smtp_port"])
		sender_address = email_properties["sender_address"]
		sender_password = os.environ["EMAILEE_SENDER_PASSWORD"]
		receiver_address = email_properties["receiver_address"]
		title = email_properties["title"]
		message = f"Subject: { title }\n"
		with open("body.txt", "r") as f:
			message += ''.join(f.readlines())
	except FileNotFoundError:
		print("File 'text.txt' is not present in current directory.")
	except KeyError:
		print("You did not provide all required email properties.")
		print("Required email properties are: smtp_host, smtp_port, sender_address, receiver_address, and title.")
		print("Also, note that sender_password should be set as a system environment variable named 'EMAILEE_SENDER_PASSWORD'")
	except Exception as e:
		print("Unexpected error occured.")
		raise e
	else:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
			server.login(sender_address, sender_password)
			server.sendmail(sender_address, receiver_address, message)
		print(f"Successfully sent email to { receiver_address }.")

def read_email_properties():
	email_properties = {} 
	try:
		email_properties = { property.split('=')[0]: property.split('=')[1] for property in sys.argv[1:] }
	except IndexError as e:
		print(f"Email properties should be of form <property>=<value>, however { sys.argv[1:] } are provided.")
	
	return email_properties

if __name__ == "__main__":
	email_properties = read_email_properties()
	send_email(email_properties)	