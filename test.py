from asammdf import MDF, Signal
import numpy as np

def run(filename, variable) :
    with MDF(filename, version='3.30') as mdf_file :
        mdf_file_Resample = mdf_file.resample(0.01)
        data_num=len(variable)
        sig =[]
        sig.append(mdf_file_Resample.get(variable[0]).timestamps)
        sig2 = mdf_file_Resample.get(variable[3]).samples

        # print(type(mdf_file_Resample.get(variable[3]).samples[0]))

        # if (type(mdf_file_Resample.get(variable[1]).samples[0]) == np.bytes_):
        #     mdf_file_Resample.get(variable[1]).samples.decode('utf-8')
        #
        # '''type(Byte) Decode'''
        # sig3_Conv = list()
        # sig4_Conv = list()
        # data_num = len(sig1)
        # j = 0
        # while j < data_num:
        #     sig3_Conv.append(sig3[j].decode('utf-8'))
        #     sig4_Conv.append(sig4[j].decode('utf-8'))
        #     j += 1
        # ''' '''



        print(type(sig2))
        print(sig2)
        print(type(sig))
        print(sig[0])
        print(data_num)
        j=0
        while j < data_num:
            sig.append(mdf_file_Resample.get(variable[j]).samples)
            j += 1
            # while
            # if (type(sig[j][0])==np.bytes_) :
            #     data_num=len(sig[j])
            #
            #


        if (type(mdf_file_Resample.get(variable[3]).samples[0]) == np.bytes_):
            print('true')
            print(sig[4])
            data_num = len(sig[4])
            print(data_num)
            j = 0
            sig4 = []
            while j < data_num:
                sig4.append(sig[4][j].decode('utf-8'))
                j += 1
            print(sig4)
            sig[4] = sig4
            ''' '''
        # sig3_Conv.append(sig3[j].decode('utf-8'))
        return (sig)


        # sample_time = mdf_file_Resample.get(variable[0]).timestamps
        # sig1 = mdf_file_Resample.get('dmm_GRincorrDiff1_rpm').samples
        # sig2 = mdf_file_Resample.get('dmm_GRincorrDiff2_rpm').samples
        # sig3 = mdf_file_Resample.get('gbm_ActGearOdd').samples
        # sig4 = mdf_file_Resample.get('gbm_ActGearEven').samples
        # sig5 = mdf_file_Resample.get('iom_VSP16').samples
        # sig6 = mdf_file_Resample.get('rbm_TTCur').samples
        # print('''
        # [0] : sample time
        # [1] : dmm_GRincorrDiff1_rpm
        # [2] : dmm_GRincorrDiff2_rpm
        # [3] : gbm_ActGearOdd
        # [4] : gbm_ActGearEven
        # [5] : iom_VSP16
        # [6] : rbm_TTCur
        # ''')

    #     print("[[0] : sample time :",type(sig1))
    #     return (sample_time,sig1,sig2,sig3,sig4,sig5,sig6)
    #
    # print(type(sig1))
    # '''type(Byte) Decode'''
    # sig3_Conv = list()
    # sig4_Conv = list()
    # data_num = len(sig1)
    # j = 0
    # while j < data_num:
    #     sig3_Conv.append(sig3[j].decode('utf-8'))
    #     sig4_Conv.append(sig4[j].decode('utf-8'))
    #     j += 1
    # ''' '''