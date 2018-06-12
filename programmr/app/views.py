from __future__ import division
import requests, filecmp
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from models import *
from forms import *
from google_script import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

getGoogle = GooglePlus(settings.GOOGLE_PLUS_APP_ID, settings.GOOGLE_PLUS_APP_SECRET)


def index(request):
	if request.user.is_active:
		return redirect(reverse_lazy('dashboard'))
	
	return render(request, 'index.html')


def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			return render(request, 'login.html', {'error': 'Sorry, Username or Password is incorrect!!!'})
	return render(request, 'login.html')



def signup_view(request):
	if request.method == 'POST':
		try:
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
			user = User.objects.create_user(username, email, password)
			user.save()
			login(request, user)
			return redirect(reverse_lazy('profile'))
		except:
			return render(request, 'signup.html', {'error': 'Sorry, this username is already taken!!!'})

	return render(request, 'signup.html')



def logout_view(request):

	if request.user.is_active:
		logout(request)
	
	return redirect(reverse_lazy('index'))


def profile(request):

	if not request.user.is_active:
		return redirect(reverse_lazy('index'))

	if request.method == 'POST':
		user = User.objects.get(id=request.user.id)
		user_profile = UserProfile()
		user.first_name = request.POST['fname']
		user.last_name = request.POST['lname']
		user_profile.user = user
		user_profile.year = request.POST['year']
		user_profile.branch = request.POST['branch']
		user_profile.mobile = request.POST['mobile']
		user_profile.college = request.POST['college']
		user.save()
		user_profile.save()

		return redirect(reverse_lazy('dashboard'))

	return render(request, 'profile.html')


def dashboard(request):
	
	if not request.user.is_active:
		return redirect(reverse_lazy('login_page'))
	
	try:
		user_detail = UserProfile.objects.get(user=request.user)
	except:
		return redirect(reverse_lazy('profile'))
	queryset = Question.objects.all()

	context = { 
			"user": user_detail, 
	        "questions": queryset,
	    }
	
	return render(request, "dashboard.html", context)


def question_detail(request,id=None):
	
	if not request.user.is_active:
		return redirect(reverse_lazy('login_page'))

	user_detail = UserProfile.objects.get(user=request.user)
	instance = get_object_or_404(Question,id=id)
	form = UploadFileForm()
	context = { 
		"question": instance,
		"form": form,
		"user": user_detail,
	}
	return render(request, "question_detail.html", context)


def submission(request,id=None):

	#! -*- coding: utf-8 -*-
	#import string

	user_detail = UserProfile.objects.get(user=request.user)
	if not request.user.is_active:
		
		return redirect(reverse_lazy('login_page'))

	elif request.method == 'POST':
		
		user_id = user_detail.user.username

		id = request.POST['id']
		instance = get_object_or_404(Question, id=id)

		# constants
		RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
		CLIENT_SECRET = '**********************'
		
		ques = Question.objects.all().get(id=id)
		lang = ques.lang
		f = ques.testcase_input
		f.open(mode='rb') 
		lines_input = f.read()
		f.close()

		g = Question.objects.all().get(id=id).testcase_output
		g.open(mode='rb') 
		lines_output = g.read()
		g.close()

		if len(request.POST['source']) != 0:
			
			source = request.POST['source']

			data = {
		    	'client_secret': CLIENT_SECRET,
		    	'async': 0,
		    	'source': source,
		    	'lang': lang,
		    	'time_limit': 5,
		    	'memory_limit': 262144,
		    	'input':lines_input,
			}

		elif len(request.FILES) != 0:
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				file = request.FILES['file']
				source = file.read()

				data = {
			    	'client_secret': CLIENT_SECRET,
			    	'async': 0,
			    	'source': source,
			    	'lang': lang,
			    	'time_limit': 5,
			    	'memory_limit': 262144,
			    	'input':lines_input,
				}
		else:
			return redirect(reverse_lazy('question_detail', kwargs={'id':id}))
		r = requests.post(RUN_URL, data=data)
		response = r.json()
		status = response['run_status']['status']
		web_link = response['web_link']
		c_status = None
		if(status == "CE"):
			result = "CE"
			c_status = response['compile_status']
		elif(status == "TLE"):
			result = "TLE"
		elif(status == "RE"):
			result = "RE"
		elif(status == "AC"):
			output = response['run_status']['output']
			same = set(output).intersection(lines_output)
			same.discard('\n')
			if same:
				result = "CA"
				if instance.submission_set.filter(user_ID=user_id, status=result).count() == 0:
					user_detail.total_score += 100
					user_detail.save()
					instance.correct_submissions += 1
					
			else:
				result="WA"

		query = Submission(ques_ID=instance, user_ID=user_id, question_ID=id, status=result,source_code_URL=web_link)
		query.save()

		instance.total_submissions += 1 
		instance.accuracy = (instance.correct_submissions/instance.total_submissions)*100
		instance.save()
		
		context = { "result":result, "user": user_detail, "error": c_status }
		
		return render(request,"submission.html",context)

	else:
		return render(request,"errors/404.html", { "user":user_detail })


def leaderboard(request):
	user_detail = UserProfile.objects.get(user=request.user)
	data = UserProfile.objects.annotate().order_by('-total_score')
	context = {
		'user': user_detail,
		'data': data,
	}
	return render(request,"leaderboard.html", context)


def announcements(request):
	queryset=Announcement.objects.all()
	user_detail = UserProfile.objects.get(user=request.user)
	context={
	    "Announcement": queryset,
	    "user": user_detail,
	}
	return render(request,"announcements.html",context)
	

def rules(request):
	user_detail = UserProfile.objects.get(user=request.user)
	return render(request,"rules.html", {'user': user_detail})
