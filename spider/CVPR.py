import numpy as np
import requests,bs4
from concurrent.futures import ProcessPoolExecutor
import time
import os
import io
from PyPDF2 import PdfMerger  
import contextlib
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import random

agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36'
        ]
ua = random.choice(agent) 


class Spider():
    def __init__(self, work_root="./", name="Spider", num_workers=5):
        self.url_list = []
        self.name = name 
        self.root = work_root
        self.num_workers = num_workers
        self.target_dir = os.path.join(self.root, self.name)

    def get_name(self):
        return self.name
    
    def get_pdf_list_file(self):
        pass

    def get_idx_to_paper_file(self):
        pass

    def get_pdf(self, unit):
        if len(unit) == 2:
            title, paper_link = unit[0], unit[1]
        elif len(unit) == 3:
            title, paper_link, supp_link = unit[0], unit[1], unit[2]
        target_paper_dir = os.path.join(self.target_dir, "paper")
        if not os.path.exists(target_paper_dir):
            os.mkdir(target_paper_dir)
        save_path = os.path.join(target_paper_dir, title)
        if os.path.exists(save_path+".pdf"):
            print(" Exists...",save_path)
            pass
        else:
            self.get_file_from_url(paper_link=paper_link, save_path=save_path)
            if len(unit) == 3 and supp_link is not None:
                save_supp_path = os.path.join(target_paper_dir, 'supp_'+title)
                self.get_file_from_url(paper_link=supp_link, save_path=save_supp_path)

    def get_file_from_url(self, paper_link, save_path):
        send_headers = {
            "User-Agent": ua,
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cookie": "OJSSID=lmv39p08rj7chjsi5sqpunoejb",
        }
        req = requests.get(paper_link, headers=send_headers)  
        bytes_io = io.BytesIO(req.content)  
        with open(save_path + ".pdf", 'wb') as file:
            file.write(bytes_io.getvalue())  
            print("***Saved", save_path)
        time.sleep(1)
        return bytes_io

    def single_spider(self):
        for unit in self.url_list:
            self.get_pdf(unit)

    def process_spider(self):
        process_pool = ProcessPoolExecutor(max_workers = self.num_workers)
        process_pool.map(self.get_pdf, self.url_list)

    def spider(self, mode="single", is_merge=False):
        start = time.time()
        # get_target_pdf_list_file
        self.get_pdf_list_file()
        end = time.time()
        print("Stage I: get pdf list file finish! Time Consume: {:3f}".format(end - start))

        # get_target_idx_to_paper_file
        start = end
        self.get_idx_to_paper_file()
        end = time.time()
        print("Stage II: get idx_to_paper file finish! Time Consume: {:3f}".format(end - start))

        # start spider
        start = end
        if mode == 'single':
            self.single_spider()
        elif mode == "process":
            self.thread_spider()
        end = time.time()
        print("Finish! Time Consume: {:3f}".format(end - start))

        # test
        if is_merge:
            self.pdf_merge()
    

    # test
    def pdf_merge(self):
        paper_dir = os.path.join(self.target_dir, "paper")
        merge_paper_dir = os.path.join(self.target_dir, "paper_merge")
        if not os.path.exists(merge_paper_dir):
            os.mkdir(merge_paper_dir)
        files_list = os.listdir(paper_dir)
        for file_name in files_list:
            if "supp" in file_name:
                target_merge_path = os.path.join(merge_paper_dir, file_name.split("_")[-1])
                with contextlib.ExitStack() as stack:
                    merger = PdfMerger()
                    fs = [stack.enter_context(open(pdf,'rb')) for pdf in [os.path.join(paper_dir, file_name), os.path.join(paper_dir, file_name.split("_")[-1])]]
                    for f in fs: 
                        merger.append(f)
                    with open(target_merge_path,'wb') as new_file:
                        merger.write(new_file)
    
    def __call__(self, mode='single', is_merge=False):
        return self.spider(mode=mode, is_merge=is_merge)
    
class CVPR_spider(Spider):
    def __init__(self, home_page, target_prefix_page, work_root="./", name="CVPR", num_workers=5):
        super(CVPR_spider, self).__init__(work_root=work_root, name=name, num_workers=num_workers)
        self.home_page = home_page
        self.target_prefix_page = target_prefix_page
        self.target_dir = os.path.join(self.root, self.name)
        if not os.path.exists(self.target_dir):
            os.mkdir(self.target_dir)
        self.target_file_name = os.path.join(self.target_dir, self.get_name() + "_pdf_list.txt")
        self.target_idx_to_paper_name = os.path.join(self.target_dir, self.get_name() + "_idx_to_paper.txt")

    def get_pdf_list_file(self):
        f = open(self.target_file_name, 'w+')
        response = requests.get(url=self.home_page)
        if response.content:
            soup = bs4.BeautifulSoup(response.text, features="lxml")
            ele_list = soup.select("dd")
            paper_num=0
            for ele in ele_list:
                # if 'pdf' in ele.text or 'supp' in ele.text:
                if 'pdf' in ele.text :
                    href = ele.findAll("a")
                    if "pdf" in href[0].text:
                        paper = href[0].get('href')
                        f.write(self.target_prefix_page + paper[1:] + "\n")
                    # if "supp" in href[1].text:
                    #     supp = href[1].get('href') 
                    #     f.write(self.target_prefix_page + supp[1:] + "\n")
                    f.write("\n")
                    paper_num+=1
                    if(paper_num>=200):
                        break
        f.close()

    def get_idx_to_paper_file(self):
        index = open(self.target_idx_to_paper_name,"w+")
        url_list = []
        with open(self.target_file_name,"r") as fpdf:
            paper = None
            supp = None
            paper_cnt = 0
            for line in fpdf.readlines():
                if line == "\n":
                    paper_cnt += 1
                    title =  " ".join(paper.split("/")[-1].split("_")[1:-3])
                    index.write(str(paper_cnt) +" "+title+"\n")
                    self.url_list.append((str(paper_cnt), paper))
                    paper = None
                    supp = None
                elif paper is None: 
                    paper = line.strip()
                # else:
                    # supp = line.strip()
            index.close()

"""CVPR home page: https://openaccess.thecvf.com/CVPR2022?day=all
         prefix page: https://openaccess.thecvf.com/ """


if __name__ == "__main__":
    home_page = "https://openaccess.thecvf.com/CVPR2024?day=all"
    target_prefix_page = "https://openaccess.thecvf.com/"
    cvpr_spider = CVPR_spider(home_page=home_page, target_prefix_page=target_prefix_page)
    cvpr_spider()