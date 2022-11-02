from logging import root
import urllib.request as req
import bs4 
import argparse
import csv

def parse_articles(url):
    request= req.Request(url,headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
    articles=root.find_all("div", class_="title")
    # nrecs=root.find_all("div", class_="nrec")
    # <div class="nrec"><span class="hl f1">爆</span></div>
    Ans=[]
    for element in articles:
        nrec=element.find_previous_sibling("div", class_="nrec")
        if element.a != None:
            # print("標題",element.a.string)
            if nrec.span!= None:
                # print("讚數" ,nrec.span.text)
                Ans.append({"title":element.a.string,"nrec":nrec.span.text})
    return Ans

def write_csv(data,fileName):
    fieldnames = ['title', 'nrec']

    with open('Crawler_Output/'+ fileName +'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def write_json(dict_in,fileName):
    dict_in
    import json
    with open('Crawler_Output/'+ fileName + '.json', 'w', encoding='utf-8') as file:
        json.dump(dict_in, file, ensure_ascii=False,indent=4)

parser = argparse.ArgumentParser()
# parser.add_argument("--verbosity", help="increase output verbosity")
# if args.verbosity:
#     print("verbosity turned on")
    
parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', metavar=('START_INDEX', 'END_INDEX'), type=int, nargs=2, help="Start and end index")
args, unknown = parser.parse_known_args()
url = "https://www.ptt.cc/bbs/"+args.b+"/index"

if args.i:
    start = args.i[0]
    if args.i[1] == -1:
        end = 1
    else:
        end = args.i[1]
data=[]
for element in range(args.i[0],args.i[1]+1):
    print("Page_" ,element, 'had been parsed')
    for dict_out in parse_articles(url+str(element)+".html"):
        data.append(dict_out)
write_csv(data,args.b + "_" +str(args.i[0])+"_"+str(args.i[1]))
write_json(data,args.b + "_" +str(args.i[0])+"_"+str(args.i[1]))
print("parse finished")
# url += args.i+".html"
#https://www.ptt.cc/bbs/graduate/search?q=%E5%8F%B0%E8%81%AF%E5%A4%A7

