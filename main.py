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
items = soup.find_all("h3", {"class":"QJPWVe"})

# find all titles
for idx, item in enumerate(items):
    print(idx, item.contents[0])
