import requests
import re

urls = ['http://www.mosigra.ru/']
mails =[]
deep=0
mainPage = 'http://www.mosigra.ru/'
print('Начало просмотра страниц')
def  findEmails (pUrl):
    print (pUrl)
    global urls
    global deep
    deep +=1
    page = requests.get(pUrl)
    if page.status_code == 200: 
        resUrl = re.findall('href="(.*?)"',page.text)
        resEmail = re.findall (r"[a-zA-Z0-9_.+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",page.text)
        NewUrls = list(set(resUrl))
        NewEmails = list(set(resEmail))
        for mail in NewEmails:
            mails.append(mail)
        if len(NewUrls) >0:
            for url in NewUrls:
                if url.find('mail') !=-1:
                    url = url[7:]
                    if url not in urls :
                        urls.append(url)
                elif len(url)>0  and url[0]=='#':
                    url='http://www.mosigra.ru/'+url
                    if url not in urls :
                        urls.append(url)
                elif url.find('pdf')!=-1 and url.find('jpg')!=-1:
                    if len(url)>0 and url[0] == '/':
                        url='http://www.mosigra.ru/'+url
                    if url not in urls :
                        urls.append(url)
                else:
                    if len(url)>0 and url[0] == '/':
                        url='http://www.mosigra.ru'+url     
                    if url not in urls:
                        urls.append(url)
                        if url[:18]=='http://www.mosigra' and deep<=3 and url.find('mode')==-1:
                            findEmails (url)
                            deep -=1
findEmails (mainPage)
print(' ')
print("Найденные e-mail'ы:")
mails= set(mails)
for i in mails:
    print (i)

