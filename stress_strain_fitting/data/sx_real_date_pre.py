import pandas as pd
url = 'data/sx_real_data_processed.xlsx'
df = pd.read_excel(url, sheet_name=None)
# # 为每个sheet添加表头
# header = ['num', 'gamma_0', "G'", 'G"', 'LossFactor', 'gamma', 'sigma']

# # 遍历所有sheet
# for sheet_name in df:
#     # 获取当前sheet的数据
#     sheet_data = df[sheet_name]
    
#     # 获取原始表头（列名）
#     original_header = sheet_data.columns.tolist() if not sheet_data.empty else []
#     print(original_header)
#     # 创建新的DataFrame，首先添加新表头，然后添加原始表头，最后添加原始数据
#     new_data = pd.DataFrame([header, original_header] + sheet_data.values.tolist())
    
#     # 更新原始DataFrame
#     df[sheet_name] = new_data

# # 创建一个ExcelWriter对象，用于写入Excel文件
# output_file = 'data/sx_real_data_processed.xlsx'
# with pd.ExcelWriter(output_file) as writer:
#     # 遍历所有sheet，将处理后的数据写入新的Excel文件
#     for sheet_name in df:
#         # 获取当前sheet的数据
#         processed_data = df[sheet_name]
        
#         # 将处理后的数据写入Excel文件的相应sheet
#         processed_data.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

# print(f"处理后的数据已保存到 {output_file}")

# 处理每个sheet
for sheet_name in df:
    # 获取当前sheet的数据
    sheet_data = df[sheet_name]
    
    # 删除列名为'num'的列（如果存在）
    if 'num' in sheet_data.columns:
        sheet_data = sheet_data.drop(columns=['num'])
    
    # 对于每一列（除了gamma和sigma），填充空值为该列的第一个非空且为数值的值
    for column in sheet_data.columns:
        if column != 'gamma' and column != 'sigma':
            # 获取该列的第一个非空且为数值的值
            numeric_values = sheet_data[column].dropna()
            numeric_values = pd.to_numeric(numeric_values, errors='coerce').dropna()
            first_numeric_value = numeric_values.iloc[0] if not numeric_values.empty else None
            if first_numeric_value is not None:
                # 填充该列的空值
                sheet_data[column] = sheet_data[column].fillna(first_numeric_value)
    
    # 更新原始DataFrame
    df[sheet_name] = sheet_data

# 创建一个ExcelWriter对象，用于写入Excel文件
output_file = 'data/sx_real_data_processed_no_num.xlsx'
with pd.ExcelWriter(output_file) as writer:
    # 遍历所有sheet，将处理后的数据写入新的Excel文件
    for sheet_name in df:
        # 获取当前sheet的数据
        processed_data = df[sheet_name]
        
        # 将处理后的数据写入Excel文件的相应sheet
        processed_data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"处理后的数据已保存到 {output_file}")
