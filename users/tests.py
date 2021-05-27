from django.test import TestCase
from users.models import Profile
from django.contrib.auth.models import User # help us fake user
from datetime import date

#forms, views, models

class TestProfilePersonal(TestCase):
	def setUp(self):
		#fake google user
		googleUser = User.objects.create_user('randomUser')
		#googleUser.save()

		myProfile = Profile.objects.create(user = googleUser, name="steven bowers", email="sbowers@virginia.edu", bio="I know about	Integrated Circuits", birthday=date.today(),
			graduation_year=2050, gender="Male", my_car_status="I have a car")

	def testUsername(self):
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.user.username, 'randomUser' )

	def testName(self):
		#current = User.objects.create_user('randomUser')
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.name, "steven bowers")

	def testEmail(self):
		#current = User.objects.create_user('randomUser')
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.email, "sbowers@virginia.edu")

	def testBio(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.bio, "I know about	Integrated Circuits")

	def testBirthday(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.birthday, date.today())

	def testGraduationYear(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.graduation_year, 2050)

	def testGender(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.gender, "Male")

	def testGender(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.my_car_status, "I have a car")

class TestProfilePersonalDefault(TestCase):
	def setUp(self):
		
		#fake google user
		googleUser = User.objects.create_user('coolUser')
		#googleUser.save()

		myProfile = Profile.objects.create(user = googleUser)

	def testDefaultUsername(self):
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.user.username, 'coolUser' )

	def testDefaultName(self):
		#current = User.objects.create_user('randomUser')
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.name, None)

	def testDefaultEmail(self):
		#current = User.objects.create_user('randomUser')
		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.email, None)

	def testDefaultBio(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.bio, 'Click Edit Profile to write your bio!')

	def testDefaultBirthday(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.birthday, date.today())

	def testDefaultGraduationYear(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.graduation_year, 2022)

	def testDefaultGender(self):

		getMyProfile = Profile.objects.get_queryset()[0]

		self.assertEqual(getMyProfile.my_car_status, 'No Car Status Specified Yet')

#15 tests
#class CheckingProfileForm(TestCase):
	#def context(self):
		#myUser = User.objects.create_user('myUser')
		#Profile.objects.create(user=myUser, name="")