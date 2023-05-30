import numpy as np
import pandas as pd


def fuse_liverdata(list1):
    if len(list1) == 2:
        data1 = pd.read_csv(list1[0])
        data2 = pd.read_csv(list1[1])
        data = pd.merge(data1, data2, how='outer')
    if len(list1)> 2:
        data1 = pd.read_csv(list1[0])
        data2 =pd.read_csv(list1[1])
        data = pd.merge(data1, data2, how='outer')
        for i in range(2,len(list1)):
            data1 = pd.read_csv(list1[i])
            data = pd.merge(data,data1,how='outer')
    first_length = len(data)
    data = data.drop(['Dataset'], axis=1)
    age = lambda x: 'children' if x >= 0 and x <= 6 else ('adolescents' if x > 6 and x <= 12 else (
        'teens' if x > 12 and x <= 19 else ('young adults' if x > 19 and x <= 35 else (
            'middle-aged adults' if x > 35 and x <= 55 else 'older adults'))))
    value = []
    for i in data['Age']:
        value.append(age(i))
    data['AgeGroup'] = np.array(value)
    bilirubin = lambda x: 'low' if x < 0.3 else ('normal' if x >= 0.3 and x <= 1.2 else 'high')
    value = []
    for i in data['Total_Bilirubin']:
        value.append(bilirubin(i))
    data['Total_BilirubinGroup'] = np.array(value)
    phosphatase = lambda x: 'low' if x < 44 else (
        'normal' if x >= 44 and x <= 147 else ('high' if x > 147 and x <= 500 else 'veryhigh'))
    value = []
    for i in data['Alkaline_Phosphotase']:
        value.append(phosphatase(i))
    data['Alkaline_PhosphotaseGroup'] = np.array(value)
    aminotransferase = lambda x: 'low' if x < 4 else (
        'normal' if x >= 4 and x <= 36 else ('high' if x > 36 and x <= 100 else 'veryhigh'))
    value = []
    for i in data['Alamine_Aminotransferase']:
        value.append(aminotransferase(i))
    data['Alamine_AminotransferaseGroup'] = np.array(value)
    aminotransferase = lambda x: 'low' if x < 8 else (
        'normal' if x >= 8 and x <= 33 else ('high' if x > 33 and x <= 100 else 'veryhigh'))
    value = []
    for i in data['Aspartate_Aminotransferase']:
        value.append(aminotransferase(i))
    data['Aspartate_AminotransferaseGroup'] = np.array(value)
    protiens = lambda x: 'low' if x < 6.0 else (
        'normal' if x >= 6.0 and x <= 8.3 else ('high' if x > 8.3 and x <= 50.0 else 'veryhigh'))
    value = []
    for i in data['Total_Protiens']:
        value.append(protiens(i))
    data['Total_ProtiensGroup'] = np.array(value)
    albumin = lambda x: 'low' if x < 3.4 else (
        'normal' if x >= 3.4 and x <= 5.4 else ('high' if x > 5.4 and x <= 50.0 else 'veryhigh'))
    value = []
    for i in data['Albumin']:
        value.append(albumin(i))
    data['AlbuminGroup'] = np.array(value)
    albumin_and_globulin_ratio = lambda x: 'low' if x < 39 else (
        'normal' if x >= 39 and x <= 51 else ('high' if x > 51 and x <= 100 else 'veryhigh'))
    value = []
    for i in data['Albumin_and_Globulin_Ratio']:
        value.append(albumin_and_globulin_ratio(i))
    data['Albumin_and_Globulin_RatioGroup'] = np.array(value)
    data = data.drop(['Age', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
                      'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio'], axis=1)
    data = data.dropna()
    data = data.drop_duplicates()
    data.to_csv('media/result/data_liver_fused.csv')
    return len(list1),first_length, len(data)