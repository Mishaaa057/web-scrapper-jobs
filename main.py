from bs4 import BeautifulSoup # to parse HTML code
import requests # to make HTTP requests

# google job search, location: San Jose CA
page = 1
url = f"""
https://www.google.com/about/careers/applications/jobs/results?location=San%20Jose%2C%20CA%2C%20USA&page={page}#!t=jo&jid=127025001&
"""

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
# li - list tag in HTML
# h3 - header tag
# items = soup.find_all("h3", {"class":"QJPWVe"})

# find all titles
# for idx, item in enumerate(items):
#     print(idx, item.contents[0])

jobs = soup.find_all("div", {"class":"sMn82b"})

# title = jobs[0].contents[0].string 
# title = jobs[0].find("h3", {"class":"QJPWVe"}).string
# experience = jobs[0].find("span", {"class":"wVSTAb"}).string

for idx, job in enumerate(jobs):
    idx += 1
    try:
        title = job.find("h3", {"class":"QJPWVe"}).string

        experience_tag = job.find("span", {"class":"wVSTAb"})
        #experience = job.find("span", {"class":"wVSTAb"}).string
        if experience_tag:
            experience = experience_tag.string
        else:
            experience = job.find_all("span", {"class":"RP7SMd"})[1].find("span").text

        print(f"[{idx}] - [{experience}] {title}")
    except Exception as err:
        print("\n")

        print(f"[ERROR]: [{idx}] - {err}")

        print("\n")
    