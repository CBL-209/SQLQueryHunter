# SQLQueryHunter
Web Crawling &amp; Database Query Link Extractor for Penetration Testing

- Script by Mohammad Radmehr
- Contact : [Telegram](https://t.me/CBL_209) - [t.me/CBL_209](https://t.me/CBL_209)

# Description
This Python script is designed to perform web crawling on a list of URLs and extract potentially malicious or vulnerable database query links. These links are typically used in SQL injection attacks or to interact with databases via web interfaces. The script simulates browsing through the web pages and identifies links or form actions that include typical query parameters related to databases. It can be a valuable tool for penetration testers to quickly find potential attack vectors that need further examination.

Additionally, the script supports user agent rotation, referer header manipulation to bypass WAFs (Web Application Firewalls), and extraction of relevant database query links based on common SQL injection patterns.

# Features
- Crawl Web Pages: The script visits each URL provided by the user and analyzes all anchor (<a>) links, forms (<form>), and JavaScript (<script>) to detect database query links.

- SQL Injection Detection: Uses a list of common database-related keywords (like id, query, db, select, insert, etc.) to identify links and form actions that could be vulnerable to SQL injection or related database attacks.

- Bypass WAFs: The script uses randomized User-Agent and Referer headers to simulate normal user traffic and bypass basic Web Application Firewalls (WAFs).

- Output: The script generates a list of identified database-related links and saves them to a file. Links that contain the main domain of interest are filtered and saved in a separate output file.

- HttpRequest Analysis: After extracting database-related links, the script sends HTTP requests with headers and bodies in a format suitable for SQLMap analysis. These requests are stored in the Request folder, ready to be used in automated penetration testing.

- Status Code Monitoring: As HTTP requests are sent, the script outputs the HTTP status codes of responses to provide real-time feedback on the success or failure of requests.

# How It Works
## Input and URL Crawling
- You provide a text file containing URLs that you want to crawl and analyze.
- For each URL, the script sends an HTTP request and scans the page for links, form actions, and embedded JavaScript that might be interacting with databases.

## Link Extraction
- The script extracts links that contain query parameters commonly associated with SQL injections, such as id=, action=, search=, etc.
- Form actions and JavaScript links are also analyzed for potential database interaction.

## User-Agent & Referer Rotation
- Random User-Agent headers are used to simulate requests from different browsers and devices to avoid detection by WAFs.
- Random Referer headers are also used in the second attempt if no database-related links are found initially, helping to bypass restrictions based on referrer validation.

## Filtered Links
- The script filters out links that are unrelated to the target domain, ensuring that only relevant links are saved for further analysis.

## SQLMap-Formatted Requests
Once database-related links are identified, the script generates HTTP request files in a format compatible with SQLMap, a popular penetration testing tool for automated SQL injection testing.

## Request Logs
The HTTP requests, including headers and body data, are saved in text files and organized in a folder called Request, ready for use in further testing with tools like SQLMap.

# Requirements
- Python 3.x
- BeautifulSoup (pip install beautifulsoup4)
- Requests (pip install requests)
- Colorama (pip install colorama)

# Usage
## Install Dependencies: Before running the script, make sure you have installed the required Python libraries
- pip install requests beautifulsoup4 colorama
- Prepare Input File: Create a text file (e.g., urls.txt) containing the list of URLs you want to analyze. Each URL should be on a new line.

## Run the Script: After installing the dependencies and preparing the input file, run the script
- python crawl_and_extract.py
- Provide the Domain: When prompted, provide the main domain name (e.g., example.com). This will filter the results to only include links that are part of the target domain.

- View Results: The script will output the database-related links to a file named output_links.txt, and store SQLMap-compatible HTTP request files in a Request folder.

## Contribution
- Feel free to fork the repository, submit issues, and create pull requests. This project is open to improvements, bug fixes, and suggestions for new features.


























































