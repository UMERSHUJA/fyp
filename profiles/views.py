from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
        

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check passwords are same 
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('/')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('/')
                else:
                    # Look good
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    user.set_password(password)
                    user.save()
                    messages.success(request, f'{username}! You are now registered and can log in')
                    return redirect('/')
        else:
            messages.error(request, 'Password do not match')
            return redirect('/')
    else:
        return render(request, 'listings/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f'{username}! You are now logged in')
            return redirect('/')

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        return render(request, 'listings/index.html')



def dashboard(request):
    pass


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('/')
