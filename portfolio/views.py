from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import os
from .remove_files import remove_files
from .exposure_fusion import align_images, exposure_fusion
import pandas as pd
import datetime
import cv2
from .fuse_heart_data import fuse_heartdata
from .fuse_liver_data import fuse_liverdata
from .fuse_diabetics_data import fuse_diabeticsdata

cwd = os.getcwd()


# Create your views here.


@login_required(login_url='login-h')
def home(request):
    return render(request, 'index.html')


def loginpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        except:
            messages.warning("Fill the details")
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login-h')
    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login-h')


def add_patient(request):
    last_patient.objects.all().delete()
    part = Body_part.objects.all()
    gender = Gender.objects.all()
    if request.method == 'POST':
        form = detail_form(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['Name']
            Age = form.cleaned_data['Age']
            phonenumber = form.cleaned_data['phonenumber']
            Sex = form.cleaned_data['Sex']
            bodypart = form.cleaned_data['part']
            bodypart = bodypart.lower()
            print(bodypart)
            bpart = Body_part.objects.get(part=bodypart)
            gen = Gender.objects.get(gender=Sex)
            var1 = last_patient(Name=name, phonenumber=phonenumber, part=bpart)
            var1.save()
            variable = scanning_reports(Date=datetime.datetime.now(), Name=name, Age=Age, phonenumber=phonenumber,
                                        Sex=gen)
            variable.save()
            if bodypart == 'brain':
                remove_files(cwd + '/media/Brain')
            elif bodypart == 'lungs':
                remove_files(cwd + '/media/Lungs')
            else:
                remove_files(cwd + '/media/Files')
            return render(request, 'addpatients.html', {'part': part, 'gender': gender, 'msg': 'Successfully added'})
    return render(request, 'addpatient.html', {'part': part, 'gender': gender})


def imagefusion(request):
    count_model.objects.all().delete()
    if request.method == 'POST':
        form = count_form(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            print(count)
            var = count_model(count=count)
            var.save()
            form1 = file_forms(request.POST)
            count = int(count)
            print(os.getcwd())
            list1 = []
            lastpatient = last_patient.objects.all().last()
            if count < 0:
                if str(lastpatient.part) == 'brain':
                    return render(request, 'bimagefusion.html')
                elif str(lastpatient.part) == 'lungs':
                    return render(request, 'imagefusion.html')
                else:
                    return render(request, 'imagefusion.html')
            if request.method == 'POST':
                count = count - 1
                if str(lastpatient.part) == 'brain':
                    form = brain_forms(request.POST, request.FILES)
                    dir = cwd + '/media/Brain'
                elif str(lastpatient.part) == 'lungs':
                    form = lungs_forms(request.POST, request.FILES)
                    dir = cwd + '/media/Lungs'
                else:
                    form = file_forms(request.POST, request.FILES)
                    dir = cwd + '/media/Files'
                if count < 0:
                    if str(lastpatient.part) == 'brain':
                        return render(request, 'bimagefusion.html')
                    elif str(lastpatient.part) == 'lungs':
                        return render(request, 'imagefusion.html')
                    else:
                        return render(request, 'imagefusion.html')
                if form.is_valid():
                    form.save()
                    if count < 0:
                        if str(lastpatient.part) == 'brain':
                            return render(request, 'bimagefusion.html')
                        elif str(lastpatient.part) == 'lungs':
                            return render(request, 'imagefusion.html')
                        else:
                            return render(request, 'imagefusion.html')
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            path = os.path.join(dir, file)
                            print(path)
                            list1.append(path)
                        print(len(list1))
                        if count < 0:
                            if str(lastpatient.part) == 'brain':
                                return render(request, 'bimagefusion.html')
                            elif str(lastpatient.part) == 'lungs':
                                return render(request, 'imagefusion.html')
                            else:
                                return render(request, 'imagefusion.html')

            return render(request, 'imageupload.html', {'form': form1, 'count': count})
    return render(request, 'image.html')


def brain_merge(request):
    v = last_patient.objects.all()
    for i in v:
        pass
    else:
        var = scanning_reports.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber).order_by('-Date')[0]
    images = []
    part = []
    fusion1 = [[[]]]
    rootdir = cwd + '/media/Brain'
    i = last_patient.objects.all().last()
    print(i)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img = cv2.imread(os.path.join(subdir, file))
            img = cv2.resize(img, (500, 500))
            images.append(img)
            cv2.imshow('img', img)
            cv2.waitKey(0)
    else:
        fusion1 = exposure_fusion(images, depth=3, time_decay=4)
        print(fusion1)
        print(type(fusion1))
        filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(cwd + '/media/output/' + filename1 + '.jpg', fusion1)
        cv2.imwrite(cwd + '/static/output/output.jpg', fusion1)

        if str(i.part) == 'brain':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 brain=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('brain')
        elif str(i.part) == 'lungs':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 lungs=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('lungs')
        else:
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 stomach=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('stomach')
        var.delete()
    return render(request, 'final.html', {'file': cwd + '/static/output/output.jpg'})


def merge(request):
    v = last_patient.objects.all()
    for i in v:
        pass
    else:
        var = scanning_reports.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber).order_by('-Date')[0]
    images = []
    part = []
    fusion1 = [[[]]]
    rootdir = cwd + '/media/Files'
    i = last_patient.objects.all().last()
    print(i)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img = cv2.imread(os.path.join(subdir, file))
            img = cv2.resize(img, (500, 500))
            images.append(img)
            cv2.imshow('img', img)
            cv2.waitKey(0)
    else:
        fusion1 = exposure_fusion(images, depth=3, time_decay=4)
        print(fusion1)
        print(type(fusion1))
        filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(cwd + '/media/output/' + filename1 + '.jpg', fusion1)
        cv2.imwrite(cwd + '/static/output/output.jpg', fusion1)

        if str(i.part) == 'brain':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 brain=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('brain')
        elif str(i.part) == 'lungs':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 lungs=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('lungs')
        else:
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 stomach=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('stomach')
        var.delete()
    return render(request, 'final.html', {'file': cwd + '/static/output/output.jpg'})


