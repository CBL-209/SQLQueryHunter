import os
import requests
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import time
import random
import urllib3
import sys
from colorama import init, Fore

print("──────────────────────────────────────────────")
print("  Script name : SQLQueryHunter ")
print("  Script by Mohammad Radmehr")
print("  Contact: Telegram = t.me/CBL_209")
print("  Cybersecurity expert with a focus on web penetration testing")
print("  vulnerability assessment, and comprehensive reporting to strengthen")
print("  the security of web-based systems.")
print("──────────────────────────────────────────────")

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# List of common User-Agents to bypass WAF
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Linux; Android 10; SM-A305F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
]

# List of common Referer headers to bypass WAF
referers = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.yahoo.com/',
    'https://www.reddit.com/',
    'https://www.amazon.com/',
    'https://www.facebook.com/',
    'https://www.twitter.com/',
    'https://www.wikipedia.org/',
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

def is_database_query(url):
    query_keywords = [
        'search', 'query', 'id', 'sql', 'db', 'filter', 'category', 'page', 'sort', 'keyword', 'action', 
        'user', 'password', 'login', 'auth', 'session', 'email', 'token', 'product', 'order', 'price', 
        'zipcode', 'location', 'searchTerm', 'tag', 'post', 'update', 'delete', 'insert', 'select', 'join', 
        'update', 'queryType', 'row', 'column', 'type', 'filterBy', 'sortBy', 'query', 'ref', 'source',
        'offset', 'limit', 'join', 'count', 'database', 'search', 'lookup', 'item', 'data', 'file', 'download'
    ]
    
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for param in query_params:
        if any(keyword in param.lower() for keyword in query_keywords):
            return True
    return False

def extract_links_from_page(url, base_url, referer=None):
    try:
        headers['Referer'] = referer if referer else random.choice(referers)
        response = requests.get(url, headers=headers, verify=False)  # Disable SSL verification
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        
        db_links = []
        for link in links:
            href = link['href']
            absolute_url = urljoin(base_url, href)
            if is_database_query(absolute_url):
                db_links.append(absolute_url)
        
        form_links = extract_form_links(soup, base_url)
        db_links.extend(form_links)
        
        js_links = extract_js_links(soup, base_url)
        db_links.extend(js_links)
        
        return db_links
    
    except requests.exceptions.RequestException as e:
        print(f"Error in sending request to {url}: {e}")
        return []

def extract_form_links(soup, base_url):
    form_links = []
    forms = soup.find_all('form', action=True)
    for form in forms:
        action = form['action']
        absolute_action_url = urljoin(base_url, action)
        if is_database_query(absolute_action_url):
            form_links.append(absolute_action_url)
    return form_links

def extract_js_links(soup, base_url):
    js_links = []
    scripts = soup.find_all('script', src=True)
    
    for script in scripts:
        src = script['src']
        absolute_script_url = urljoin(base_url, src)
        if is_database_query(absolute_script_url):
            js_links.append(absolute_script_url)
    
    return js_links

def crawl_page(url, referer=None):
    base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
    db_links = extract_links_from_page(url, base_url, referer)
    
    return db_links

def process_addresses(filename, output_filename):
    domain_name = input("Please enter the main domain name (e.g., example.com): ").strip()
    
    with open(filename, 'r') as file:
        addresses = file.readlines()
        
        with open(output_filename, 'w') as output_file:  # Open output file for writing
            for address in addresses:
                address = address.strip()
                if address:
                    print(f"Analyzing {address}...", end=" | ", flush=True)
                    
                    db_links = crawl_page(address)
                    found_count = len(db_links)
                    
                    if found_count == 0:
                        print("Found: 0, retrying with Referer...", end=" | ", flush=True)
                        db_links = crawl_page(address, random.choice(referers))
                        found_count = len(db_links)
                    
                    filtered_links = [link for link in db_links if domain_name in link]
                    
                    if filtered_links:
                        for link in filtered_links:
                            output_file.write(f"{link}\n")
                            print(Fore.GREEN + link)
                    
                    print(f"Found: {len(filtered_links)}")
                    time.sleep(random.uniform(1, 3))

def save_request_details(request_method, url, headers, body, filename):
    request_data = f"{request_method} {url} HTTP/1.1\n"
    for header, value in headers.items():
        request_data += f"{header}: {value}\n"
    if body:
        request_data += f"\n{body}\n"
    
    with open(filename, 'w') as req_file:
        req_file.write(request_data)

def save_sqlmap_format_request(request_method, url, headers, body, filename):
    request_data = f"{request_method} {url} HTTP/1.1\n"
    for header, value in headers.items():
        request_data += f"{header}: {value}\n"
    
    # For GET requests, body will be None. If it's a POST, include the body in the request file.
    if body:
        request_data += f"\n{body}\n"

    with open(filename, 'w') as req_file:
        req_file.write(request_data)

def send_http_requests(output_filename):
    # Create 'Request' folder if not exists
    os.makedirs('Request', exist_ok=True)

    with open(output_filename, 'r') as file:
        links = file.readlines()
        
        for idx, link in enumerate(links):
            link = link.strip()
            
            if link:
                # Send HTTP request
                try:
                    response = requests.get(link, headers=headers, verify=False)
                    
                    # Print status code to terminal
                    print(f"Status code for {link}: {response.status_code}")
                    
                    # Save the request headers and body in sqlmap-compatible format
                    request_method = 'GET'
                    body = None  # For GET request, there won't be a body usually
                    request_file = f"Request/request_{idx + 1}.txt"
                    save_sqlmap_format_request(request_method, link, response.request.headers, body, request_file)
                    
                    print(f"Request sent for {link} | Saved to {request_file}")
                
                except requests.exceptions.RequestException as e:
                    print(f"Error sending request to {link}: {e}")

filename = input("Enter the name of the TXT file containing URLs: ")
output_filename = "output_links.txt"
process_addresses(filename, output_filename)

# After processing, send HTTP requests for each extracted link
send_http_requests(output_filename)
