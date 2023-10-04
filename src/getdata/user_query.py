import os
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time
from src.getdata.crawler.web_extractor import WebPageTextExtractor
list_tails = ['.html', '.htm', '.chn', '.aspx', '.ldo']

def get_urls(query, num_urls):
    """
    A function to get a list of URLs from Google search results.
    Args:
        query: (str) -> The query string.
        num_urls: (int) -> The number of URLs to return.
    Returns:
        urls: (list) -> A list of URLs.
    """
    urls = []
    for url in search(query, tld="co.in", num=10, stop=num_urls, pause=2):
        for val in list_tails:
            if val in url and 'dfat.gov' not in url:
                urls.append(url)
    return urls
    
# def delete_all_file(path):
#     files = os.listdir(path)
    
#     for file in files:
#         f = os.path.join(path,file)
#         if os.path.isfile(f):
#             os.remove(f)
    
# def get_data(query,num_urls = 2,query_folder = 'data'):
#     def process_url(url, i):
#         file_name = f'_{i}.txt'
#         print(url,file_name)
#         run = 'python src/getdata/web_extractor.py {0} --output-dir={1} --file-name={2}'.format(url, query_folder, file_name)
#         os.system(run)

def get_data(query,num_urls = 2):
    res = []
    start = time.time()
    urls = get_urls(query, num_urls)
    urls = set(urls)
    print(urls)
    for url in urls:
        text_extractor = WebPageTextExtractor(url)
        text = text_extractor.get_text_from_div()
        if text:
            res.append(text)

    print('crawl in:', time.time() - start)
    return res


if __name__ == "__main__":
   pass