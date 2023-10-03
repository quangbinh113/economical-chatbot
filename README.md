<!-- PROJECT LOGO -->
<div align="center">

  <img src="https://www.wordperfect.com/static/wpo/product_content/wordperfect/x9/icons/icon-performance.png" alt="Project Logo">

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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
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

- DATA_PATH

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
    'tapchicongsan.org.vn': 'clearfix ContentDetail'  
    'baodautu.vn': 'col630 ml-auto mb40'  
    'tuoitre.vn': 'detail__cmain'  
    'laodong.vn': 'pl'  
    'dangcongsan.vn': 'detail-post hnoneview'  
    'kinhtevadubao.vn': 'post',  
    'tapchinganhang.gov.vn': 'col_left',  
    'dantri.com.vn': 'singular-wrap',  
}

<!-- USAGE EXAMPLES -->
## Usage
To run this application, you need to start up two modules:

1. Run the front-end
   ```sh
   streamlit run app.py
   ```
2. Run the back-end
   ```sh
   python main.py
   ```

<!-- CONTRIBUTORS -->
## Contributors

This project was developed as part of the training course. The project was developed by AI Intern 3AE, a team of 3 intern employees:

- [Huy Anh Do](https://github.com/huyanhdo2023)
- [David Huy Ng](https://github.com/Godfreeyyy)
- [Binh Truong](https://github.com/quangbinh113)

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Thanks to Mr. [Pham Dinh Khanh](https://github.com/phamdinhkhanh) for guiding us in this project.
