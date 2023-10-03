<!-- PROJECT LOGO -->
<div align="center">

  <h1 align="center"><br>Vietnamese Economical Chatbot</br></h1>

</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-repository">About The Repository</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>


<!-- ABOUT THE REPOSITORY -->
## About The Repository

This repository is used to build a friendly Vietnamese Chatbot which can answer your questions about Economic Information



### Built With
[![Python]](https://www.python.org/)

[![OpenAI](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/OpenAI_logo.svg/320px-OpenAI_logo.svg.png)](https://www.openai.com/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install all packages mentioned in requirements.txt
   ```sh
   pip install -r requirements.txt
   ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Repository-Name.git
   ```
2. Install all packages mentioned in requirements.txt
   ```sh
   pip install -r requirements.txt
   ```
3. Create the .env file inside the economical-chatbot folder. Configure all of the following environment variables:
- OPENAI_API_KEY
- NEWS_CLASS_MAPPING = {  
        'vnexpress': 'sidebar-1',  
        'cafef': 'left_cate totalcontentdetail','vietstock': 'content',  
        'wikipedia': 'mw-content-container',  
        'tinnhanhchungkhoan': 'leftBlock wrap_noi_dung',  
        'thanhnien': 'detail__cmain',  
        'mof.gov': 'new-content cd-content',  
        'vneconomy.vn': 'detail__header',  
        'nhandan.vn': 'main-content article',  
        'baochinhphu.vn': 'detail-mcontent'  
        'tapchicongthuong.vn': 'post-content'  
        'tapchitaichinh.vn': 'detail-wrap'  
        'quochoi.vn': 'container'  
        'vtv.vn': 'noidung'  
        'www.tapchicongsan.org.vn': 'clearfix ContentDetail'  
        'baodautu.vn': 'col630 ml-auto mb40'  
        'tuoitre.vn': 'detail__cmain'  
        'laodong.vn': 'pl'  
        'dangcongsan.vn': 'detail-post hnoneview'  
        'kinhtevadubao.vn': 'post',  
        'tapchinganhang.gov.vn': 'col_left',  
        'dantri.com.vn': 'singular-wrap',  
}

