
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from datetime import datetime  
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import os
from django.contrib import messages
from .models import Profile, Roommate_Request, Match, Post
from .forms import ProfileUpdateForm, ProfilePreferencesForm
from django.core.paginator import Paginator
from groupy.client import Client
from groupy.api.messages import DirectMessages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

"""
*  REFERENCES
*  Title: Django-Blog Tutorial
*  Author: Corey M Schafer
*  Date: 2018
*  URL: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*
*
*  Title: DStep by Step guide to add friends with Django
*  Author: Abhik
*  Date: October 2020
*  URL: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
*
"""


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'picture']

    def form_valid(self, form):
    	post = form.save(commit=False)
    	form.instance.author = self.request.user.profile
    	post.save()
    	return super().form_valid(form)

@login_required
def searchingAll(request):
	template_name = 'users/searchAll.html'

	all_profiles_list = Profile.objects.exclude(user=request.user)
	if len(list(all_profiles_list)) == 0 :
		flag = False
	else :
		flag = True
	
	return render(request, template_name, {'all_profiles': all_profiles_list})

@login_required
def searching(request):
	template_name = 'users/search.html'

	#using paginator
	user = User.objects.get(username=request.user)
	profile = Profile.objects.get(user=user)

	all_profiles_list = Profile.objects.exclude(user=request.user)

	filters = ["graduation_year", "gender", "my_car_status", "noise_level", "location", "budget"]

	for each_profile in all_profiles_list:

		if Match.objects.filter(this_profile=profile, with_profile=each_profile).exists():

			Match.objects.filter(this_profile=profile, with_profile=each_profile).delete()
		
		Match.objects.create(this_profile=profile, with_profile=each_profile)

		currentMatch = Match.objects.get(this_profile=profile, with_profile=each_profile)


		for attribute_name in filters:

		
			if(getattr(each_profile, attribute_name) == getattr(profile, attribute_name)):
				currentMatch.similarity_tokens+= 1

		currentMatch.similarity_tokens = (currentMatch.similarity_tokens/len(filters))*100
		currentMatch.save()



	all_matches = Match.objects.all()
	match_list  = all_matches.filter(this_profile=profile)
	all_profiles_list = match_list.order_by('-similarity_tokens')

	all_profiles = all_profiles_list

	"""
	paginator = Paginator(all_profiles_list,1)

	try:
		page = int(request.GET.get('page','1'))
	except:
		page = 1

	try:
		all_profiles = paginator.page(page)
	except(EmptyPage, InvalidPage):
		all_profiles = paginator.page(paginator.num_pages)
	"""

	return render(request, template_name, {'all_profiles': all_profiles})

#login NOT required
@login_required
def view_profile(request, userID):
	template_name= 'users/view_profile.html'

	user = User.objects.get(id=userID)
	profile = Profile.objects.filter(user=user).first()

	return render(request, template_name, {'profile': profile})



@login_required
def loadFriendRequests(request):
	template_name = 'users/friend_requests.html'

	user = request.user
	#all_profiles = Profile.objects.all()
	#all_user_friends = request.user.profile.friends
	all_friend_requests = Roommate_Request.objects.filter(to_profile=request.user.profile)

	return render(request, template_name, {'user': user, 'all_friend_requests': all_friend_requests})


@login_required
def loadFriendPage(request):
	template_name = 'users/friends.html'

	user = request.user
	#all_profiles = Profile.objects.all()
	#all_friend_requests = Roommate_Request.objects.all()

	all_friends = request.user.profile.friends.all()

	return render(request, template_name, {'user': user, 'all_friends': all_friends})


@login_required
def loadMainPage(request):
	template_name = 'roommate_app/index.html'
	
	user = request.user
	
	all_posts = Post.objects.all().order_by('-date_posted')


	return render(request, template_name, {'user': user, 'all_posts': all_posts})


