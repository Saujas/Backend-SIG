from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib import auth
from .forms import LoginForm
from .models import Client


def index(request):
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
			client = Client.objects.get(user=request.user)
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