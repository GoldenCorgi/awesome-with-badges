import urllib.request
from tqdm import tqdm
from urllib.request import Request, urlopen
import json
import os.path

def downloadReadme(URL) -> str:
    response = urllib.request.urlopen(URL)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    return text

def replaceLocalSrcWithOriginalGitHubLink(text, URL) -> str:
    URLImageReplacementList = URL.split("https://raw.githubusercontent.com/")[1].split("/")
    URLImageReplacementList.insert(2,"raw")
    URLImageReplacementString = "https://github.com/"+"/".join(URLImageReplacementList[:-1]) + "/"


    y = text.split('src="')
    for i in y:
        url = i.split('"')[0]
        if "https://" in url:
            continue
        if "http://" in url:
            continue
        else:
            text = text.replace('src="' + url +'"', 'src="' + URLImageReplacementString+url +'"')
    return text

def getListOfGithubLinks(text) -> list:
    listpog=[]
    y = text.split("(")
    for i in y:
        url = i.split(")")[0]
        if "github.com" in url:
            listpog.append(url)
    return listpog

def removeDuplicateOfIndex(list2d, index=1) -> list:
    tmpDup = []
    newlist = []
    for i in list2d:
        if i[index] in tmpDup:
            continue
        else:
            newlist.append(i)
            tmpDup.append(i[index])
    return newlist


