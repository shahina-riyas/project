import numpy as np
import pandas as pd


def fuse_diabeticsdata(list1):
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
    data = data.drop(['Pregnancies'], axis=1)
    glucose = lambda x: 75 if x <= 75 else (100 if x > 75 and x <= 100 else (125 if x > 100 and x <= 125 else (
        150 if x > 125 and x <= 150 else (175 if x > 150 and x <= 175 else (
            200 if x > 175 and x <= 200 else (225 if x > 200 and x <= 225 else 250))))))
    value = []
    for i in data['Glucose']:
        value.append(glucose(i))
    data['GlucoseGroup'] = np.array(value)
    bp = lambda x: 'hypotension' if x < 60 else (
        'normal' if x >= 60 and x <= 80 else ('prehypertension' if x > 80 and x < 90 else 'hypertension'))
    value = []
    for i in data['BloodPressure']:
        value.append(bp(i))
    data['BloodPressureGroup'] = np.array(value)
    skin = lambda x: 0 if x <= 10 else (10 if x > 10 and x <= 20 else (20 if x > 20 and x <= 30 else (
        30 if x > 30 and x <= 40 else (40 if x > 40 and x <= 50 else (50 if x > 50 and x <= 60 else (
            60 if x > 60 and x <= 70 else (70 if x > 70 and x <= 80 else (
                80 if x > 80 and x <= 90 else (90 if x > 90 and x <= 100 else 100)))))))))
    value = []
    for i in data['SkinThickness']:
        value.append(skin(i))
    data['SkinThicknessGroup'] = np.array(value)
    insulin = lambda x: 0 if x <= 100 else (100 if x > 100 and x <= 200 else (200 if x > 200 and x <= 300 else (
        300 if x > 300 and x <= 400 else (400 if x > 400 and x <= 500 else (500 if x > 500 and x <= 600 else (
            600 if x > 600 and x <= 700 else (700 if x > 700 and x <= 800 else (
                800 if x > 800 and x <= 900 else (900 if x > 900 and x <= 1000 else 1000)))))))))
    value = []
    for i in data['Insulin']:
        value.append(insulin(i))
    data['InsulinGroup'] = np.array(value)
    bmi = lambda x: 'underweight' if x < 18.5 else (
        'normal' if x >= 18.5 and x <= 25 else ('overweight' if x > 25 and x < 30 else 'obesity'))
    values = []
    for i in data['BMI']:
        values.append(bmi(i))
    data['BMIGroup'] = np.array(values)
    pedigreefunction = lambda x: 0.75 if x <= 0.75 else (1 if x > 0.75 and x <= 1 else (
        1.25 if x > 1 and x <= 1.25 else (1.25 if x > 1.25 and x <= 1.5 else (1.5 if x > 1.5 and x <= 1.75 else (
            1.75 if x > 1.75 and x <= 2.00 else (2.00 if x > 2.00 and x <= 2.25 else (
                2.25 if x > 2.25 and x <= 2.50 else (2.50 if x > 2.75 and x <= 3.00 else 3.00))))))))
    value = []
    for i in data['DiabetesPedigreeFunction']:
        value.append(pedigreefunction(i))
    data['DiabetesPedigreeFunctionGroup'] = np.array(value)
    age = lambda x: 'children' if x >= 0 and x <= 6 else ('adolescents' if x > 6 and x <= 12 else (
        'teens' if x > 12 and x <= 19 else ('young adults' if x > 19 and x <= 35 else (
            'middle-aged adults' if x > 35 and x <= 55 else 'older adults'))))
    value = []
    for i in data['Age']:
        value.append(age(i))
    data['AgeGroup'] = np.array(value)
    data = data.drop(['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'],
                     axis=1)
    data = data.dropna()
    data = data.drop_duplicates()
    data.to_csv('media/result/data_liver_fused.csv')
    return len(list1),first_length, len(data)