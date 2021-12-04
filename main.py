#!/usr/bin/env python
# -*-coding: utf-8-*-

import requests
import re

find=""
bookid=""

### init
method_find=input("按1书名搜索，按2图书ID搜索 ")
if method_find=="1":
  find=input("请输入图书名称: ")
elif method_find=="2":
  bookid=input("请输入图书ID: ")
else :
  print("输入错误!")

### url

bookname_url1 = "https://findcumt.libsp.com/find/unify/search"
bookname_url2 = "https://findcumt.libsp.com/find/unify/getPItemAndOnShelfCountAndDuxiuImageUrl"
bookid_url = "https://findcumt.libsp.com/find/physical/groupitems"

### headers

bookname_headers={
    "Host": "findcumt.libsp.com",
    "Connection": "keep-alive",
    "Content-Length": '510',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'groupCode': '200069',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'mappingPath': "",
    'x-lang': 'CHI',
    'sec-ch-ua-platform': "Windows",
    'Origin': 'https://findcumt.libsp.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://findcumt.libsp.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'SameSite=None',
}

bookid_headers={
  "Accept": "application/json, text/plain, */*",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9",
  "Connection": "keep-alive",
  "Content-Length": "72",
  "Content-Type": "application/json;charset=UTF-8",
  "Cookie": "SameSite=None",
  "groupCode": "200069",
  "Host": "findcumt.libsp.com",
  "mappingPath":"",
  "Origin": "https://findcumt.libsp.com",
  "Referer": "https://findcumt.libsp.com/",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "Windows",
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "same-origin",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
  "x-lang": "CHI"
}

bookname_headers2={
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "84",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "SameSite=None",
        "groupCode": "200069",
        "Host": "findcumt.libsp.com",
        'mappingPath': "",
        "Origin": "https://findcumt.libsp.com",
        "Referer": "https://findcumt.libsp.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "x-lang": "CHI"
}
#get data
  #data1
pagedata1='{"docCode": [null],"searchFieldContent":"'
pagedata2='","searchField": "keyWord","matchMode": "2","resourceType": [],"subject": [],"discode1": [],"publisher": [],"libCode": [],"locationId": [],"eCollectionIds": [],"curLocationId": [],"campusId": [],"kindNo": [],"collectionName": [],"author": [],"langCode": [],"countryCode": [],"publishBegin": null,"publishEnd": null,"coreInclude": [],"ddType": [],"verifyStatus": [],"group": [],"sortField": "relevance","sortClause": "asc","page":'
page=1
pagedata3=',"rows": 10,"onlyOnShelf": null,"searchItems": null,"keyWord": []}'
pagedata4=pagedata1+find+pagedata2

def json_dataGet(page):
  data=pagedata4+str(page)+pagedata3
  data=data.encode("utf-8")
  return data

image_data1='{"title": "'
image_data2='","isbn": "'
image_data3='","recordId": '
image_data4='}'

def imagedataGet(t,i,r):
  data=image_data1+str(t)+image_data2+str(i)+image_data3+str(r)+image_data4
  data=data.encode("utf-8")
  return data

  #data2
bookid_data1='{"page": 1,"rows": 20,"entrance": null,"recordId": "'
bookid_data2='","isUnify": true}'
bookid_data=bookid_data1+bookid+bookid_data2

### datalist
all_isbns=[]
all_publishers=[]
all_recordIds=[]
all_titles=[]
all_locations=[]
all_states=[]
all_codes=[]
all_pics=[]
all_counts=[]

### input
if method_find=="1":
  for i in range(1,10):
      json_data=json_dataGet(i)
      r = requests.post(bookname_url1,data=json_data,headers=bookname_headers)
      r = r.text
      if len(r)<2000 : 
        break
      all_title = re.findall('"title":"(.*?)"',r,re.S)
      all_recordId = re.findall('{"recordId":(.*?),"',r,re.S)
      all_publisher = re.findall('"publisher":"(.*?)"',r,re.S)
      all_isbn = re.findall('"isbn":"(.*?)"',r,re.S)
      all_titles+=all_title
      all_publishers+=all_publisher
      all_recordIds+=all_recordId
      all_isbns+=all_isbn
      for t,i,r in zip(all_title,all_isbn,all_recordId):
        imagedata=imagedataGet(t,i,r)
        # print(imagedata)
        imageGet=requests.post(bookname_url2,data=imagedata,headers=bookname_headers2)
        pic=imageGet.text
        # print(pic)
        all_pic=re.findall('"duxiuImageUrl":(.*?),',pic,re.S)
        # print(all_pics)
        all_count=re.findall('"onShelfCount":(.*?),',pic,re.S)
        all_pics+=all_pic
        all_counts+=all_count
elif method_find=="2":
  book=requests.post(bookid_url,data=bookid_data,headers=bookid_headers)
  book=book.text
  all_locations=re.findall('"locationName":"(.*?)"',book,re.S)
  all_codes=re.findall('"barcode":"(.*?)"',book,re.S)
  all_states=re.findall('"processType":"(.*?)"',book,re.S)

### output
if method_find=="1":
  with open("data.txt","w",encoding='utf-8') as file:
    for t,r,p,i,c,pic in zip(all_titles,all_recordIds,all_publishers,all_isbns,all_counts,all_pics):
      file.write("图书名称:"+t+" ")
      file.write("图书ID:"+r+" ")
      file.write("出版社:"+p+" ")
      file.write("isbn号:"+i+" ")
      file.write("馆藏数量:"+c+"\n")
      file.write("封面地址:"+pic+"\n")
  file.close()
elif method_find=="2":
  with open("data.txt","w",encoding='utf-8') as file:
    for t,r,p in zip(all_locations,all_codes,all_states):
      file.write("馆藏地:"+t+"\n")
      file.write("条码号:"+r+"\n")
      file.write("书刊状态:"+p+"\n"+"\n")
  file.close()