def straightUpPoggers(main_url):
    # URL = "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md"

    
    # choose master or main? hmm
    mainOrMaster = "master"
    URL = f"https://raw.githubusercontent.com/{main_url}/{mainOrMaster}/README.md"
    text = downloadReadme(URL)

    text = replaceLocalSrcWithOriginalGitHubLink(text, URL)

    listpog = getListOfGithubLinks(text)

    listpog2 = []

    # dangerous magic happens below wtf
    divider = "["
    verypog = text.split(divider)
    for url in listpog:

        for i,x in enumerate(verypog):
            
            if url in x:
                if "#" in url:
                    url = url.split("#")[0]
                newurl = url.split("github.com/")[1]
                if newurl[-1] == "/":
                    newurl = newurl[:-1]
                listpog2.append([x.split("]")[0],newurl])
                fullbadge = f"[![GitHub stars](https://img.shields.io/github/stars/{newurl}.svg)](https://GitHub.com/{newurl}/stargazers/)"
                # print(fullbadge+" "+x)
                oldtext = text
                text = text.replace(divider+x,fullbadge+" "+divider+x)
                # print(x,fullbadge+" "+x)


    listpog2 = removeDuplicateOfIndex(listpog2, index=1)

    strx = ""
    strx = strx + """  <tr style="text-align:center;">
        <th>Repo Name</th>
        <th>Links</th>
        <th>Description</th>
        <th>Stars</th>
    </tr>"""

    # listpog2 = listpog2[:3]

    for i in tqdm(listpog2):
        newurl = i[1]
        
        urlWithUnderscore = newurl.replace("/","_")
        i.append(0)
        file_path = f"badges/stars/{urlWithUnderscore}.svg"
        if os.path.exists(file_path):
            with open(f"badges/stars/{urlWithUnderscore}.svg","r",encoding="utf-8") as f:
                text = f.read()
        else:
            req = Request(f"https://img.shields.io/github/stars/{newurl}.svg", headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()

            # response = urllib.request.urlopen(f"https://img.shields.io/github/stars/{newurl}.svg",header=hdr)
            # data = response.read()      # a `bytes` object
            text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        for x in text.split(">"):
            if "</text" in x:
                newX = x.replace("</text","")
                if newX != "stars":
                    
                    try:
                        if ("k") in newX:
                            newX = float(newX[:-1])*1000
                        i[2] = int(newX)
                    except:
                        pass

        with open(f"badges/stars/{urlWithUnderscore}.svg","w",encoding="utf-8") as f:
            f.write(text)
    
    # STRAIGHTUP POGGERS!! SAVED SHIT
    urlWithUnderscore = main_url.replace("/","_")
    with open(f'List_{urlWithUnderscore}.json', 'w') as filehandle:
        json.dump(listpog2, filehandle)

    listpog2.sort(key=lambda x:x[2],reverse=True)
    for i in tqdm(listpog2):
        badge = ""
        try:
            title = i[1].split("/")[1]
        except:
            print("Error at ",i)
            continue
        desc = i[0]
        newurl = i[1]
        urlWithUnderscore = newurl.replace("/","_")
        originalURL = f"https://github.com/{i[1]}"
        # badge = f"[![GitHub stars](https://img.shields.io/github/stars/.svg)](https://GitHub.com/{newurl}/stargazers/)"
        badgeURL = f"awesome/{urlWithUnderscore}.md"
        strx = strx + f"""<!-- ** {title} -->
    <tr>
        <td rowspan="2"><b><p style="display:inline-block;" ><div style='vertical-align:middle; display:inline;'>{title}</div></p></b></td>
        <td rowspan="2"><a href="{originalURL}">original</a></td>
        <td rowspan="2">{desc}</a></td>
        <td rowspan="2"><a href="https://GitHub.com/{newurl}/stargazers/">
        <img src="../badges/stars/{urlWithUnderscore}.svg" alt="Logo" ></a></td>
    </tr>
    <tr>
    </tr>
    """
    newText = f"""<p align="center">
  <a href="https://github.com/goldencorgi/awesome-with-badges">
    <img src="../images/daftpunkpoggers.png" alt="Logo" >
  </a>
  <p align="center">"i only date people with repos that have > 1k stars"</p>

  <h2 align="center">{main_url}</h2>

</p>
""" + '<table style="max-width:100%;table-layout:auto;">' + strx + "</table>"
    
    
    urlWithUnderscore = main_url.replace("/","_")
    with open(f"awesome/{urlWithUnderscore}.md","w") as f:
        f.write(newText)



straightUpPoggers("onurakpolat/awesome-analytics")


input("-")

# URL = "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md"
URL = "https://raw.githubusercontent.com/bayandin/awesome-awesomeness/master/README.md"

URLImageReplacementList = URL.split("https://raw.githubusercontent.com/")[1].split("/")
URLImageReplacementList.insert(2,"raw")
URLImageReplacementString = "https://github.com/"+"/".join(URLImageReplacementList[:-1]) + "/"
response = urllib.request.urlopen(URL)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

# [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
# [![HitCount](http://hits.dwyl.io/Naereen/badges.svg)](http://hits.dwyl.io/Naereen/badges)
# [![GitHub stars](https://img.shields.io/github/stars/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/stargazers/)

y = text.split('src="')
for i in y:
    url = i.split('"')[0]
    if "https://" in url:
        continue
    if "http://" in url:
        continue
    else:
        text = text.replace('src="' + url +'"', 'src="' + URLImageReplacementString+url +'"')


listpog=[]
y = text.split("(")
for i in y:
    url = i.split(")")[0]
    if "github.com" in url:
        listpog.append(url)

listpog2 = []

divider = "["
verypog = text.split(divider)
for url in listpog:

    for i,x in enumerate(verypog):
        
        if url in x:
            if "#" in url:
                url = url.split("#")[0]
            newurl = url.split("github.com/")[1]
            if newurl[-1] == "/":
                newurl = newurl[:-1]
            listpog2.append([x.split("]")[0],newurl])
            fullbadge = f"[![GitHub stars](https://img.shields.io/github/stars/{newurl}.svg)](https://GitHub.com/{newurl}/stargazers/)"
            # print(fullbadge+" "+x)
            oldtext = text
            text = text.replace(divider+x,fullbadge+" "+divider+x)
            # print(x,fullbadge+" "+x)
listpog2 = removeDuplicateOfIndex(listpog2, index=1)

with open('ListOfAwesome.json', 'w') as filehandle:
    json.dump(listpog2, filehandle)

strx = ""
strx = strx + """  <tr style="text-align:center;">
    <th>Repo Name</th>
    <th>Links</th>
    <th>Description</th>
    <th>Stars</th>
  </tr>"""

# listpog2 = listpog2[:3]

for i in tqdm(listpog2):
    newurl = i[1]
    urlWithUnderscore = newurl.replace("/","_")

    i.append(0)
    req = Request(f"https://img.shields.io/github/stars/{newurl}.svg", headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()

    # response = urllib.request.urlopen(f"https://img.shields.io/github/stars/{newurl}.svg",header=hdr)
    # data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    for x in text.split(">"):
        if "</text" in x:
            newX = x.replace("</text","")
            if newX != "stars":
                
                try:
                    if ("k") in newX:
                        newX = float(newX[:-1])*1000
                    i[2] = int(newX)
                except:
                    pass

    with open(f"badges/stars/{urlWithUnderscore}.svg","w",encoding="utf-8") as f:
        f.write(text)

listpog2.sort(key=lambda x:x[2],reverse=True)
for i in tqdm(listpog2):
    badge = ""
    title = i[1].split("/")[1]
    desc = i[0]
    newurl = i[1]
    urlWithUnderscore = newurl.replace("/","_")
    originalURL = f"https://github.com/{i[1]}"
    # badge = f"[![GitHub stars](https://img.shields.io/github/stars/.svg)](https://GitHub.com/{newurl}/stargazers/)"
    badgeURL = f"awesome/{urlWithUnderscore}.md"
    strx = strx + f"""
      <!-- ** {title} -->
  <tr>
    <td rowspan="2"><b><p style="display:inline-block;" ><div style='vertical-align:middle; display:inline;'>{title}</div></p></b></td>
    <td><a href="{originalURL}">original</a></td>
    <td rowspan="2">{desc}</a></td>
    <td rowspan="2"><a href="https://GitHub.com/{newurl}/stargazers/">
    <img src="badges/stars/{urlWithUnderscore}.svg" alt="Logo" ></a></td>
  </tr>
  <tr>
    <td><a href="{badgeURL}">with badges</a></td>
  </tr>"""
#     <td rowspan="2"><a href="https://GitHub.com/{newurl}/">
    # <img src="https://img.shields.io/github/last-commit/{newurl}.svg" alt="Logo" ></a></td>


# open output file for reading
with open("README.md","r") as f:
    pogggg = f.read()

firstPart = pogggg.split('<table style="max-width:100%;table-layout:auto;">')[0]
SecondPart = pogggg.split('</table>')[1]
newText = firstPart + '<table style="max-width:100%;table-layout:auto;">' + strx + "</table>"+ SecondPart
with open("README.md","w") as f:
    f.write(newText)
