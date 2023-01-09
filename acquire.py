#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd


# In[7]:


def get_blog_articles():
    '''
    This function scrapes data from Codeup's
    blog to gget the title and content of the
    blog articles and appends the articles to
    a dataframe, then creates a csv file for
    the dataframe. The dataframe is returned.
    '''
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link['href'] for link in soup.select('.more-link')]

    articles = []

    for url in links:

        url_response = get(url, headers=headers)
        soup = BeautifulSoup(url_response.text, 'html.parser')

        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()

        article_dict = {
            'title': title,
            'content': content
        }

        articles.append(article_dict)
        
    blog_article_df = pd.DataFrame(articles)
    blog_article_df.to_csv('blog_articles.csv', index=False)
    
    return blog_article_df


# In[8]:


def get_news_articles():
    '''
    This function scrapes data from Inshorts's
    site to get the title and content of the
    articles and appends the articles to
    a dataframe, then creates a csv file for
    the dataframe. The dataframe is returned.
    '''
    url = 'https://inshorts.com/en/read'
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = [li.text.lower() for li in soup.select('li')][1:]
    categories[0] = 'national'

    inshorts = []

    for category in categories:

        url = 'https://inshorts.com/en/read' + '/' + category
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        titles = [span.text for span in soup.find_all('span', itemprop='headline')]
        contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

        for i in range(len(titles)):

            article = {
                'title': titles[i],
                'content': contents[i],
                'category': category,
            }

            inshorts.append(article)
    
    inshorts_article_df = pd.DataFrame(inshorts)
    inshorts_article_df.to_csv('news_articles.csv', index=False)
    
    return inshorts_article_df

