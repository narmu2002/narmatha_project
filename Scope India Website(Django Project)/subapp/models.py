from django.db import models

class student(models.Model):
    datas= [('male','Male'), ('female', 'Female'), ('others','Others')]
    data1= [('india', 'India')]
    data2=[('Tamil Nadu','Tamil Nadu'),('Kerala','Kerala'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana'),
           ('Odisha','Odisha'),('Karnataka','Karnataka'),('Goa','Goa'),('Haryana','Haryana'),('Bihar','Bihar')]
    data3=[('Listening music','Listening music'), ('dancing','dancing'),('story writing','story writing'),
                   ('painting','painting'),('others','others')]
    data4=[('Kanniyakumari','Kanniyakumari'),('Tirunelveli','Tirunelveli'),('Thoothukudi','Thoothukudi'),('Chennai','Chennai'), ('Coimbatore','Coimbatore'),('Kanchipuram','Kanchipuram'),('Vellore','Vellore')]
    data5=[('Agasteeswaram','Agasteeswaram'),('Anjugramam','Anjugramam'),('Mylaudy','Mylaudy'),('Aralvaimozhi','Aralvaimozhi'),
           ('Boothapandi','Boothapandi'),('Azhagappapuram','Azhagappapuram'),('Colachel','Colachel')]
    name= models.CharField(max_length=100)
    age= models.IntegerField()
    email= models.EmailField()
    gender= models.CharField(max_length=100, choices=datas, null=True)
    date_of_birth= models.DateField()
    phone_number = models.CharField(max_length=15)
    country= models.CharField(choices=data1, null=True)
    state= models.CharField(choices=data2, null=True)
    district=models.CharField(choices=data4, null=True)
    city=models.CharField(choices=data5, null=True)
    hobbies= models.CharField(max_length=100,choices=data3, null=True, blank=False)
    file= models.FileField(blank=False, null=True, upload_to='mediafile')
    password = models.CharField(max_length=128, null=True, blank=True)  # To store hashed password or temp password
    
    class Meta:
        verbose_name_plural = "student"
    def __str__(self):
        return self.name
    

class TempUser(models.Model):
    email = models.EmailField(unique=True)
    temp_password = models.CharField(max_length=100)
    new_password = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.email
