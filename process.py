import csv

# 读取1.txt文件
with open('dataset/2022_1.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 处理数据
data = []
current_record = []

for line in lines:
    line = line.strip()
    if line:  # 如果行不为空
        current_record.append(line)
        if len(current_record) == 13:  # 每13行为一条完整记录
            # 删除学期(第1个元素)和操作(最后一个元素)
            current_record.pop(0)  # 删除学期
            current_record.pop(-1)  # 删除操作
            data.append(current_record)
            current_record = []

# 写入CSV文件，不包含学期和操作列
headers = ['选课序号', '课程编码', '课程名称', '学分', '开课院系', 
          '任课教师', '选课人数', '评价人数', '有效评价人数', '平均分', '中位数']

with open('dataset/2022_1.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for record in data:
        writer.writerow(record) 