def lung_merge(request):
    v = last_patient.objects.all()
    for i in v:
        pass
    else:
        var = scanning_reports.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber).order_by('-Date')[0]
    images = []
    part = []
    fusion1 = [[[]]]
    rootdir = cwd + '/media/Lungs'
    i = last_patient.objects.all().last()
    print(i)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img = cv2.imread(os.path.join(subdir, file))
            img = cv2.resize(img, (500, 500))
            images.append(img)
            cv2.imshow('img', img)
            cv2.waitKey(0)
    else:
        fusion1 = exposure_fusion(images, depth=3, time_decay=4)
        print(fusion1)
        print(type(fusion1))
        filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(cwd + '/media/output/' + filename1 + '.jpg', fusion1)
        cv2.imwrite(cwd + '/static/output/output.jpg', fusion1)

        if str(i.part) == 'brain':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 brain=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('brain')
        elif str(i.part) == 'lungs':
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 lungs=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('lungs')
        else:
            b = scanning_reports(Date=datetime.datetime.now(), Name=i.Name, Age=var.Age,
                                 phonenumber=i.phonenumber,
                                 Sex=var.Sex,
                                 stomach=cwd + '/media/output/' + filename1 + '.jpg')
            b.save()
            part.append('stomach')
        var.delete()
    return render(request, 'final.html', {'file': cwd + '/static/output/output.jpg'})


