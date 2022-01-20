import csv
import requests
from bs4 import BeautifulSoup
import os,glob
os.system('clear')

files = os.listdir('./') 
csvfiles = glob.glob('*.csv') 
if len(csvfiles) != 0 : 
  os.system('rm *.csv')

#-----알바몬에서 슈퍼브랜드 이름,링크
alba = requests.get("http://www.alba.co.kr")
alba = BeautifulSoup(alba.text,"html.parser")
company_dic={}
for a in alba.select('#MainSuperBrand > ul > li > a.goodsBox-info'):
    title_data = ''
    span = a.select('.company')
    for title in span:  
      title_data = title.text   
    company_dic[a] = {'company_name' :title_data,
                    'company_url':a["href"]}                
company_list = list(company_dic.values())

def extract_job(html):  
  title = html.find("td",{"class":"local first"})
  if title is not None : 
    title = html.find("td",{"class":"local first"}).get_text().replace(u'\xa0', u' ')

  place = html.find("span",{"class":"company"})
  if place is not None : 
    place = html.find("span",{"class":"company"}).get_text().replace(u'\xa0', u' ') 

  worktime = html.find("td",{"class":"data"})
  if worktime is not None : 
    worktime = html.find("td",{"class":"data"}).get_text()    

  pay = html.find("td",{"class":"pay"})
  if pay is not None : 
    pay = html.find("td",{"class":"pay"}).get_text() 
  
  lastdate =  html.find("td",{"class":"regDate last"})
  if lastdate is not None : 
    lastdate =  html.find("td",{"class":"regDate last"}).get_text()

  return {'place':place,'title': title,'time':worktime,'pay':pay,'date':lastdate}

#각슈퍼브랜드정보 불러와 각각 파일에저장
for company in company_list :
  f=open(f'{company["company_name"]}.csv'.replace('/',"_"), 'w')
  print(company["company_name"])
  wr = csv.writer(f)
  wr.writerow(['place','title','time','pay','date'])
  company = requests.get(company["company_url"])
  soup = BeautifulSoup(company.text,"html.parser")
  results = soup.select('#NormalInfo > table > tbody > tr')
  jobs = []
  i=0
  for result in results:  
    i += 1
    # 알바몬 일반직업정보가 홀수에만 정상임
    if i%2!=0:      
      job = extract_job(result)  
      wr.writerow(list(job.values()))    
      jobs.append(job)
  f.close()


#정답
# def write_company(company):
#     file = open(f"{company['name']}.csv", mode="w")
#     writer = csv.writer(file)
#     writer.writerow(["place", "title", "time", "pay", "date"])
#     for job in company["jobs"]:
#       writer.writerow(list(job.values()))
#     print(f"Completed....{company['name']}")


# alba_url = "http://www.alba.co.kr"

# alba_request = requests.get(alba_url)
# alba_soup = BeautifulSoup(alba_request.text, "html.parser")
# main = alba_soup.find("div", {"id": "MainSuperBrand"})
# brands = main.find_all("li", {"class": "impact"})
# for brand in brands:
#     link = brand.find("a", {"class": "goodsBox-info"})
#     name = brand.find("span", {"class": "company"})
#     if link and name:
#         link = link["href"]
#         name = name.text
#         if "/" in name :
#           name = name.replace("/"," ")
#         company = {'name': name, 'jobs': []}
#         jobs_request = requests.get(link)
#         jobs_soup = BeautifulSoup(jobs_request.text, "html.parser")
#         tbody = jobs_soup.find("div", {"id": "NormalInfo"}).find("tbody")
#         rows = tbody.find_all("tr", {"class": ""})
#         for row in rows:
#             local = row.find("td", {"class": "local"})
#             if local:
#                 local = local.text
#             title = row.find("td", {"class": "title"})
#             if title:
#                 title = title.find("a").find("span", {
#                     "class": "company"
#                 }).text.strip()

#             time = row.find("td", {"class": "data"})
#             if time:
#                 time = time.text
#             pay = row.find("td", {"class": "pay"})
#             if pay:
#                 pay = pay.text
#             date = row.find("td", {"class": "regDate"})
#             if date:
#                 date = date.text
#             job = {
#                 "place": local,
#                 "title": title,
#                 "time": time,
#                 "pay": pay,
#                 "date": date
#             }
#             company['jobs'].append(job)
#         write_company(company)