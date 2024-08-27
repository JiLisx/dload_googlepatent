#!/usr/local/bin/python3
import requests
import os
from lxml import etree
import multiprocessing
from tqdm import tqdm


def dl_pt(pt, path):
    url = "https://patents.google.com/patent/" + pt
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text


def download_pdf(pt, pdf_url, path, folder_idx):
    pdf_folder = os.path.join(path, f"CN{folder_idx:06d}")
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    response = requests.get(pdf_url, stream=True)
    pdf_path = os.path.join(pdf_folder, pt + ".pdf")
    print(f"Downloading {pt}")
    with open(pdf_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)


def extract_and_download_pdf(pt, path, queue, folder_idx):
    pt_text = dl_pt(pt, path)
    tree = etree.HTML(pt_text)
    if tree is not None:
        pdf_links = tree.xpath(f'//a[contains(@href, "{pt}") and contains(@href, ".pdf")]/@href')
        if pdf_links:
            pdf_url = pdf_links[0]
            download_pdf(pt, pdf_url, path, folder_idx)
        else:
            print(f"No PDF link found for patent {pt}")
    with open(os.path.join(path, "../finish.txt"), 'a') as f:
        f.write(pt + "\n")
    queue.put(1)


def d_parse(args):
    pt, path, queue, folder_idx = args
    extract_and_download_pdf(pt, path, queue, folder_idx)


def get_existing_counts(root_path):
    folder_idx = 123001
    pdf_count = 0
    while True:
        folder_path = os.path.join(root_path, f"CN{folder_idx:06d}")
        if not os.path.exists(folder_path):
            break
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        pdf_count = len(pdf_files)
        if pdf_count < 1000:
            break
        folder_idx += 1
        pdf_count = 0
    return folder_idx, pdf_count


if __name__ == "__main__":
    root_path = "/Volumes/WDC5/dload2023/"

    grant_file = os.path.join(root_path, "../grant_pnr_all.txt")
    finish_file = os.path.join(root_path, "../finish.txt")
    
    if not os.path.exists(finish_file):
        open(finish_file, 'w').close()
       
    # 读取已经完成的专利编号
    with open(finish_file, 'r') as file:
        finish = set(line.strip() for line in file.readlines())

    # 读取所有需要下载的专利编号
    with open(grant_file, 'r') as f:
        pts = [line.strip() for line in f.readlines()]

    # 生成未下载的专利列表
    pts_to_download = [pt for pt in pts if pt not in finish]

    # 获取当前的文件夹索引和已下载的文件计数
    folder_idx, pdf_count = get_existing_counts(root_path)

    manager = multiprocessing.Manager()
    queue = manager.Queue()
    pool = multiprocessing.Pool(10)
    results = []
    max_pdfs_per_folder = 1000

    for pt in pts_to_download:
        if pdf_count >= max_pdfs_per_folder:
            folder_idx += 1
            pdf_count = 0
        
        # 动态生成保存路径
        path = os.path.join(root_path, f"CN{folder_idx:06d}")
        if not os.path.exists(path):
            os.makedirs(path)
        
        result = pool.apply_async(func=d_parse, args=((pt, path, queue, folder_idx),))
        results.append(result)
        pdf_count += 1

    with tqdm(total=len(results), desc="Overall Progress") as pbar:
        for _ in range(len(results)):
            queue.get()
            pbar.update(1)

    pool.close()
    pool.join()
