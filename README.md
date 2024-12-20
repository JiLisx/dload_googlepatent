/data/home/liji/dload/dload2023/CN123B



# 所有授权专利列表

## 按日期筛选

```
awk -F, 'NR==1 {for (i=1; i<=NF; i++) {if ($i == "gdate") gdate_col=i; if ($i == "grant_pnr") pnr_col=i}} 
awk -F, 'NR==1 {for (i=1; i<=NF; i++) {if ($i == "gdate") gdate_col=i; if ($i == "grant_pnr") pnr_col=i}} 
NR>1 && $gdate_col >= "1800-01-01" && $gdate_col <= "2999-01-01" {print $pnr_col}' cnpinfo1.csv > grant_pnr_all.txt
```

## 按公开号筛选

### 统计以 'A' 结尾的数量
`tail -n +2 grant2406.csv | awk -F',' '$2 ~ /A$/' | wc -l`

### 统计以 'B' 结尾的数量
`tail -n +2 grant2406.csv | awk -F',' '$2 ~ /B$/' | wc -l`

### 统计以 'C' 结尾的数量
`tail -n +2 grant2406.csv | awk -F',' '$2 ~ /C$/' | wc -l`

### 统计不以 'A', 'B', 'C' 结尾的数量
`tail -n +2 grant2406.csv | awk -F',' '$2 !~ /[ABC]$/' | wc -l`


从`grant2406.csv` 文件中筛选出已授权的专利，并将其公开号（`pnr`）保存到 `grant_pnr_all2402.txt` 文件中

`tail -n +2 grant2406.csv | awk -F',' '$2 ~ /[BC]$/ {print $2}' > grant_pnr_all2402.txt`




# 下载pdf数据统计

## 到2024年6月所有授权的pdf数量
- `wc -l grant_pnr_all2406.txt`
- **6949729** grant_pnr_all2406.txt

## 已经下载的pdf数量
1. **`/data/home/jdang/SIPO_PDF_B`**
   - 总共包含 **5219008** 个 PDF 文件，这部分是党老师直接给的。
   - find /data/home/jdang/SIPO_PDF_B -type f -name "*.pdf" | wc -lc
2. **`/data/home/liji/dload/dload2023/`**
   - CN122 + CN123A + CN123B + CN2406
   - 包含 **3041734** 个 PDF 文件。
   - find /data/home/liji/dload/dload2023 -type f -name "*.pdf" | wc -lc
3. **`/data/home/liji/dload/dload2023/CN123A`**
   - **793668** PDF 文件数量。
   - 这个是下载错的pdf，是专利申请文件，从总数中剔除
   - find /data/home/liji/dload/dload2023/CN123A -type f -name "*.pdf" | wc -lc
4. **`/data/home/liji/dload/dload2023/CN122`**
   - **521909** PDF 文件数量。
   - 这个重复下载的pdf，jdang里已经有了
   - find /data/home/liji/dload/dload2023/CN122 -type f -name "*.pdf" | wc -lc


**已下载的 PDF 文件总数为 6943152**。 (1+2-3-4)



# 运行check.py输出结果

## 剔除CN123A的结果
```
Total granted patents read: 6949729
Total patent PDF files found: 7467074
Scanning PDF files: 7467482it [00:51, 144374.85it/s]
Total PDF files downloaded: 6943152
Patents found in the grant file but missing in the download files: 18410【没有下载成功的】
Extra PDF files found in the download directory but not in the grant file: 11833 【下载了但是不在授权列表的】
Total duplicate PDFs that has been downloaded found: 523906 【重复下载的】
Duplicate PDFs and their paths written to: /data/home/jdang/SIPO_PDF_B/duplicate_pdfs2406.txt
Missing pdf has been written to /data/home/jdang/SIPO_PDF_B/missing_pdfs2406.txt
Extra PDF has been written to /data/home/jdang/SIPO_PDF_B/extra_pdfs2406.txt
Duplicate PDFs have been written to /data/home/jdang/SIPO_PDF_B/duplicate_pdfs2406.txt

```
## 剔除CN122和CN123A的结果
```
Total granted patents read: 6949729
Total patent PDF files found: 6945165
Scanning PDF files: 6945580it [00:49, 139996.62it/s]
Total PDF files downloaded: 6943152
Patents found in the grant file but missing in the download files: 18410
Extra PDF files found in the download directory but not in the grant file: 11833
Total duplicate PDFs that has been downloaded found: 2003
Duplicate PDFs and their paths written to: /data/home/jdang/SIPO_PDF_B/duplicate_pdfs2406.txt
Missing pdf has been written to /data/home/jdang/SIPO_PDF_B/missing_pdfs2406.txt
Extra PDF has been written to /data/home/jdang/SIPO_PDF_B/extra_pdfs2406.txt
Duplicate PDFs have been written to /data/home/jdang/SIPO_PDF_B/duplicate_pdfs2406.txt
```

## Extra PDF: 已经下载但不在txt中的pdf文件列表

- 总数：11833
   - 直接查看最后一位字母的分布和数字
      - `grep -o '.$' extra_pdfs2406.txt | sort | uniq -c`
      -  348 8、299 9、11182 B、4 C


- 以B结尾的授权专利没有下载下来：11182
  - 这部分应该是他给的列表的问题，导致我下载了，但是后边更新的列表里没有了
     - 有的专利还没授权，打开google patent下载的其实是A，比如CN116703122B
     - 有的已经授权了，但是后边给的列表里没有了？CN116810336B

- 查找extra txt里，以B结尾的行有多少个
   - `grep -c 'B$' extra_pdfs2406.txt`
- 如果查询不以B结尾的
   - `grep -vc 'B$' extra_pdfs2406.txt` 


## Missing PDF: 在授权列表中，但是没有下载到pdf

- 无法下载的PDF：18410
   - 15762 B、 2648 C

- 例如：
  - https://patents.google.com/patent/CN101140787B/en?oq=CN101140787B
  - https://patents.google.com/patent/CN100338773C/en?oq=CN100338773C
 
- 有的是国知局网站也没有pdf，有些国知局网站有，google没有

- Missing PDF的详细信息：missing_detail.txt
   - 匹配grant2406.csv
      - `grep -Ff missing_pdfs2406.txt grant2406.csv > missing_detail.txt`
   - 统计年度分布
      - `awk -F, '{print substr($2, 1, 4)}' missing_detail.txt | sort | uniq -c | sort -k2`
      - 
![image](https://github.com/user-attachments/assets/a7c4cce6-cffe-4cb5-89a1-dc9a504cd91f)

## 重复下载的pdf：523906
- 重复文件总数：523906
   - 又在liji又在jdang：521903【主要在CN122里】
   - 只在liji：1994
   - 只在jdang：9

- CN122里重复的数量：521909
   - grep "CN122" duplicate_pdfs2406.txt | awk -F, '{count=0; for(i=3; i<=NF; i++) if ($i ~ /CN122/) count++; print count}' | paste -sd+ | bc

- CN123B里重复的数量：3998
   - 一个文件可能在三个路径下重复
   - grep "CN123" duplicate_pdfs2406.txt | awk -F, '{count=0; for(i=3; i<=NF; i++) if ($i ~ /CN123B/) count++; print count}' | paste -sd+ | bc


