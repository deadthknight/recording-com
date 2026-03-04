import pandas as pd
import re
from datetime import datetime

# === 1. 读取 Excel 文件 ===
file_path = r"C:\Users\wlaqc-pc\Desktop\1.xlsx"
df = pd.read_excel(file_path, header=None, names=['raw_date'])

# === 2. 当前年份 ===
current_year = datetime.now().year

# === 3. 定义提取年份的函数 ===
def extract_year(value):
    if pd.isna(value):
        return None
    text = str(value)
    # 匹配 4 位年份（2000-2099、1900-1999）
    match = re.search(r'(20\d{2}|19\d{2})', text)
    if match:
        return int(match.group(1))
    return None

# === 4. 提取年份列 ===
df['year'] = df['raw_date'].apply(extract_year)

# === 5. 去掉无法识别年份的行 ===
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)

# === 6. 计算使用年限 ===
df['age'] = current_year - df['year']

# === 7. 统计结果 ===
total = len(df)
over_5 = (df['age'] > 5).sum()
over_10 = (df['age'] > 10).sum()
before_2020 = (df['year'] < 2020).sum()
before_2022 = (df['year'] < 2022).sum()   # ✅ 新增：统计 2022 年以前的设备数量

# === 8. 计算比例 ===
over_5_ratio = over_5 / total * 100
over_10_ratio = over_10 / total * 100
before_2020_ratio = before_2020 / total * 100
before_2022_ratio = before_2022 / total * 100   # ✅ 新增比例

# === 9. 输出结果 ===
print(f"总记录数：{total}")
print(f"超过5年：{over_5} ({over_5_ratio:.2f}%)")
print(f"超过10年：{over_10} ({over_10_ratio:.2f}%)")
print(f"2020年之前：{before_2020} ({before_2020_ratio:.2f}%)")
print(f"2022年之前：{before_2022} ({before_2022_ratio:.2f}%)")  # ✅ 新增输出

# === 10. 导出结果（含年份列） ===
output_path = r"C:\Users\wlaqc-pc\Desktop\output_with_years.xlsx"
df.to_excel(output_path, index=False)
print(f"\n已保存详细结果到：{output_path}")
