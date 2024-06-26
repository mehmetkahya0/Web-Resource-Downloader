import os
import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib.parse
from colorama import Fore, Back, Style
import datetime
from prettytable import PrettyTable, MARKDOWN
import argparse
import shutil
import time



def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_to_absolute_url(url, base_url):
    return urllib.parse.urljoin(base_url, url)

def get_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        url = convert_to_absolute_url(link['href'], base_url)
        if '://' in url and urllib.parse.urlparse(base_url).netloc != urllib.parse.urlparse(url).netloc:
            continue
        links.add(url)

    return links

def get_resources(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    resources = set()
    for tag in soup.find_all(re.compile('^link|img|script'), src=True):
        url = urllib.parse.urljoin(base_url, tag['src'])
        resources.add(url)

    for tag in soup.find_all('link', href=True):
        url = urllib.parse.urljoin(base_url, tag['href'])
        resources.add(url)

    for tag in soup.find_all('a', href=True):
        url = urllib.parse.urljoin(base_url, tag['href'])
        resources.add(url)

    return resources

def download_resources(folder, resources):
    # Initialize the table
    table = PrettyTable(["Date", "Status", "Resource"])
    
    for resource in resources:
        filename = os.path.join(folder, resource.split('/')[-1])
        if os.path.isdir(filename):
            Date = datetime.datetime.now()
            table.add_row([Date, Fore.BLUE + "Skipped (Directory)" + Fore.RESET, filename])
            continue
        try:
            r = requests.get(resource, stream=True)
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            Date = datetime.datetime.now()
            table.add_row([Date, Fore.GREEN + "Downloaded" + Fore.RESET, filename])
        except requests.exceptions.RequestException as e:
            Date = datetime.datetime.now()
            table.add_row([Date, Fore.RED + "Error" + Fore.RESET, str(e)])

    # Write the table to a text file
    with open('output.txt', 'w') as f:
        f.write(str(table))
    
    return table.get_string(format=MARKDOWN)    

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Download resources from a website.")
    parser.add_argument("url", help="The URL of the website to download resources from.")
    parser.add_argument("folder", help="The folder to download resources to.")
    parser.add_argument("--delete", action="store_true", help="Delete the folder after downloading resources.")
    args = parser.parse_args()

    url = args.url
    folder = args.folder

    if not os.path.exists(folder):
        os.makedirs(folder)

    html = get_html(url)
    links = get_links(html, url)
    resources = get_resources(html, url)

    markdown_table = download_resources(folder, resources)
    with open('output.md', 'w') as f:
        f.write(markdown_table)
        
    print(markdown_table)

    # If the --delete option was provided, delete the folder
    if args.delete:
        print(Fore.RED + "Deleting folder..." + Fore.RESET)
        shutil.rmtree(folder)
        print(Fore.GREEN + "Folder deleted successfully" + Fore.RESET)
        print("System exit..") 
        exit(0)

    for link in links:
        html = get_html(link)
        resources = get_resources(html, link)
        markdown_table = download_resources(folder, resources)
        print(markdown_table)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(Fore.LIGHTYELLOW_EX + f"System run time: {elapsed_time} seconds" + Fore.RESET)

if __name__ == '__main__':
    main()