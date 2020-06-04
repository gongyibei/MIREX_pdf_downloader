import os
import re

import requests
from bs4 import BeautifulSoup


def mkdir(director):
    if not os.path.exists(director):
        os.mkdir(director)


def find_all_pdfurl(html):
    pattern = 'http.+\.pdf'
    pdfurls = re.findall(pattern, html)
    return pdfurls


def download_pdfs(year, url, save_dir):
    mkdir(save_dir)
    rsp = requests.get(url)
    pdfurls = find_all_pdfurl(rsp.text)
    for pdfurl in pdfurls:
        if pdfurl.endswith('.pdf'):
            name = pdfurl.split('/')[-1]
            name = f'{year}_{name}'
            save_path = os.path.join(save_dir, name)
            try:
                pdf = requests.get(pdfurl).content
                with open(save_path, 'wb') as f:
                    f.write(pdf)
            except:
                print('Download failed!')

            print(f'Downloaded : {save_dir}/{name}')


def get_tasks(year):
    base = 'https://www.music-ir.org'
    url = f'https://www.music-ir.org/mirex/wiki/{year}:MIREX{year}_Results'
    tasks = []

    rsp = requests.get(url)
    soup = BeautifulSoup(rsp.text)
    mw = soup.find(class_='mw-parser-output')
    for ul in mw.children:
        if ul.name != 'ul':
            continue
        for li in ul.children:
            if li.name != 'li':
                continue
            # parse task name
            task_name = li.text.split('\n')[0].rstrip()
            task_name = '_'.join(task_name.split())
            # parse task url
            a = li.find('a')
            task_url = a['href']
            if not task_url.startswith('http'):
                task_url = f'{base}{task_url}'
            tasks.append([year, task_name, task_url])
    return tasks


def download_by_year(year):
    mkdir('pdf')
    tasks = get_tasks(year)
    for year, task_name, url in tasks:
        task_dir = task_name.replace('/', '_')
        task_dir = f'pdf/{task_dir}' 
        mkdir(task_dir)
        download_pdfs(year, url, task_dir)


if __name__ == '__main__':
    download_by_year(2019)
