from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile



class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    birthday = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))#forms.DateField(widget = forms.SelectDateWidget)

    bio = forms.CharField(label="Description", widget=forms.Textarea(attrs={'rows':3}))

    #BUDGET_RANGE = [(i,i) for i in range(2000)]

    GENDER_CHOICES = (
    	('NB','Non-binary'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CAR_STATUS_CHOICES = (
        ('Has car', 'I have a car'),
        ('Does not have car', 'No, I do not have a car'),
    )

    LOCATION_CHOICES = (
		('On-Grounds', 'On-Grounds'),
		('Off-Grounds', 'Off-Grounds'),
	)

    
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    my_car_status = forms.ChoiceField(choices=CAR_STATUS_CHOICES)
    location = forms.ChoiceField(choices=LOCATION_CHOICES)


    budget = forms.IntegerField(min_value=1, max_value=2000)
    noise_level = forms.IntegerField(min_value=1, max_value=20)
    graduation_year = forms.IntegerField(label="Graduating", min_value=2021, max_value=2050)

    class Meta:
        model = Profile
        fields = ['name', 'email', 'bio', 'gender', 'birthday', 'graduation_year', 'location', 'budget', 'noise_level', 'my_car_status','image']


class ProfilePreferencesForm(forms.ModelForm):
	#add all the preferences that you want from the profile here
	#see Forms in django documentation
	# minimum_age = models.BigIntegerField(default=18)
	# maximum_age = models.BigIntegerField(default=30)
	# budget_low = models.BigIntegerField(default=0)
	# budget_high = models.BigIntegerField(default= 500)
	# noise_minimum = models.BigIntegerField(default= 5)
	# noise_maximum = models.BigIntegerField(default= 5)
	# preferred_gender = models.CharField(default=None, max_length=255, null=True)
	# location_preference = models.CharField(default=None, max_length=255, null=True)
	# car_status = models.CharField(default=None, max_length=255, null=True)
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	CAR_STATUS_CHOICES = (
        ('Has car', 'Have a car'),
        ('Does not have car', 'Do not have a car'),
    )
	LOCATION_CHOICES = (
        ('On-Grounds', 'On-Grounds'),
		('Off-Grounds', 'Off-Grounds'),
    )

	preferred_gender = forms.ChoiceField(choices=GENDER_CHOICES)
	car_status = forms.ChoiceField(choices=CAR_STATUS_CHOICES)
	location_preference = forms.ChoiceField(choices=LOCATION_CHOICES)

	class Meta:
		model = Profile 
		fields = ['minimum_age', 'maximum_age', 'budget_low', 'budget_high', 'noise_minimum','noise_maximum','preferred_gender','car_status' , 'location_preference', 'graduation_year_preference']


#class ProfileRoommatePreferenceForm(forms.ModelForm):
	# same as above

	#class Meta:
		#model = Profile
		#frieleds =  #write the preferences that you want your roommate to have
