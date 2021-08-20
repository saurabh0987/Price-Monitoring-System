# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
from Linkadd import receiver

global headers
headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

def send_email(message,site):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('your mail id','your password')
    email=EmailMessage()
    email['From']="nehesaurabh3@gmail.com"
    print(receiver)
    email['To']=receiver
    email['Subject']="Regarding Price Drop of your product on {}".format(site)
    email.set_content(message)
    server.send_message(email)
    

try:
    df=pd.read_csv("links.csv")
except:
    pass 


def scrap(df):
    linklist=df.loc[:]['Link']
    targetlist=df.loc[:]['TargetPrice']
    
    ziplist=list(zip(linklist,targetlist))
    
    currentprice=[]
    
    for link,target in ziplist:
        source=requests.get(link,headers=headers).content
        soup=BeautifulSoup(source,'html.parser')
        if link[12:20]=='flipkart':
             site='Flipkart'
             stringg=soup.find('div',class_="_30jeq3 _16Jk6d").text.strip()[1:]
             product=soup.find('span',class_="B_NuCI").text.strip()
        elif link[12:18] == 'amazon':
             site="Amazon"
             product=soup.find('span',class_="a-size-large product-title-word-break").text.strip()
             stringg=soup.find('span',class_="a-size-medium a-color-price priceBlockBuyingPriceString").text.strip()
             stringg=stringg[2:-3]
        stringg="".join(stringg.split(","))
        cprice=int(stringg)
        if cprice<=target:
            print(target)
            message="Hello,\n       This is a price alert for your following product on {}:\nProduct Name:\n{}\n\nProduct Link:\n{}\n\nYour Trigger Price: {}\n\nCurrent Listed Price: {}".format(site,product,link,target,cprice)             
            send_email(message,site)
        currentprice.append(cprice)
    df['CurrentPrice']=currentprice
    df.to_csv('links.csv',index=False)
    
        
scrap(df)
    
        