from bs4 import BeautifulSoup # to parse HTML code
import requests # to make HTTP requests
from urllib.parse import urljoin
import csv # Save scrapped data as csv file


def update_url(page=1):
    url = f"""
    https://www.google.com/about/careers/applications/jobs/results?location=San%20Jose%2C%20CA%2C%20USA&page={page}#!t=jo&jid=127025001&
    """

    return url

def main():
    # google job search, location: San Jose CA
    data = []

    url = update_url()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    number_jobs = int(soup.find("span", {"class":"SWhIm"}).text)
    # number of links to parse
    number_to_parse = (number_jobs//20)+1 # each page shows 20 jobs

    jobs = soup.find_all("div", {"class":"sMn82b"})
    counter = 0
    
    print(f"Number of jobs - [{number_jobs}]")
    
    for page in range(number_to_parse):
        page += 1

        url = update_url(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find_all("div", {"class":"sMn82b"})
        data = parse(jobs, counter, data)
        counter+=20
        print(f"Parsed page [{page}/{number_to_parse}]")
        # if page == 1:
        #     exit()
    
    print("Finished")
    write_data(data)
    

    
    
def parse(jobs, counter, data, debugging=False):
    for job in jobs:
        counter += 1
        try:
            title = job.find("h3", {"class":"QJPWVe"}).string
            experience_tag = job.find("span", {"class":"wVSTAb"})
            if experience_tag:
                experience = experience_tag.string
            else:
                experience = job.find_all("span", {"class":"RP7SMd"})[0].find("span").text

            base_link = "https://www.google.com/about/careers/applications"
            href = job.find("a", {"class": "WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb"}, href=True).get("href")
            link = urljoin(base_link, href)
            
            data.append([counter, experience, title, link])

            if debugging:
                # Show parsed job
                print(f"[{counter}] - [{experience}] {title}\n\t{link}")
        
        except Exception as err:
            print("\n")
            print(f"[ERROR]: [{counter}] - {err}")
            print("\n")
            break

    return data

def write_data(data, filename="job-data.csv"):
    with open(filename, "w", newline='') as file:
        spamwriter = csv.writer(file)
        for line in data:
            spamwriter.writerow(line)
    print(f"Data saved in {filename}")


if __name__=="__main__":
    main()