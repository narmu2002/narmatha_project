from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class studentform(forms.Form):
    name= forms.CharField(max_length=100)
    age= forms.IntegerField()
    email= forms.EmailField()
    gender= forms.CharField(widget=forms.RadioSelect(choices=[('male','Male'), ('female', 'Female'), ('others','Others')]))
    date_of_birth= forms.DateField()
    phone_number = forms.CharField(max_length=15)
    country= forms.CharField(widget=forms.Select(choices=[('india', 'India')]))
    state= forms.CharField(widget=forms.Select(choices=[('Tamil Nadu','Tamil Nadu'),('Kerala','Kerala'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana'),('Odisha','Odisha'),('Karnataka','Karnataka'),('Goa','Goa'),('Haryana','Haryana'),('Bihar','Bihar')]))
    district=forms.CharField(widget=forms.Select(choices=[('Kanniyakumari','Kanniyakumari'),('Tirunelveli','Tirunelveli'),('Thoothukudi','Thoothukudi'),('Chennai','Chennai'), ('Coimbatore','Coimbatore'),('Kanchipuram','Kanchipuram'),('Vellore','Vellore')]))
    city=forms.CharField(widget=forms.Select(choices=[('Agasteeswaram','Agasteeswaram'),('Anjugramam','Anjugramam'),('Mylaudy','Mylaudy'),('Aralvaimozhi','Aralvaimozhi'),('Boothapandi','Boothapandi'),('Azhagappapuram','Azhagappapuram'),('Colachel','Colachel')]))
    hobbies= forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[('Listening music','Listening music'), ('dancing','dancing'),('story writing','story writing'),('painting','painting'),('others','others')]))
    file= forms.FileField(required=False)
    
def clean(self) ->dict[str,any]:
       name=self.cleaned_data['name']
       age=self.cleaned_data['age']
       email=self.cleaned_data['email']
       gender=self.cleaned_data['gender']
       date_of_birth=self.cleaned_data['date_of_birth']
       phone_number=self.cleaned_data['phone_number']
       country=self.cleaned_data['country']
       state=self.cleaned_data['state']
       hobbies=self.cleaned_data['hobbies']
       file=self.cleaned_data['file']
        
       if name.islower():
           self.add_error('name', 'Name not in small letter')
       if age<=18:
           self.add_error('age', 'Age is not allowed')
       if email and not email.endswith("@gmail.com"):
           self.add_error('email', 'Email must be a gmail address.')
       valid_genders= ['male','female','others']
       if gender and gender not in valid_genders:
           self.add_error('gender', 'Invalid gender selection.')
       if file.size >2 * 1024 * 1024:
              self.add_error('file',"Files size should not exceed 2mb.")
              return self.cleaned_data


User = get_user_model()    
class loginform(forms.Form):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                stu = student.objects.get(email=username)
            except student.DoesNotExist:
                raise ValidationError("No student found with this email address.")

            # You can also check password validity here (if stored in plain text — not recommended)
            if stu.password != password:
                raise ValidationError("Incorrect password.")
        
        return cleaned_data
