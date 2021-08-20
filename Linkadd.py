# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests



global df,headers,receiver
headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
receiver="saurabhnehe2@gmail.com"
def main(receiver):
    try:
        df=pd.read_csv("links.csv")
    except:
        df= pd.DataFrame(columns=('Date','Product Name','Link','CurrentPrice','TargetPrice','ECOM site'))
    
    try:
        def add():
            global dt_obj,price,product,cprice,l
            def linkverify(link):
                 try:
                     global source,sitename
                     source=requests.get(link,headers=headers).content
                     if link[12:20]=='flipkart':
                        sitename="Flipkart"
                     elif link[12:18] == 'amazon':
                        sitename='Amazon'
                     else:
                        print("\nOnly Links From Flipkart and Amazon are supported")
                        return False
                     return True
                 except:
                     print("\nInvalid Link --Enter valid link")
                     return False
                 
            while True:         
                l=input("\nEnter the link\n")
                if linkverify(l)==True:
                    break 
                
            dt_obj=datetime.today().date()
            price=int(input("\nEnter Target Price of product\n"))
            soup=BeautifulSoup(source,'html.parser')
            
            if sitename=='Flipkart':
                product=soup.find('span',class_="B_NuCI").text.strip()
                stringg=soup.find('div',class_="_30jeq3 _16Jk6d").text.strip()[1:]
            else:
                """
                s=HTMLSession()
                r=s.get(l)
                r.html.render(sleep=1)
                product=r.html.xpath('//*[@id="priceblock_ourprice"]',first=True).text
                """
                product=soup.find('span',class_="a-size-large product-title-word-break").text.strip()
                stringg=soup.find('span',class_="a-size-medium a-color-price priceBlockBuyingPriceString").text.strip()
                stringg=stringg[2:-3]
            stringg="".join(stringg.split(","))
            cprice=int(stringg)
            print(cprice)
        
        
        while True:
            i=input("\n1.Add Product\n2.Change Receiver's mail\n3.Exit\n")
            if i=="1":
                add()
                df=df.append({'Date':dt_obj,'Product Name':product,'Link':l,'CurrentPrice':cprice,'TargetPrice':price,'ECOM site':sitename},ignore_index=True)
                print(df)
                df.to_csv("links.csv",index=False)
            elif i=="2":
                print("\nCurrent Receiver is:\n")
                print(receiver)
                receiver=input("\nEnter new valid receiver's email address\n")
            elif i=="3":
                break
            else:
                print("\nInvalid Option")
    
    except:
        print("\nproduct unavailable")

if __name__=="__main__":
    main(receiver)
    
    


