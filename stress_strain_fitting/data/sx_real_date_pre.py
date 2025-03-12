import numpy as np
import pandas as pd
url = 'data/sx_real_data.xlsx'
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
# for sheet_name in df:
#     # 获取当前sheet的数据
#     sheet_data = df[sheet_name]
    
#     # 删除列名为'num'的列（如果存在）
#     if 'num' in sheet_data.columns:
#         sheet_data = sheet_data.drop(columns=['num'])
    
#     # 对于每一列（除了gamma和sigma），填充空值为该列的第一个非空且为数值的值
#     for column in sheet_data.columns:
#         if column != 'gamma' and column != 'sigma':
#             # 获取该列的第一个非空且为数值的值
#             numeric_values = sheet_data[column].dropna()
#             numeric_values = pd.to_numeric(numeric_values, errors='coerce').dropna()
#             first_numeric_value = numeric_values.iloc[0] if not numeric_values.empty else None
#             if first_numeric_value is not None:
#                 # 填充该列的空值
#                 sheet_data[column] = sheet_data[column].fillna(first_numeric_value)
    
#     # 更新原始DataFrame
#     df[sheet_name] = sheet_data

# # 创建一个ExcelWriter对象，用于写入Excel文件
# output_file = 'data/sx_real_data_processed_no_num.xlsx'
# with pd.ExcelWriter(output_file) as writer:
#     # 遍历所有sheet，将处理后的数据写入新的Excel文件
#     for sheet_name in df:
#         # 获取当前sheet的数据
#         processed_data = df[sheet_name]
        
#         # 将处理后的数据写入Excel文件的相应sheet
#         processed_data.to_excel(writer, sheet_name=sheet_name, index=False)

# print(f"处理后的数据已保存到 {output_file}")
# data_file = 'data/sx_real_data.xlsx'
# # 读取Excel文件中所有sheet的数据，返回一个字典，键为sheet名称，值为对应的DataFrame
# df_new = pd.read_excel(data_file, sheet_name=None)

# # 定义每个sheet对应的时间步数组，并使用高精度计算（dtype=np.float64）
# time_step_values = np.array([68.84, 129.2, 189.5, 249.9, 310.2, 370.5, 430.9, 491.2, 551.6, 611.9, 672.2, 732.6, 792.9, 853.3, 913.6, 973.9, 1034, 1095, 1155, 1215, 1276, 1336, 1396, 1457, 1517, 1577, 1638], dtype=np.float64) / 512.0

# # 对于每个sheet，增加Time和gammadot两列
# for idx, (sheet_name, sheet_data) in enumerate(df_new.items()):
#     # 如果sheet数量超过数组长度，则后续sheet使用最后一个时间步
#     if idx < len(time_step_values):
#         dt = time_step_values[idx]
#     else:
#         dt = time_step_values[-1]
    
#     # 获取当前sheet行数
#     n_rows = sheet_data.shape[0]
    
#     # 使用高精度numpy计算生成Time列，时间从0开始，每个时间点间隔为dt
#     time_array = np.arange(n_rows, dtype=np.float64) * dt
#     sheet_data['Time'] = time_array
    
#     # 计算gammadot列：对现有的gamma列求导
#     # 首先确保gamma列以高精度numpy数组形式处理
#     gamma_array = sheet_data['gamma'].to_numpy(dtype=np.float64)
#     # 使用numpy的gradient函数，利用时间步长dt计算导数
#     gammadot = np.gradient(gamma_array, dt)
#     sheet_data['gammadot'] = gammadot

# # 将处理后的数据写入新的Excel文件
# output_file = 'data/sx_real_data_with_time_and_gammadot.xlsx'
# with pd.ExcelWriter(output_file) as writer:
#     for sheet_name, sheet_data in df_new.items():
#         sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

# print(f"处理后的数据已保存到 {output_file}")


# 遍历所有sheet
for sheet_name, sheet_data in df.items():
    # 计算Time列的差值
    delta_t = sheet_data['Time'].diff()
    
    # 将第一行的值设置为与第二行相同
    delta_t.iloc[0] = delta_t.iloc[1]
    
    # 将delta_t列添加到sheet中
    sheet_data['delta_t'] = delta_t

# 将处理后的数据保存到新文件
output_file = 'data/sx_real_data_with_delta_t.xlsx'
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, sheet_data in df.items():
        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"已添加delta_t列并保存到 {output_file}")
