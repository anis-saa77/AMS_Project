from config_conv_model import sendConvMessage
from config_conv_model import configConv
from pdf import create_pdf

historic = []
while True:
    message = input("Enter your message : ")
    if message == "exit":
        break
    historic.append(message)
    historic.append(sendConvMessage(message, "French", configConv))

create_pdf(historic)