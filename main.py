import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")

#-----알바몬 슈퍼브랜드 이름,링크
alba = requests.get("http://www.alba.co.kr")
alba = BeautifulSoup(alba.text,"html.parser")

companyList={}
for a in alba.select('#MainSuperBrand > ul > li > a.goodsBox-info'):
    title_data = ''
    span = a.select('.company')
    for title in span:  
      title_data = title.text   
    companyList[a] = {'title' :title_data,
                    'companyList':a["href"]}
                

dfdf
AlIST = list(companyList.values())

for company in AlIST :
  print(company['title'])
  file=open(f'{company["title"]}.csv'.replace("/","_"), mode='w')
  writer = csv.writer(file)
  #writer.writerow(["place","title","time","pay","date"])




  # save_to_file(company)












