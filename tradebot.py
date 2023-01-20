import openai
import re
import smtplib
import secrets

openai.api_key = "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"
name = input("What is your name? ")
email = input("What is your email? ")

from email.mime.text import MIMEText

def send_otp(email):
    otp = secrets.token_hex(6)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("madharatheghost@gmail.com", "zzbscbpchgdjdteh")
    message = f"Your OTP is: {otp} \nDescription: This OTP is to verify your email address for connecting to the bot."
    msg = MIMEText(message)
    msg['Subject'] = 'OTP for connecting to the bot'
    msg['From'] = 'madharatheghost@gmail.com'
    msg['To'] = email
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    return otp


# Verify OTP function
def verify_otp(otp_input):
    if otp_input == otp:
        return True
    else:
        return False

# Send OTP to email
otp = send_otp(email)

# OTP verification
otp_input = input("Enter the OTP received via email: ")
if not verify_otp(otp_input):
    print("Invalid OTP. Please try again.")
    exit()
else:
    print("OTP verified. You are now connected to the bot.")

def handle_message(message):
    match = re.search("write (\d+) poems", message, re.IGNORECASE)
    if match:
        num_poems = int(match.group(1))
        response = ""
        for i in range(num_poems):
            poem = openai.Completion.create(
                engine="text-davinci-002",
                prompt="Write a poem",
                temperature=0.7
            )
            response += poem["choices"][0]["text"] + "\n" if i != num_poems-1 else poem["choices"][0]["text"]
    elif re.search("hi|hello|hey|greetings", message, re.IGNORECASE):
        response = f"Hello {name}, How can I help you today?"
    else:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"chatbot: {message}",
            temperature=0.7
        )
        response = response["choices"][0]["text"]
    return response.strip()

# Main function to run the chatbot
def chatbot():
    user_input = input(f"{name} ")
    while user_input != "goodbye":
        print(f"Bot: {handle_message(user_input)}")
        user_input = input(f"{name} ")
    print(f"Bot: {handle_message(user_input)}")

# Run the chatbot
chatbot()
