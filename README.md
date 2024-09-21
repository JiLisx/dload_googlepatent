/data/home/liji/dload/dload2023/CN123B



# 所有授权专利生成txt

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




# 数据统计

## 到2024年6月所有授权的pdf数量
`wc -l grant_pnr_all2406.txt`
**6936180** grant_pnr_all2406.txt

## 已经下载的pdf数量
1. **`/data/home/jdang/SIPO_PDF_B`**
   - 总共包含 **6,534,585** 个 PDF 文件，包括 `CN123A` 目录中的文件。
   - find /data/home/jdang/SIPO_PDF_B -type f -name "*.pdf" | wc -lc
2. **`/data/home/jdang/SIPO_PDF_B/dload/dload2023/CN123A`**
   - 包含 **793,668** 个 PDF 文件。
   - find /data/home/jdang/SIPO_PDF_B/dload/dload2023/CN123A -type f -name "*.pdf" | wc -lc
3. **`/data/home/liji/dload/dload2023/CN123B`**
   - 704,355 PDF 文件数量。
   - find /data/home/liji/dload/dload2023/CN123B -type f -name "*.pdf" | wc -lc

**已下载的 PDF 文件总数为 6,445,272**。 (1-2+3)


## 到2024年6月，缺少的pdf数量

**490908** = 6936180 - 6,445,272



# 运行check.py输出结果

```
Total granted patents read: 6936178
Total patent PDF files found: 8554517
Scanning PDF files: 8554904it [00:16, 514917.71it/s] 【包括重复计算了两个路径下的CN123A和CN122】
Total PDF files processed : 6715018
**Total missing PDFs: 1026661**  【有五十多万pdf没有link，无法下载】
Total extra PDFs: 805501
Missing PDFs written to: /data/home/jdang/SIPO_PDF_B/missing_pdfs2406.txt
Extra PDFs written to: /data/home/jdang/SIPO_PDF_B/extra_pdfs2406.txt
Missing PDFs list has been written to /data/home/jdang/SIPO_PDF_B/missing_pdfs2406.txt
Extra PDFs list has been written to /data/home/jdang/SIPO_PDF_B/extra_pdfs2406.txt
```

## 已经下载但不在txt中的pdf文件列表

- 查找extra txt里 不以A结尾的行有多少个
- `grep -vc 'A$' extra_pdfs2406.txt`
  - **11833**
  - 这部分应该是他给的列表的问题，导致我下载了，但是后边更新的列表里没有了

- 查找extra txt里 以A结尾的行有多少个
- `grep -c 'A$' extra_pdfs2406.txt` 
  - 793668
  - 这是因为我下载错了，下载成发明申请



# 无法下载的PDF

** 有51多万的专利，google patent里没有pdf **

- 例如：
  - https://patents.google.com/patent/CN101140787B/en?oq=CN101140787B
  - https://patents.google.com/patent/CN100338773C/en?oq=CN100338773C

- 具体数字可能是：**515180** =  1219177 - 703997
  - liji@Zhuss-Mac-Pro /V/W/dload2023 (master)> wc -l finish.txt
    - 703997 finish.txt
  - liji@Zhuss-Mac-Pro /V/W/dload2023 (master)> wc -l missing_pdfs.txt
    - 1219177 missing_pdfs.txt





这次应该再下载511481个专利
