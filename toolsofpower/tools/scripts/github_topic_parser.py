from json import dump
from time import sleep
from random import randint
from requests import get
from bs4 import BeautifulSoup

from tools.models import Tool

def has_pagination(html):
    #if html.find('form', class_='ajax-pagination-form js-ajax-pagination'):
    if html.find('input', {'name':'page'}):
        return True
    return False

def request(url):
    res = get(url)
    if res.status_code != 200:
        raise Exception(f'Error request - {res.url} | {res.status_code}')
    print(f'[+] Requested {url} - {res.status_code} - {len(res.text)}')
    return BeautifulSoup(res.text, features='html.parser')

def get_articles(html):
    articles = []
    for article in html.find_all('article'):
        try:
            new_article = {
                'name': article.find('h3').find_all('a')[-1].text.strip(),
                'description': article.find('div', class_='color-bg-default rounded-bottom-2').find('div', class_='').get('text', ''),
                'github_tags': [a.text.strip() for a in article.find('div', class_='color-bg-default rounded-bottom-2').find('div', class_='d-flex flex-wrap border-bottom color-border-muted px-3 pt-2 pb-2').find_all('a')],
            }
            articles.append(new_article)
        except Exception as e:
            print(f'[!] Error in get_articles - {e} - {new_article}')
    return articles

#TODO: recursive func
def get_topics(page, max):
    html = request(f'https://github.com/topics/pentest?page={page}')
    articles = get_articles(html)
    
    while has_pagination(html) and page < max:
        try:
            page += 1
            html = request(f'https://github.com/topics/pentest?page={page}')
            articles += get_articles(html)
            sleep(randint(1,5))
        except Exception as e:
            print(f'[!] Error in get_topics - {e}')
            break
    return articles

def get_topics_recursive(page, max, articles=[]):
    html = request(f'https://github.com/topics/pentest?page={page}')
    if not has_pagination(html) or page > max:
        return articles
    articles += get_articles(html)
    sleep(randint(1,5))
    get_topics_recursive(page+1, max, articles)
    return articles

def run(*args):    
    start_page = 1
    max_page = 100
    out_file = None

    splited = args[0].split(' ')
    if '-p' in splited:
        start_page = int(splited[splited.index('-p')+1])
    if '-m' in splited:
        max_page = int(splited[splited.index('-m')+1])
    if '-f' in splited:
        out_file = splited[splited.index('-f')+1]

    #topics = get_topics(start_page, max_page)
    topics = get_topics_recursive(start_page, max_page)

    if out_file:
        print(f'[+] Total tools found - {len(topics)}')
        with open(out_file, 'w') as f:
            dump(topics, f)
    else:
        for tool in topics:
            if not Tool.objects.get(name=tool['name']):
                t = Tool(name=tool['name'], description=tool['description'])
                t.save()