import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Function to send the email
def send_email(sender_email, sender_password, receiver_email, subject, body, attachment):
    # Create a MIMEMultipart object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Handling file attachment
    if attachment:
        filename = os.path.basename(attachment)
        attachment_file = open(attachment, "rb")

        # Instance of MIMEBase and named as part
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_file.read())

        # Encode file in base64
        encoders.encode_base64(part)

        # Add header with file name
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        
        # Attach the instance 'part' to the message
        msg.attach(part)
        attachment_file.close()

    # Creating the SMTP session
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security

        # Authentication
        server.login(sender_email, sender_password)

        # Convert the message to string and send it
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f'Email sent to {receiver_email}')
    except Exception as e:
        print(f'Failed to send email: {str(e)}')
    finally:
        server.quit()

if __name__ == '__main__':
    # Get user input
    sender_email = input("Enter your email address: ")
    sender_password = input("Enter your email password: ")
    receiver_email = input("Enter recipient's email address: ")
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    attachment = input("Enter the file path of the attachment (or press Enter to skip): ")
    
    # If the user doesn't provide an attachment path, set it to None
    if attachment.strip() == "":
        attachment = None

    # Send the email
    send_email(sender_email, sender_password, receiver_email, subject, body, attachment)

