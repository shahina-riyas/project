from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class count_form(forms.Form):
    count = forms.CharField(max_length=1)


class data_forms(forms.ModelForm):
    class Meta:
        model = data_model
        fields = ['file']


class uploading_details(models.Model):
    filecount = models.IntegerField()


class uploading_form(forms.Form):
    filecount = forms.IntegerField()


class detailed_file(models.Model):
    header = models.IntegerField(null=True, blank=True)
    coulmn_names = models.CharField(max_length=500)
    personal = models.CharField(max_length=500, null=True, blank=True)
    date = models.CharField(max_length=500, null=True, blank=True)


'''


class data_forms(forms.ModelForm):
    class Meta:
        model = data_model
        fields = ['file']'''


class patient_form(forms.Form):
    Name = forms.CharField(max_length=50)
    phonenumber = forms.CharField(max_length=10)
    part = forms.CharField(max_length=10)


class detail_form(forms.Form):
    Name = forms.CharField(max_length=50)
    Age = forms.CharField(max_length=2)
    phonenumber = forms.CharField(max_length=10)
    Sex = forms.CharField(max_length=15)
    part = forms.CharField(max_length=10)


class details_form(forms.Form):
    Name = forms.CharField(max_length=50)
    Age = forms.CharField(max_length=2)
    phonenumber = forms.CharField(max_length=10)
    Sex = forms.CharField(max_length=15)


class patient_detail_form(forms.Form):
    Name = forms.CharField(max_length=50)
    phonenumber = forms.CharField(max_length=10)


class add_patient_form(forms.Form):
    BloodPressure = forms.CharField(max_length=10)
    SkinThickness = forms.CharField(max_length=10)
    Insulin = forms.CharField(max_length=10)
    BMI = forms.CharField(max_length=10)
    DiabetesPedigreeFunction = forms.CharField(max_length=10)
    pain = forms.CharField(max_length=20)


class add_patients_form(forms.Form):
    BloodSugarBefore = forms.CharField(max_length=10)
    BloodSugarAfter = forms.CharField(max_length=10)
    MaximumHeartRate = forms.CharField(max_length=10)
    smoking_status = forms.CharField(max_length=10)


class file_forms(forms.ModelForm):
    class Meta:
        model = file_model
        fields = ['file']


class brain_forms(forms.ModelForm):
    class Meta:
        model = brain_model
        fields = ['file']


class lungs_forms(forms.ModelForm):
    class Meta:
        model = lung_model
        fields = ['file']


class FilesUploadForm(forms.ModelForm):
    class Meta:
        model = csv_file
        fields = ['filename']


