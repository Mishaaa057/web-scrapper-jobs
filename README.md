# Google Job Scrapper in San Jose area

This Python script scrapes job listings from Googl'es sareers page for a specified location (San Jose, CA) and stores the data in CSV file. The script uses BeautifulSoup for parsing HTML, requests for making HTTP requests, and argparse for handling command-line arguments.

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library
- `argparse` library

## Installation
1. Cloning the repository
  ```bash
  git clone https://github.com/Mishaaa057/web-scrapper-jobs/
  cd web-scrapper-jobs
  ```
2. Install the required libraries
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

Run the script with the desired options
```bash
python main.py --run --limit <NUMBER_OF_JOBS> --filename <FILENAME>
```

Command-line Arguments 
```
  -r, --run: Run the parser (required).
  -l, --limit: Limit the number of jobs parsed. To collect all the data, enter -1 (required).
  -n, --filename: Filename for storing the parsed data (optional).
  -d, --debugging: Enable debugging mode to display detailed job information during parsing (optional).
```
