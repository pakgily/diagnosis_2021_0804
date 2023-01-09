from asammdf import MDF, Signal
import numpy as np

''' 목적 : mdf 파일과 분석코자하는 변수를 입력 받아 분석가능한 형태로 Array로 반환
        1. 입력 받은 변수 순서대로 반환하는 Array 변수에 순차적으로 저장
        2. 입력 받은 변수가 bytes 타입일 경우, 데이터 값 앞에 b가 붙기 때문에 utf-8 decode가 필요하기에 해당 부분도 포함.
'''
def run(filename, variable):
    with MDF(filename, version='3.30') as mdf_file:
        mdf_file_Resample = mdf_file.resample(0.01)
        data_num = len(variable)
        data_len = len(mdf_file_Resample.get(variable[0]))
        sig = []
        sig.append(mdf_file_Resample.get(variable[0]).timestamps)

        i = 0
        while i < data_num:
            if (type(mdf_file_Resample.get(variable[i]).samples[0]) == np.bytes_):
                raw_data = mdf_file_Resample.get(variable[i]).samples #mdf 데이터 메모리에 저장 후에 Decode(utf-8)해야 시간 소요 적음
                decode_data = []
                j = 0
                while j < data_len :
                    decode_data.append(raw_data[j].decode('utf-8'))
                    j += 1
                decode_data = np.array(decode_data) # list를 ndarray로 변경
                sig.append(decode_data)
            else :
                sig.append(mdf_file_Resample.get(variable[i]).samples)
            i += 1
    return(sig)