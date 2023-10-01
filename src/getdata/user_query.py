import os
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
import time

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
    
def delete_all_file(path):
    files = os.listdir(path)
    
    for file in files:
        f = os.path.join(path,file)
        if os.path.isfile(f):
            os.remove(f)
    
def get_data(query,num_urls = 2,query_folder = 'data'):
    def process_url(url, i):
        file_name = f'_{i}.txt'
        print(url,file_name)
        run = 'python src/getdata/get_text.py {0} --output-dir={1} --file-name={2}'.format(url, query_folder, file_name)
        os.system(run)

    start = time.time()
    if os.path.exists(query_folder) == False:
        os.makedirs(query_folder)
    else:
        delete_all_file(query_folder)
    urls = get_urls(query, num_urls)
    i = 0
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
        for url in urls:
            i += 1
            executor.submit(process_url, url, i)

    print('crawl in:', time.time() - start)


if __name__ == "__main__":
    query_arr = [
#         'Thị trường chứng khoán Việt Nam',
#         'Thông tin về giá cổ phiếu VNM',
#         'Thông tin về giá cổ phiếu VCB',
#         'Cổ phiếu họ Vingroup',
#         'Cổ phiếu họ Masan',
#         'Biến động thị trường quý 2 năm 2023',
#         'Lãi suất tiền gửi ngân hàng Việt Nam',
#         'Tăng trưởng GDP Việt Nam năm 2023',
#         'Tác động của đại dịch COVID-19 lên nền kinh tế Việt Nam',
        'Kế hoạch phát triển hạ tầng giao thông Việt Nam',
        'Thị trường bất động sản Việt Nam',
        'Chính sách thuế tại Việt Nam',
        'Chỉ số tiêu dùng và lạm phát Việt Nam',
        'Ngành công nghiệp công nghệ thông tin tại Việt Nam',
        'Tình hình xuất khẩu và nhập khẩu hàng hóa của Việt Nam',
        'Tác động của biến đổi khí hậu lên nông nghiệp Việt Nam',
        'Chương trình hỗ trợ doanh nghiệp tại Việt Nam',
        'Chính sách ngân hàng trung ương Việt Nam',
        'Nguy cơ và cơ hội đầu tư tại Việt Nam',
        'Phát triển nguồn nhân lực và lao động tại Việt Nam',
        'Hiệu quả của các dự án công trình hạ tầng ở Việt Nam',
        'Dự đoán tình hình kinh tế Việt Nam trong năm 2023',
        'Dự báo xu hướng thị trường chứng khoán Việt Nam năm 2023',
        'Lộ trình phục hồi kinh tế sau đại dịch COVID-19 tại Việt Nam',
        'Cơ hội và thách thức cho doanh nghiệp Việt Nam trong năm 2023',
        'Chính sách tài khóa và tiền tệ của Việt Nam dự kiến trong năm 2023',
        'Dự kiến biến động lãi suất và tỷ giá ngoại tệ năm 2023 tại Việt Nam',
        'Kế hoạch đầu tư công và phát triển hạ tầng của Việt Nam trong tương lai gần',
        'Các nguy cơ và cơ hội đầu tư dài hạn tại Việt Nam',
        'Dự kiến biến đổi khí hậu và tác động lên kinh tế nông nghiệp tại Việt Nam',
        'Chương trình hỗ trợ doanh nghiệp và phát triển công nghệ trong năm 2023',
        'Các vấn đề xã hội và giáo dục đáng quan tâm tại Việt Nam trong tương lai',
        'Dự kiến thay đổi trong lĩnh vực chính trị và chính sách ở Việt Nam',
        'Tình hình thị trường bất động sản Việt Nam trong năm 2023',
        'Dự kiến biến đổi công nghiệp và thương mại tại Việt Nam',
        'Chương trình bảo hiểm xã hội và bảo hiểm y tế trong tương lai gần của Việt Nam',
        'Phát triển nguồn nhân lực và lao động trong các ngành công nghiệp tại Việt Nam',
        'Hiệu quả của các dự án công trình hạ tầng và xây dựng trong năm 2023',
        'Dự báo xu hướng công nghiệp 4.0 tại Việt Nam trong năm 2023',
        'Cách ứng phó với biến đổi khí hậu tại Việt Nam trong thập kỷ tới',
        'Tác động của cách mạng công nghiệp lên thị trường lao động tại Việt Nam',
        'Kế hoạch phát triển năng lượng sạch và tái tạo của Việt Nam trong năm 2023',
        'Cách chính phủ Việt Nam đối phó với tình trạng tỷ lệ thất nghiệp tăng cao',
        'Dự kiến thay đổi trong lĩnh vực giáo dục và đào tạo tại Việt Nam',
        'Biến động giá dầu và tác động lên nền kinh tế Việt Nam trong năm 2023',
        'Cơ hội đầu tư vào ngành công nghiệp tiện ích và dịch vụ tại Việt Nam',
        'Thách thức của Việt Nam trong việc duy trì tăng trưởng bền vững',
        'Dự báo tác động của chính trị và bầu cử vào nền kinh tế Việt Nam',
        'Tình hình thị trường lao động và việc làm trong năm 2023 tại Việt Nam',
        'Cơ hội và rủi ro của ngành công nghiệp du lịch tại Việt Nam trong tương lai',
        'Chính sách hỗ trợ doanh nghiệp khởi nghiệp tại Việt Nam trong năm 2023',
        'Dự kiến biến đổi trong lĩnh vực y tế và chăm sóc sức khỏe tại Việt Nam',
        'Kế hoạch phát triển thương mại và xuất khẩu của Việt Nam trong năm 2023',
        'Hiệu quả của các dự án xây dựng cơ sở hạ tầng giao thông ở Việt Nam',
    ]


    num_urls = 30
    folder = r'C:\Users\binh.truong\Code\economical-chatbot\data\data_crawl'
    if os.path.exists(folder) == False:
        os.makedirs(folder)
    for i, query in enumerate(query_arr):
        query_folder = os.path.join(folder, '_'.join(query.split(' ')))
        urls = get_urls(query, num_urls)
        for i, url in enumerate(urls):
            print('Start scraping', url)
            file_name = f'_{i}.txt' 
            run = r'C:\Users\binh.truong\Code\economical-chatbot\src\getdata\get_text.py {0} --output-dir={1} --file-name={2}'.format(url, query_folder, file_name)
            os.system(run)
        print('Done with query: ', query)
        print('------------------------------------------------------------------------')