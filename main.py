from bs4 import BeautifulSoup # to parse HTML code
import requests # to make HTTP requests
from urllib.parse import urljoin
import csv # Save scraped data as csv file


DEBUGGING = True


def main() -> None:
    """
    Main function to execute the script
    """
    # google job search, location: San Jose CA
    data = []

    url = update_url()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    soup = request(url, headers)
    number_jobs = int(soup.find("span", {"class":"SWhIm"}).text)
    # number of links to parse
    number_to_parse = (number_jobs//20)+1 # each page shows 20 jobs

    counter = 0
    
    print(f"Number of jobs - [{number_jobs}]")


    for page in range(number_to_parse):
        page += 1

        url = update_url(page)
        soup = request(url, headers)

        data = parse(soup, counter, data)
        counter+=20
        print(f"Parsed page [{page}/{number_to_parse}]")
        if DEBUGGING:
            if page == 3:
                exit()
    
    print("Finished")
    write_data(data)



def update_url(page=1) -> str:
    """
    Constructs URL for the given page number.

    Args:
        page (int): page number to fetch jobs from
    
    Returns:
        url (str): URL address of specific page number.
    """

    url = f"""
    https://www.google.com/about/careers/applications/jobs/results?location=San%20Jose%2C%20CA%2C%20USA&page={page}#!t=jo&jid=127025001&
    """

    return url


def request(url:str, headers:str) -> BeautifulSoup:
    """
    Sends request to desired URL and creating soup parser

    Args:
        url (str): URL string to parse from
        headers (str): metadata about the request.
    
    Returns:
        soup (BeautifulSoup): soup parser for desired URL
    """

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def parse(soup:BeautifulSoup, counter:int, data:list) -> list[list]:
    """
    Parsing data of jobs from BeautifulSoup parser
    

    Args:
        soup (BeautifulSoup): soup parser
        counter (int): job counter value, uses counter from previous parse() to keep track of jobs
        data (list): data of jobs from previous parse() to keep all gathered data together
    
    Returns:
        data (list of lists with data): matrix of collected data of jobs. It stores job counter, experience level, title of the job, and link to the job
    
    Example:
        data = [
                [1, "Advanced", "Job Title1", "https://www.google.com/joblink1"],
                [2, "Mid", "Job Title2", "https://www.google.com/joblink2"]
        ]
    """

    jobs = soup.find_all("div", {"class":"sMn82b"})

    for job in jobs:
        counter += 1
        try:
            title = job.find("h3", {"class":"QJPWVe"}).string
            experience_tag = job.find("span", {"class":"wVSTAb"})
            if experience_tag:
                experience = experience_tag.string
            else:
                if len(job.find_all("span", {"class":"RP7SMd"}))>1:
                    experience = job.find_all("span", {"class":"RP7SMd"})[1].find("span").text
                else:
                    experience = job.find_all("span", {"class":"RP7SMd"})[0].find("span").text

            base_link = "https://www.google.com/about/careers/applications"
            href = job.find("a", {"class": "WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb"}, href=True).get("href")
            link = urljoin(base_link, href)
            
            data.append([counter, experience, title, link])

            if DEBUGGING:
                # Show parsed job
                print(f"[{counter}] - [{experience}] {title}\n\t{link}")
        
        except Exception as err:
            print("\n")
            print(f"[ERROR]: [{counter}] - {err}")
            print("\n")
            exit()

    return data


def write_data(data, filename="job-data.csv") -> None:
    """
    Store collected data into csv file.
    The function will REWRITE any existing file with the same name.

    Args:
        data (list[list]): Matrix with gathered data of jobs.
        filename (str): Filename to store all collected data.
    
    Returns:
        None
    """
    with open(filename, "w", newline='') as file:
        spamwriter = csv.writer(file)
        for line in data:
            spamwriter.writerow(line)
    print(f"Data saved in {filename}")


if __name__=="__main__":
    main()