from numpy import source
from pandas_datareader import data as web
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date as dt
import smtplib
import email as email

today = dt.today()
today = today.strftime("%d/%m/%Y")

def getDayCot(ticker):
    cot = web.DataReader(ticker, data_source='yahoo', start=today, end=today)
    cot.pop('Adj Close')
    cot.pop('Volume')
    cot['Difference'] = cot['Close'] - cot['Open']

    print(cot)
    return cot

#Example with actions of Petrobras and Google 
tickersName = {'PETR4.SA', 'GOGL34.SA'}

def emailBody(ticker):
    cot = getDayCot(ticker)
    high = float(cot['High'])
    low = float(cot['Low'])
    op = float(cot['Open'])
    cl = float(cot['Close'])
    dif = float(cot['Difference'])

    if(dif>0):
        text = f"Growth of {dif:.3f}"
    else:
        text = f"Drop of {dif:.3f}"
    
    return f"""
    <h1>TICKER:    {ticker}</h1>
    <h2>{text}</h2>
    <p><b>Close Value: {cl:.3f}</b></p>
    <p>Open Value: {op:.3f}</p>
    <p>Highest value: {high:.3f}</p>
    <p>Lowest value: {low:.3f}</p>
    </br>
    """
    
def sendEmail():  
    emailB = f""""""
    for tick in tickersName:
        emailB += emailBody(tick)
    msg = email.message.Message()
    msg['Subject'] = "Stock Exchange of "+str(today)
    msg['From'] = 'sender@email'
    msg['To'] = 'receiver@email'
    password = 'pass' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(str(emailB) )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email sent successfully')

sendEmail()