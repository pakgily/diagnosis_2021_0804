import pandas as pd
from pandas import DataFrame

## DataFrame 만들기
df = DataFrame({"Temp": [20.1, 22.3, 21.5, 20.7, 21.2]})

## XlsxWriter 엔진으로 Pandas writer 객체 만들기
writer = pd.ExcelWriter('pandas_xlsxWriter.xlsx', engine='xlsxwriter')

## DataFrame을 xlsx에 쓰기
df.to_excel(writer, sheet_name='Sheet1')

## Pandas writer 객체 닫기
writer.close()