def history(request):
    var = None
    part = []
    last_patient.objects.all().delete()
    if request.method == 'POST':
        form = patient_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            phonenumber = form.cleaned_data['phonenumber']
            bodypart = form.cleaned_data['part']
            print(bodypart)
            variable1 = scanning_reports.objects.filter(Name=name).filter(phonenumber=phonenumber)
            if len(variable1) == 0:
                try:
                    var = patient_brain.objects.filter(Name=name).filter(phonenumber=phonenumber).order_by('-Date')[0]
                    variable = patient_brain.objects.filter(Name=name).filter(phonenumber=phonenumber)
                    for i in variable:
                        if i != var:
                            i.delete()
                except:
                    print('pass')
                bodypart = Body_part.objects.get(part=bodypart)
                var1 = last_patient(Name=name, phonenumber=phonenumber, part=bodypart)
                var1.save()
                print(var1)
                return render(request, 'history1.html', {'patient': var})
            else:
                var = scanning_reports.objects.filter(Name=name).filter(phonenumber=phonenumber).order_by('-Date')[0]
                variable = patient_brain.objects.filter(Name=name).filter(phonenumber=phonenumber)
                for i in variable:
                    i.delete()
                bodypart = Body_part.objects.get(part=bodypart)
                var1 = last_patient(Name=name, phonenumber=phonenumber, part=bodypart)
                var1.save()
                bodypart = str(bodypart)
                print(var1)
                print(bodypart)
                part.append(bodypart)
                return render(request, 'history2.html', {'patient': var, 'part': part})
    part = Body_part.objects.all()
    return render(request, 'history.html', {'part': part})


def department(request):
    return render(request, 'department.html')


def heart(request):
    var = department_model(department='heart')
    var.save()
    return redirect('addmore')


def liver(request):
    var = department_model(department='liver')
    var.save()
    return redirect('addmore')


def diabetics(request):
    var = department_model(department='diabetics')
    var.save()
    return redirect('addmore')


def heart_disease(request):
    dir = cwd + '/media/data'
    list1 = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            list1.append(path)
    num, first, last = fuse_heartdata(list1)
    return render(request, 'department1.html', {'num': num, 'first': first, 'last': last})


def liver_disease(request):
    dir = cwd + '/media/data'
    list1 = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            list1.append(path)
    num, first, last = fuse_liverdata(list1)
    return render(request, 'department1.html', {'num': num, 'first': first, 'last': last})


def diabetics_disease(request):
    dir = cwd + '/media/data'
    list1 = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            list1.append(path)
    num, first, last = fuse_diabeticsdata(list1)
    return render(request, 'department1.html', {'num': num, 'first': first, 'last': last})


def addmore(request):
    dir = cwd + '/media/data'
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            print(path)
            os.remove(path)
    if request.method == 'POST':
        form = uploading_form(request.POST)
        if form.is_valid():
            filecount = form.cleaned_data['filecount']
            var = uploading_details(filecount=filecount)
            var.save()
            v1 = uploaded_file_details(input=int(filecount))
            v1.save()
            return redirect('upload')
    return render(request, 'addmore.html')


def upload(request):
    var = uploaded_file_details.objects.all().last()
    count = var.input
    form = FilesUploadForm(request.POST)
    form1 = count_form(request.POST)
    if request.method == 'POST':
        form = FilesUploadForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            count = form1.cleaned_data['count']
            form.save()
            print(count)
            count = int(count) - 1
            if count <= 0:
                detvar = department_model.objects.all().last()
                depatment = detvar.department
                if depatment == 'heart':
                    return redirect('heart_disease')
                if depatment == 'liver':
                    return redirect('liver_disease')
                if depatment == 'diabetics':
                    return redirect('diabetics_disease')
            return render(request, 'upload.html', {'form': form, 'count': str(count)})
    return render(request, 'upload.html', {'form': form, 'count': int(count)})


def det1(request):
    if request.method == 'POST':
        form = add_patients_form(request.POST or None)
        if form.is_valid():
            BloodSugarBefore = form.cleaned_data['BloodSugarBefore']
            BloodSugarAfter = form.cleaned_data['BloodSugarAfter']
            MaximumHeartRate = form.cleaned_data['MaximumHeartRate']
            smoking_status = form.cleaned_data['smoking_status']
            if BloodSugarBefore == '0':
                BloodSugarBefore = None
            if BloodSugarAfter == '0':
                BloodSugarAfter = None
            if MaximumHeartRate == '0':
                MaximumHeartRate = None
            if smoking_status == '0':
                smoking_status = None
            pat = patient.objects.all().last()
            pvar = patient(Date=pat.Date, Name=pat.Name, Age=pat.Age, phonenumber=pat.phonenumber, Sex=pat.Sex,
                           BloodPressure=pat.BloodPressure,
                           SkinThickness=pat.SkinThickness, Insulin=pat.Insulin, BMI=pat.BMI,
                           DiabetesPedigreeFunction=pat.DiabetesPedigreeFunction,
                           ChestPainType=pat.ChestPainType,BloodSugarBefore=BloodSugarBefore, BloodSugarAfter=BloodSugarAfter,
                        MaximumHeartRate=MaximumHeartRate, smoking_status=smoking_status)
            pvar.save()
            pat.delete()
            return render(request, 'det1.html', {'msg': 'Successfully stored'})
    return render(request, 'det1.html')


