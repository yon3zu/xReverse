import requests
import re
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning
from colorama import init, Fore, Style

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def reverse_ip(ip):
    url = f"https://apiv2.xreverselabs.my.id/?apiKey=freetrial&ip={ip}"
    user_agent = UserAgent().random
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            domains = data.get('domains', [])
            with open('reversed.txt', 'a') as f:
                for domain in domains:
                    f.write(domain + '\n')
            count = len(domains)
            print(Fore.LIGHTGREEN_EX + ip + Fore.LIGHTCYAN_EX + ': ' + str(count) + ' domains')
        else:
            print(Fore.LIGHTRED_EX + ip + ': No Data Found')
    except Exception as e:
        print(Fore.LIGHTRED_EX + ip + ': Failed to connect to the API!', e)

def scan_ips(ips, threads):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = []
        for ip in ips:
            tasks.append(executor.submit(reverse_ip, ip.strip()))
        for task in tasks:
            task.result()

def main():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "="*50)
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "Reverse IP Lookup Tool")
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "Site : https://xreverselabs.my.id - By t.me/xxyz4")
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "="*50)

    file_name = input(Style.BRIGHT + Fore.YELLOW + "File list of IPs: ")
    threads = int(input(Style.BRIGHT + Fore.YELLOW + "Number of threads to use: "))

    with open(file_name, 'r') as f:
        ips = f.readlines()

    scan_ips(ips, threads)

if __name__ == "__main__":
    main()
