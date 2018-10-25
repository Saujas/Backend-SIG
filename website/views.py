from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from .models import Client
from django import forms
from .forms import UserForm
from django.contrib.auth.models import User


def signup(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		print("Yes1")
		if form.is_valid():
			print("Yes")
			username = form.cleaned_data['username']
			raw_password = form.cleaned_data['password']
			if not (User.objects.filter(username=username).exists()):
				User.objects.create_user(username, None, raw_password)
				#user = authenticate(username = username, password = raw_password)
				#login(request, user)
			return redirect('/login/')
		else:
			form = UserCreationForm()
	return render(request, 'website/signup.html')



def login(request):
	data = True
	if request.POST:
		lform = LoginForm(request.POST)
		if lform.is_valid():
			data=lform.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('/test/')
			else:
				return render(request, 'website/index.html', {'data': data})	
	return render(request, 'website/index.html')



def test(request):
	if request.user.is_authenticated:
		if request.POST:
			if not Client.objects.filter(user=request.user).exists():
				obj = Client(user=request.user)
				obj.save()
				client = obj
			else:
				client=Client.objects.get(user=request.user)
			if 'post' in request.POST:
				client.data = request.POST['data']
				client.save()
			elif 'put' in request.POST:
				if request.POST['data']:
					client.data += request.POST['data']
					client.save()
			elif 'delete' in request.POST:
				client.data = 'Nothing posted'
				client.save()
			elif 'get' in request.POST:
				yes = True
				return render(request, 'website/test.html', {'yes':yes, 'client':client})



		return render(request, 'website/test.html')
	else:
		return redirect('/')


def logout(request):
	django_logout(request)
	return redirect('/')