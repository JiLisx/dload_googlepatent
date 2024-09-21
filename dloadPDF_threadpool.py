#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time


def dl_pt(pt, path):
    url = "https://patents.google.com/patent/" + pt
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text


def download_pdf(pt, pdf_url, path, folder_idx):
    pdf_folder = os.path.join(path, f"CN{folder_idx:06d}")
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    # start_time = time.time()

    response = requests.get(pdf_url, stream=True)
    pdf_path = os.path.join(pdf_folder, pt + ".pdf")
    with open(pdf_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)

    # end_time = time.time()
    # d_time = end_time - start_time
    # print(f"Downloaded {pt} in {d_time:.2f} seconds, saved to {pdf_path}")


def extract_and_download_pdf(pt, path, folder_idx, finish_file):
    try:
        pt_text = dl_pt(pt, path)
        tree = etree.HTML(pt_text)
        if tree is not None:
            pdf_links = tree.xpath(f'//a[contains(@href, "{pt}") and contains(@href, ".pdf")]/@href')
            if pdf_links:
                pdf_url = pdf_links[0]
                download_pdf(pt, pdf_url, path, folder_idx)
            else:
                print(f"No PDF link found for patent {pt}")
        with open(finish_file, 'a') as f:
            f.write(pt + "\n")
    except Exception as e:
        print(f"Error processing {pt}: {e}")


def get_existing_counts(root_path, initial_folder_idx):
    folder_idx = initial_folder_idx
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
    root_path = "/Volumes/WDC5/dload2023/CN2406/"
    initial_folder_idx = 124001

    grant_file = os.path.join(root_path, "../missing_pdfs2406.txt")
    finish_file = os.path.join(root_path, "../finish2406.txt")

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
    folder_idx, pdf_count = get_existing_counts(root_path, initial_folder_idx)

    max_pdfs_per_folder = 1000
    max_threads = 10  # 设置线程数

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_pt = {}
        for pt in pts_to_download:
            if pdf_count >= max_pdfs_per_folder:
                folder_idx += 1
                pdf_count = 0
            future = executor.submit(extract_and_download_pdf, pt, root_path, folder_idx, finish_file)
            future_to_pt[future] = pt
            pdf_count += 1

        with tqdm(total=len(future_to_pt), desc="Overall Progress") as pbar:
            for future in as_completed(future_to_pt):
                pt = future_to_pt[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing {pt}: {e}")
                pbar.update(1)