@login_required
def send_roommate_request(request, userID):

	from_profile = request.user.profile

	user = User.objects.get(id=userID)
	to_profile = Profile.objects.filter(user=user).first()

	roommate_request, created = Roommate_Request.objects.get_or_create(from_profile=from_profile, to_profile=to_profile)

	all_profiles = Profile.objects.all()
	all_friend_requests = Roommate_Request.objects.all()

	if created:
		messages.success(request, f'friend request sent to ' + str(roommate_request.to_profile.name))

	else:
		messages.warning(request, str(roommate_request.to_profile.name) + ' has yet to respond to your first roommate request')

	
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def accept_roommate_request(request, requestID):
	
	all_profiles = Profile.objects.all()


	roommate_request = Roommate_Request.objects.get(id=requestID)

	
	all_friend_requests = Roommate_Request.objects.all()

	if roommate_request.to_profile == request.user.profile:
		roommate_request.to_profile.friends.add(roommate_request.from_profile)
		roommate_request.from_profile.friends.add(roommate_request.to_profile)
		roommate_request.delete()

		messages.success(request, f'friend request was accepted')
	else:

		messages.warning(request, f'friend request was not accepted')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def preferences(request):
	template_name = 'users/preferences.html'

	if request.method == 'POST':

		preference_form = ProfilePreferencesForm(request.POST, request.FILES, instance=request.user.profile)

		if preference_form.is_valid():

			preference_form.save()
			messages.success(request, f'Your preferences were updated')

			return render(request, template_name, {'preference_form': preference_form})

	else:

		preference_form = ProfilePreferencesForm(instance=request.user.profile)

		return render(request, template_name, {'preference_form': preference_form})

@login_required
def profile(request):
	template_name = 'users/profile.html'

	if request.method == 'POST':

		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if p_form.is_valid():

			p_form.save()
			messages.success(request, f'Your account has been updated!')

			return render(request, template_name, {'p_form': p_form})

	else:
		p_form = ProfileUpdateForm(instance=request.user.profile)

		all_profiles = Profile.objects.all()

		all_friend_requests = Roommate_Request.objects.all()

		return render(request, template_name, {'p_form': p_form, 'all_profiles': all_profiles, 'all_friend_requests': all_friend_requests})

class Message:
	def __init__(self, name, userSent, text):
		self.name = name
		self.userSent = userSent
		self.text = text


@login_required
def chat(request, userID=None):
	template_name = 'users/chat.html'
	if request.user.profile.chat_token is None:
		# User needs to enable groupme
		return render(request, template_name, {"client_id": os.environ.get('GROUP_API', "seRnQpG01SrTr4Bv4U440RbN1I1pIKSOkNfDXKsdwHZzEMmS")})

	# Create groupme client
	client = Client.from_token(request.user.profile.chat_token)
	# Join the roommate group (required to send dm's)
	groupid = os.environ.get('GROUP_ID', "67775296")
	groupkey = os.environ.get('GROUP_KEY', "eGoKivft")
	client.groups.join(groupid, groupkey)

	if userID is None:
		# If no user specified use the roommate groupchat
		#group = client.groups.get(groupid)
		messages = []
		#for message in group.messages.list_all():
			#messages.append(message.name + ": " + message.text)
		#messages = messages[::-1]
		return render(request, template_name, {"chat": messages, "other_id": ""})
	else:
		# Get the other users Groupme id
		try:
			other_id = Profile.objects.filter(user=User.objects.get(id=userID)).first().chat_id
		except User.DoesNotExist:
			other_id = None
		if other_id == request.user.profile.chat_id or other_id is None:
			# Check for valid / different id
			return redirect("chat")
		dm = DirectMessages(client.session, other_id)
		messages = []
		userName = client.user.get_me()['name']
		for message in dm.list_all():
			userSent = False
			if message.name == userName:
				userSent = True
			#messages.append(message.name + ": " + message.text)
			messages.append(Message(message.name, userSent, message.text))
		messages = messages[::-1][-15:]
		return render(request, template_name, {"chat": messages, "other_id": userID})

@login_required
def chat_callback(request):
	token = request.GET.get('access_token', None)
	if token is not None:
		request.user.profile.chat_token = token
		request.user.profile.chat_id = Client.from_token(token).user.get_me()['id']
		request.user.profile.save()
	return redirect("chat")

@login_required
def chat_send(request, userID=None):
	msg = request.POST['msg']
	if request.user.profile.chat_token is None:
		# User needs to enable groupme
		return redirect("chat")
	if msg == '':
		return redirect("chat")

	# Create groupme client
	client = Client.from_token(request.user.profile.chat_token)
	# Join the roommate group (required to send dm's)
	groupid = os.environ.get('GROUP_ID', "67775296")
	groupkey = os.environ.get('GROUP_KEY', "eGoKivft")
	client.groups.join(groupid, groupkey)

	if userID is None:
		# If no user specified use the roommate groupchat
		group = client.groups.get(groupid)
		group.post(text=msg)
		return redirect("chat")
	else:
		# Get the other users Groupme id
		try:
			other_id = Profile.objects.filter(user=User.objects.get(id=userID)).first().chat_id
		except User.DoesNotExist:
			other_id = None
		if other_id == request.user.profile.chat_id or other_id is None:
			# Check for valid / different id
			return redirect("chat")
		dm = DirectMessages(client.session, other_id)
		dm.create(text=msg)
		return redirect("chat", userID=userID)
