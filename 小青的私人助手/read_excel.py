import pandas as pd
import sys

file_path = '/home/ubuntu/.openclaw/media/inbound/å_æ_---å_äº_ç_¾å_æ_ç---87737fc5-759c-4334-a0cd-88e69550f812.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    print(f'工作表列表: {xl.sheet_names}')

    for sheet in xl.sheet_names:
        print(f'\n{"="*50}')
        print(f'工作表: {sheet}')
        print(f'{"="*50}')
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(df.to_string())
        print(f'\n数据形状: {df.shape}')
        print(f'列名: {list(df.columns)}')

except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()
