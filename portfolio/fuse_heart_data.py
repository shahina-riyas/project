import numpy as np
import pandas as pd


def fuse_heartdata(list1):
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
    age = lambda x: 'children' if x >= 0 and x <= 6 else ('adolescents' if x > 6 and x <= 12 else (
        'teens' if x > 12 and x <= 19 else ('young adults' if x > 19 and x <= 35 else (
            'middle-aged adults' if x > 35 and x <= 55 else 'older adults'))))
    value = []
    for i in data['age']:
        value.append(age(i))
    data['AgeGroup'] = np.array(value)
    bp = lambda x: 'hypotension' if x < 60 else (
        'normal' if x >= 60 and x <= 80 else ('prehypertension' if x > 80 and x < 90 else 'hypertension'))
    value = []
    for i in data['trestbps']:
        value.append(bp(i))
    data['TrestbpsGroup'] = np.array(value)
    chol = lambda x: 'underweight' if x < 200 else ('borderline' if x >= 200 and x < 239 else 'high')
    values = []
    for i in data['chol']:
        values.append(chol(i))
    data['CholGroup'] = np.array(values)
    hr = lambda x: 'lower' if x < 60 else ('normal' if x >= 60 and x <= 100 else (
        'kid normal' if x > 100 and x <= 110 else ('infant normal' if x > 100 and x < 150 else 'hyper')))
    values = []
    for i in data['thalach']:
        values.append(hr(i))
    data['ThalachGroup'] = np.array(values)
    peak = lambda x: 0 if x <= 0 else (1 if x > 0 and x <= 1 else (2 if x > 1 and x <= 2 else (
        3 if x > 2 and x <= 3 else (4 if x > 3 and x <= 4 else (
            5 if x > 4 and x <= 5 else (6 if x > 5 and x <= 6 else (7 if x > 6 and x <= 7 else 8)))))))
    values = []
    for i in data['oldpeak']:
        values.append(peak(i))
    data['OldpeakGroup'] = np.array(values)
    data = data.drop(['age', 'trestbps', 'chol', 'thalach', 'oldpeak'], axis=1)
    data = data.dropna()
    data = data.drop_duplicates()
    data.to_csv('media/result/heart_data_fused.csv')
    return len(list1),first_length, len(data)