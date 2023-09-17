import os
from googlesearch import search

DEFAULT_ROOTS = {
    'vnexpress': 'html', 
    'cafef': 'htm',
    'vietstock': 'chn', 
    'wikipedia': ''
}

def get_urls(query, num_urls, roots=DEFAULT_ROOTS):
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
        for root, ext in roots.items():
            if root in url and ext in url:
                urls.append(url)
    return urls


if __name__ == "__main__":
    # query = input('Nhập câu truy vấn: ')
    query = 'Thị trường chứng khoán Việt Nam'
    num_urls = 30
    query_folder = 'E:\Orient\EconomicChatbot\data'

    if os.path.exists(query_folder) == False:
        os.makedirs(query_folder)

    urls = get_urls(query, num_urls)
    i = 0
    for url in urls:
        print(url)
        file_name = ''
        for root in DEFAULT_ROOTS.keys():
            if root in url:
                i += 1
                file_name = root + str(i) + '.txt'
                break
        run = 'python E:\Orient\EconomicChatbot\src\getdata\get_text.py {0} --output-dir={1} --file-name={2}'.format(url, query_folder, file_name)
        os.system(run)