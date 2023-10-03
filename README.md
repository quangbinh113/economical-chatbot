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
[![Python](https://th.bing.com/th/id/R.60a2750039f7273f41bcb4ada00e761a?rik=7GGJS2p2OOPhhg&riu=http%3a%2f%2fclipart-library.com%2fimages_k%2fpython-logo-transparent%2fpython-logo-transparent-22.png&ehk=FnvntKvfA2g8Wai00iqiTH%2fu2DEdtPpgV0ejxYLoZpI%3d&risl=&pid=ImgRaw&r=0)](https://www.python.org/)

[![OpenAI](https://technosports.co.in/wp-content/uploads/2020/12/open-ai.png)](https://www.openai.com/)



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
    \t'vnexpress': 'sidebar-1',  
    \t'cafef': 'left_cate totalcontentdetail','vietstock': 'content',  
    \t'wikipedia': 'mw-content-container',  
    \t'tinnhanhchungkhoan': 'leftBlock wrap_noi_dung',  
    \t'thanhnien': 'detail__cmain',  
    \t'mof.gov': 'new-content cd-content',  
    \t'vneconomy.vn': 'detail__header',  
    \t'nhandan.vn': 'main-content article',  
    \t'baochinhphu.vn': 'detail-mcontent'  
    \t'tapchicongthuong.vn': 'post-content'  
    \t'tapchitaichinh.vn': 'detail-wrap'  
    \t'quochoi.vn': 'container'  
    \t'vtv.vn': 'noidung'  
    \t'www.tapchicongsan.org.vn': 'clearfix ContentDetail'  
    \t'baodautu.vn': 'col630 ml-auto mb40'  
    \t'tuoitre.vn': 'detail__cmain'  
    \t'laodong.vn': 'pl'  
    \t'dangcongsan.vn': 'detail-post hnoneview'  
    \t'kinhtevadubao.vn': 'post',  
    \t'tapchinganhang.gov.vn': 'col_left',  
    \t'dantri.com.vn': 'singular-wrap',  
}