def det(request):
    pain = pain_type.objects.all()
    if request.method == 'POST':
        form = add_patient_form(request.POST or None)
        if form.is_valid():
            BloodPressure = form.cleaned_data['BloodPressure']
            SkinThickness = form.cleaned_data['SkinThickness']
            Insulin = form.cleaned_data['Insulin']
            BMI = form.cleaned_data['BMI']
            DiabetesPedigreeFunction = form.cleaned_data['DiabetesPedigreeFunction']
            ChestPainType = form.cleaned_data['pain']
            if BloodPressure == '0':
                BloodPressure = None
            if SkinThickness == '0':
                SkinThickness = None
            if Insulin == '0':
                Insulin = None
            if BMI == '0':
                BMI = None
            if DiabetesPedigreeFunction == '0':
                DiabetesPedigreeFunction = None
            pat = patient.objects.all().last()
            pain = pain_type.objects.get(pain=ChestPainType)
            pvar = patient(Date=pat.Date, Name=pat.Name, Age=pat.Age, phonenumber=pat.phonenumber, Sex=pat.Sex,BloodPressure=BloodPressure,
                        SkinThickness=SkinThickness, Insulin=Insulin, BMI=BMI,
                        DiabetesPedigreeFunction=DiabetesPedigreeFunction,
                        ChestPainType=pain)
            pvar.save()
            pat.delete()
            return redirect('det1')
    return render(request, 'det.html',{'pain':pain})


def details(request):
    last_patient.objects.all().delete()
    gender = Gender.objects.all()
    if request.method == 'POST':
        form = details_form(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['Name']
            Age = form.cleaned_data['Age']
            phonenumber = form.cleaned_data['phonenumber']
            Sex = form.cleaned_data['Sex']
            gen = Gender.objects.get(gender=Sex)
            v = patient(Date=datetime.datetime.now(), Name=name, Age=Age, phonenumber=phonenumber, Sex=gen)
            v.save()
            b = last_patient(Name=name, phonenumber=phonenumber)
            b.save()
            return redirect('det')
    return render(request, 'detail.html', {'gender': gender})


def hisdata(request):
    last_patient.objects.all().delete()
    if request.method == 'POST':
        form = patient_detail_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            phonenumber = form.cleaned_data['phonenumber']
            print(name)
            print(phonenumber)
            var1 = last_patient(Name=name, phonenumber=phonenumber)
            var1.save()
            return render(request, 'hisdata.html', {'msg': 'Successfully stored'})
    return render(request, 'hisdata.html')


def merge_data(request):
    v = last_patient.objects.all()
    print('v is',v)
    for i in v:
        print(i)
    else:
        var = patient.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber)
        print(len(var))
        if len(var) == 0:
            return render(request, 'pat_detail.html', {'patient': None})
        elif len(var) == 1:
            return render(request, 'pat_detail.html', {'patient': var})
        else:
            for i in var:
                print(i.Age)
            df = pd.DataFrame(list(patient.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber).values()))
            df = df.fillna(method='ffill')
            df = df.fillna(method='bfill')
            df = df.drop(['id', 'Name', 'Age', 'phonenumber'], axis=1)
            df = df.sort_values(by='Date', ascending=False)
            df = df.drop(['Date'], axis=1)
            print(df.duplicated())
            df = df.drop_duplicates()
            print(df)
            print(len(df))
            variable = patient.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber).order_by('-Date')[
                       0:len(df)]
            new = patient.objects.filter(Name=i.Name).filter(phonenumber=i.phonenumber)
            if len(variable) != 0 and len(new) != 0:
                for val in new:
                    if val not in variable:
                        val.delete()
            return render(request, 'pat_detail.html', {'patient': variable})
    return render(request, 'pat_detail.html', {'patient': var})
