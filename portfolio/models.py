from django.db import models

# Create your models here.


class pain_type(models.Model):
    pain = models.CharField(max_length=50)


class Gender(models.Model):
    gender = models.CharField(max_length=50)

    def __str__(self):
        return str(self.gender)


class Body_part(models.Model):
    part = models.CharField(max_length=50)

    def __str__(self):
        return str(self.part)


class count_model(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return str(self.count)


class patient(models.Model):
    Date = models.DateField()
    Name = models.CharField(max_length=50)
    Age = models.IntegerField()
    phonenumber = models.IntegerField()
    Sex = models.ForeignKey(Gender, on_delete=models.CASCADE)
    BloodPressure = models.IntegerField(null=True, blank=True)
    SkinThickness = models.IntegerField(null=True, blank=True)
    Insulin = models.IntegerField(null=True, blank=True)
    BMI = models.IntegerField(null=True, blank=True)
    DiabetesPedigreeFunction = models.IntegerField(null=True, blank=True)
    ChestPainType = models.ForeignKey(pain_type, on_delete=models.CASCADE, null=True, blank=True)
    BloodSugarBefore = models.IntegerField(null=True, blank=True)
    BloodSugarAfter = models.IntegerField(null=True, blank=True)
    MaximumHeartRate = models.IntegerField(null=True, blank=True)
    smoking_status = models.IntegerField(null=True, blank=True)
    HeartPatient = models.IntegerField(null=True, blank=True)
    DiabeticPatient = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Name +" " + str(self.phonenumber)


class scanning_reports(models.Model):
    Date = models.DateField()
    Name = models.CharField(max_length=50)
    Age = models.IntegerField()
    phonenumber = models.IntegerField()
    Sex = models.ForeignKey(Gender, on_delete=models.CASCADE)
    brain = models.FileField('Brain/', null=True, blank=True)
    lungs = models.FileField('Lungs/', null=True, blank=True)
    stomach = models.FileField('Stomach/', null=True, blank=True)

    def __str__(self):
        return self.Name + " " + str(self.phonenumber)


class patient_brain(models.Model):
    Date = models.DateField()
    Name = models.CharField(max_length=50)
    Age = models.IntegerField()
    phonenumber = models.IntegerField()
    mri1 = models.FileField('Previous/Brain/MRI')
    mri2 = models.FileField('Previous/Brain/MRI')
    scan1 = models.FileField('Previous/Brain/Scan')
    scan2 = models.FileField('Previous/Brain/Scan')

    def __str__(self):
        return self.Name + " " + str(self.phonenumber)


class last_patient(models.Model):
    Name = models.CharField(max_length=50)
    phonenumber = models.IntegerField()
    part = models.ForeignKey(Body_part, on_delete=models.CASCADE,null=True,blank=True)


class file_model(models.Model):
    file = models.FileField(upload_to='Files/')


class brain_model(models.Model):
    file = models.FileField(upload_to='Brain/')


class lung_model(models.Model):
    file = models.FileField(upload_to='Lungs/')


class data_model(models.Model):
    file = models.FileField(upload_to='CSV/')


class department_model(models.Model):
    department = models.CharField(max_length=150)


class uploaded_file_details(models.Model):
    input = models.IntegerField(null=True, blank=True)
    output = models.IntegerField(null=True, blank=True)


class csv_file(models.Model):
    filename = models.FileField(upload_to='data/')

    class Meta:
        verbose_name = 'filename'
        verbose_name_plural = 'filenames'

    def __str__(self):
        return self.filename.url
