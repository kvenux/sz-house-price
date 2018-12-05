from lxml import etree
import urllib.request
import re
import time

def grab_page(page):
    url = "https://app02.szmqs.gov.cn/0501W/Default.aspx?page=%s"%page
    print(url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}  
    req = urllib.request.Request(url=url, headers=headers)  
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    selector=etree.HTML(result, parser=None, base_url=None)
    companys = selector.xpath('//tr[@class="tab_body bd0"]/td[1]/text() | //tr[@class="tab_body bd1"]/td[1]/text()')
    properties = selector.xpath('//tr[@class="tab_body bd0"]/td[2]/text() | //tr[@class="tab_body bd1"]/td[2]/text()')
    locations = selector.xpath('//tr[@class="tab_body bd0"]/td[3]/text() | //tr[@class="tab_body bd1"]/td[3]/text()')
    districts = selector.xpath('//tr[@class="tab_body bd0"]/td[4]/text() | //tr[@class="tab_body bd1"]/td[4]/text()')
    id_list = selector.xpath('//tr[@class="tab_body bd0"]/td[5]/a/@val | //tr[@class="tab_body bd1"]/td[5]/a/@val')
    res = []
    for i in range(len(companys)):
        line = []
        line.append(companys[i])
        line.append(properties[i])
        line.append(locations[i])
        line.append(districts[i])
        line.append(id_list[i])
        newline = ','.join(line)
        res.append(newline)
    return res

outlines = []

for page in range(1,86):
    outlines += grab_page(page)
outline = '\n'.join(outlines)
with open("properties.csv", "w") as myfile:
    myfile.write(outline)
