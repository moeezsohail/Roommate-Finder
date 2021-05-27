from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect


def home(request):

	#user = User.objects.get(username = request.user)

	if request.user.is_anonymous:
		#return HttpResponseRedirect(reverse('home'))
		return render(request, 'roommate_app/home.html')
	else:
		return HttpResponseRedirect(reverse('roommate_app:index'))
		#return render(request, "roommate_app/home.html")


		# adding test site
