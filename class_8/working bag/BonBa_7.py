import jieba
import jieba.analyse
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
from scipy.ndimage import gaussian_gradient_magnitude
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from wordcloud import WordCloud

# -----------------------分析區-----------------------------
driver = webdriver.Chrome()
driver.get("https://www.youtube.com") # 更改網址以前往不同網頁
# time.sleep(4)
# arrow = driver.find_element(By.XPATH,'//yt-formatted-string[@id="video-title" and @class="style-scope ytd-rich-grid-media"]')
# arrow.click()
# time.sleep(4)
#<a id="video-title-link" class="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media" aria-label="沙國王儲拒見拜登下不了台？天舟對接天宮2小時世界紀錄 新聞大白話 20221113 上傳者：新聞大白話 37 分鐘前 18 分鐘 觀看次數：16,926次" title="沙國王儲拒見拜登下不了台？天舟對接天宮2小時世界紀錄 新聞大白話 20221113" href="/watch?v=gzz5xk781cQ">
#   <yt-formatted-string id="video-title" class="style-scope ytd-rich-grid-media" aria-label="沙國王儲拒見拜登下不了台？天舟對接天宮2小時世界紀錄 新聞大白話 20221113 上傳者：新聞大白話 37 分鐘前 18 分鐘 觀看次數：16,926次">
#       沙國王儲拒見拜登下不了台？天舟對接天宮2小時世界紀錄 新聞大白話 20221113
#   </yt-formatted-string>
# </a>
arrow = driver.find_elements(By.XPATH,'//a[@id="video-title-link" and @class="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media"]')
for try_num in range(random.randint(0,10),20):
    try:
        arrow[try_num].click()
        break
    except:
        continue
try_num = 0
titles=""
for target in range(0,200):
    time.sleep(5)
    arrow = driver.find_elements(By.XPATH,'//span[@id="video-title" and @class=" style-scope ytd-compact-video-renderer"]')
    title_Now=driver.title
    print("title_Now = " + title_Now) 
    if " | 老高與小茉 Mr & Mrs Gao - YouTube" in title_Now:
        title_Now=title_Now.replace("| 老高與小茉 Mr & Mrs Gao - YouTube","")
    title_Now=title_Now.replace(" - YouTube","")
    print("arrow[0].text = " + arrow[0].text)
    if title_Now in titles:
        for try_num in range(random.randint(0,10),20):
            try:
                arrow[try_num].click()
                break
            except:
                continue
        try_num=0
    else:
        titles+=(title_Now + '\n')
    # arrow = driver.find_element(By.XPATH,'//yt-formatted-string[@id="video-title" and @class="style-scope ytd-rich-grid-media"]')
    for try_num in range(0,20):
        try:
            arrow[try_num].click()
            break
        except:
            continue
    try_num=0
driver.close() # 關閉瀏覽器視窗

# --------------------存檔區-------------------------
path = 'Title_Output.txt'
f = open(path, 'w',encoding="utf-8")
f.write(titles)
f.close()

jieba.set_dictionary('dict.txt.big')
jieba.load_userdict("userdict.txt")
# sentence = open('lyric_tw.txt', 'rb').read()
# print ("Input：", sentence)
words = jieba.cut(titles, cut_all=False)
# print ("Output 精確模式 Full Mode："),
Output=[]
Output_D={}
for word in words:
    if(word!=' ' and word!='\n'and word!='的'):
        print("word = " +word)
        Output.append(word)
        
for element in Output:
    if(element!=' '):
        Output_D.update({element:Output.count(element)})

print("sorted(Output_D.values()) = " )
print(sorted(Output_D.items(),key=lambda x:x[1],reverse=True))

# Serializing json
json_object = json.dumps((dict(sorted(Output_D.items(),key=lambda x:x[1],reverse=True))), indent=4,ensure_ascii=False)
# Writing to sample.json
with open("sample.json", "w",encoding="utf-8") as outfile:
    outfile.write(json_object)

path = 'JSON_Output.txt'
f = open(path, 'w',encoding="utf-8")
f.write((str)(dict(sorted(Output_D.items(),key=lambda x:x[1],reverse=True))))
f.close()
# ----------------------製圖區------------------------
txtfile = "Title_Output.txt" # 剛才下載存的文字檔
text = open(txtfile,"r",encoding="utf-8").read()


# Tokenize
text = ' '.join(jieba.cut(text))


# Mask image
mask_color = np.array(Image.open('parrot-by-jose-mari-gimenez.jpg'))
mask_color = mask_color[::3, ::3]
mask_image = mask_color.copy()
mask_image[mask_image.sum(axis=2) == 0] = 255


# Edge detection
edges = np.mean([gaussian_gradient_magnitude(mask_color[:, :, i]/255., 2) for i in range(3)], axis=0)
mask_image[edges > .08] = 255


# WordCloud
wc = WordCloud(max_words=2000,mask=mask_image,font_path='JOJO.TTC',max_font_size=40,random_state=42,relative_scaling=0)

wc.generate(text)


# Plot
plt.figure()
plt.axis('off')
plt.imshow(wc)
plt.show()