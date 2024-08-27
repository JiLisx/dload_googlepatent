import csv
from datetime import datetime

# 定义输入和输出文件名
input_file = "cnpinfo1.csv"
output_file = "grant_2023.txt"

# 定义要筛选的日期范围
start_date = datetime.strptime("20230101", "%Y%m%d")
end_date = datetime.strptime("20231231", "%Y%m%d")

def is_valid_date(date_str, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

# 打开输入文件并创建CSV读取器
with open(input_file, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    with open(output_file, "w") as outfile:
        for row in csvreader:
            if is_valid_date(row[8]):
                grant_date = datetime.strptime(row[8], "%Y-%m-%d")

                if start_date <= grant_date <= end_date:
                    outfile.write(row[11] + "\n")
            else:
                print(f"无效日期格式: {row[8]} 在行: {row}")

print("Done!")
