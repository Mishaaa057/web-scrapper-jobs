from bs4 import BeautifulSoup # to parse HTML code
import requests # to make HTTP requests
from urllib.parse import urljoin
import csv # Save scraped data as csv file
import argparse # for command-line interface


DEBUGGING = False
JOBS_PER_PAGE = 20
PARSING = True
FILENAME = None


def BuildArgParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--run", action="store_true", help="Run parser")
    parser.add_argument("-l", "--limit", action="store", required=True, type=int, help="Limit amount of jobs parsed, to collect all the data enter -1")
    parser.add_argument("-n", "--filename", action="store", help="Filename of file for the parsed data to be stored")
    parser.add_argument("-d", "--debugging", action="store_true", help="Debugging will display all the job information during parsing")
    return parser


def main() -> None:
    """
    Main function to execute the script
    """
    parser = BuildArgParser()
    args = parser.parse_args()

    if args.filename:
        global FILENAME
        FILENAME = args.filename

    if args.debugging:
        global DEBUGGING
        DEBUGGING = True

    if args.run:
        print("runnig")
        run(args.limit)


def run(limit:int):
    """
    Start parsing the data

    Args:
        limit (int): limit amount of jobs parsed, to collect all the data enter -1
    """
    # google job search, location: San Jose CA
    data = []

    is_parsing = True

    url = update_url()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    soup = request(url, headers)
    number_jobs = int(soup.find("span", {"class":"SWhIm"}).text)
    # number of links to parse
    number_to_parse = (number_jobs//JOBS_PER_PAGE)+1 # each page shows 20 jobs

    counter = 0
    
    print(f"Number of jobs - [{number_jobs}]")

    for page in range(number_to_parse):
        page += 1

        url = update_url(page)
        soup = request(url, headers)

        data, is_parsing = parse(soup, counter, data, limit, is_parsing)
        counter+=JOBS_PER_PAGE

        # Stop parsing when limit is reached
        if not is_parsing:
            break

        print(f"Parsed page [{page}/{number_to_parse}]")
        if DEBUGGING:
            if page == 3:
                exit()
    
    print("Finished")
    write_data(data)


def parse(soup:BeautifulSoup, counter:int, data:list, limit:int, is_parsing:bool) -> list[list]:
    """
    Parsing data of jobs from BeautifulSoup parser
    

    Args:
        soup (BeautifulSoup): soup parser
        counter (int): job counter value, uses counter from previous parse() to keep track of jobs
        data (list): data of jobs from previous parse() to keep all gathered data together
        limit (int): limit amount of jobs parsed, to collect all the data enter -1
        is_parsing (bool): tells run() funciton to stop on current parsed job
    
    Returns:
        data (list of lists with data): matrix of collected data of jobs. It stores job counter, experience level, title of the job, and link to the job
        is_parsing (bool): tells run() funciton to stop on current parsed job
    
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

            if limit != -1:
                if counter >= limit:
                    print("Parsed last job")
                    is_parsing = False
                    break
        
        except Exception as err:
            print("\n")
            print(f"[ERROR]: [{counter}] - {err}")
            print("\n")
            exit()

    return data, is_parsing


def request(url:str, headers:str) -> BeautifulSoup:
    """
    Sends request to desired URL and creating soup parser

    Args:
        url (str): URL string to parse from
        headers (str): metadata about the request.
    
    Returns:
        soup (BeautifulSoup): soup parser for desired URL
    """
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as err:
        print("\n")
        print(f"[ERROR]: {err}")
        print("\n")
    return soup



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
    if FILENAME != None:
        filename = FILENAME

    with open(filename, "w", newline='') as file:
        spamwriter = csv.writer(file)
        for line in data:
            spamwriter.writerow(line)
    print(f"Data saved in {filename}")


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


if __name__=="__main__":
    main()