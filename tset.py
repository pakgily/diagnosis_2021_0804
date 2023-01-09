from asammdf import MDF, Signal

def run(filename, variable) :
    with MDF(filename, version='3.30') as mdf_file :
        mdf_file_Resample = mdf_file.resample(0.01)
        sample_time = mdf_file_Resample.get('dmm_GRincorrDiff1_rpm').timestamps
        sig1 = mdf_file_Resample.get('dmm_GRincorrDiff1_rpm').samples
        sig2 = mdf_file_Resample.get('dmm_GRincorrDiff2_rpm').samples
        sig3 = mdf_file_Resample.get('gbm_ActGearOdd').samples
        sig4 = mdf_file_Resample.get('gbm_ActGearEven').samples
        sig5 = mdf_file_Resample.get('iom_VSP16').samples
        sig6 = mdf_file_Resample.get('rbm_TTCur').samples
        print('''
        [0] : sample time
        [1] : dmm_GRincorrDiff1_rpm
        [2] : dmm_GRincorrDiff2_rpm
        [3] : gbm_ActGearOdd
        [4] : gbm_ActGearEven
        [5] : iom_VSP16
        [6] : rbm_TTCur
        ''')

        print("[[0] : sample time :",type(sig1))
        return (sample_time,sig1,sig2,sig3,sig4,sig5,sig6)