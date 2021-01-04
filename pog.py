import urllib.request



def straightUpPoggers(URL):
    URLImageReplacementList = URL.split("https://raw.githubusercontent.com/")[1].split("/")
    URLImageReplacementList.insert(2,"raw")
    URLImageReplacementString = "https://github.com/"+"/".join(URLImageReplacementList[:-1]) + "/"
    response = urllib.request.urlopen(URL)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

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
    return text

URL = "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md"
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
import json

with open('ListOfAwesome.json', 'w') as filehandle:
    json.dump(listpog2, filehandle)

strx = ""
strx = strx + """  <tr style="text-align:center;">
    <th>Repo Name</th>
    <th>Links</th>
    <th>Description</th>
    <th>Stars</th>
    <th>Last Commit</th>
  </tr>"""
for i in listpog2:
    badge = ""
    title = i[1].split("/")[1]
    desc = i[0]
    newurl = i[1]
    originalURL = f"github.com/{i[1]}"
    badge = f"[![GitHub stars](https://img.shields.io/github/stars/.svg)](https://GitHub.com/{newurl}/stargazers/)"
    badgeURL = f"awesome/{newurl}.md"

    strx = strx + f"""
      <!-- ** {title} -->
  <tr>
    <td rowspan="2"><b><p style="display:inline-block;" ><div style='vertical-align:middle; display:inline;'>{title}</div></p></b></td>
    <td><a href="{originalURL}">original</a></td>
    <td rowspan="2">{desc}</a></td>
    <td rowspan="2"><a href="https://GitHub.com/{newurl}/stargazers/">
    <img src="https://img.shields.io/github/stars/{newurl}.svg" alt="Logo" ></a></td>
    <td rowspan="2"><a href="https://GitHub.com/{newurl}/">
    <img src="https://img.shields.io/github/last-commit/{newurl}.svg" alt="Logo" ></a></td>
  </tr>
  <tr>
    <td><a href="{badgeURL}">with badges</a></td>
  </tr>"""


# open output file for reading
with open("README.md","r") as f:
    pogggg = f.read()

firstPart = pogggg.split('<table style="max-width:100%;table-layout:auto;">')[0]
SecondPart = pogggg.split('</table>')[1]
newText = firstPart + '<table style="max-width:100%;table-layout:auto;">' + strx + "</table>"+ SecondPart
with open("README.md","w") as f:
    f.write(newText)
