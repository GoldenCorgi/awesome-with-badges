import urllib.request
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
            fullbadge = f"[![GitHub stars](https://img.shields.io/github/stars/{newurl}.svg)](https://GitHub.com/{newurl}/stargazers/)"
            # print(fullbadge+" "+x)
            oldtext = text
            text = text.replace(divider+x,fullbadge+" "+divider+x)
            # print(x,fullbadge+" "+x)



with open("README.md","w") as f:
    f.write(text)