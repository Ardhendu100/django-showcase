from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.hashers import make_password,check_password
from .forms import SignUpForm
from .backends import EmailBackend 


def homepage(request):
    return render(request, 'main/home.html')

def generate_username(self, first_name):
        # Create a base username
        base_username = f"{first_name.lower().strip()}"
        
        random_digit = random.randint(1000, 9999)
        
        # Combine base username with random digit
        username = f"{base_username}{random_digit}"
        
        # Ensure uniqueness of username
        while User.objects.filter(username=username).exists():
            random_digit = random.randint(0, 9)  # Generate a new random digit
            username = f"{base_username}{random_digit}"
        
        return username


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Authenticate user using the custom backend
        user = EmailBackend().authenticate(request, email=email, password=password)    

        if user is not None:
            login(request, user)
            print('login')
            return redirect('/')
    
        else:
            print('invalid')
            messages.error(request, "Invalid username or password")
            return render(request, 'main/auth/login.html')
    return render(request, 'main/auth/login.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['first_name'])
            username = form.generate_username(form.cleaned_data['first_name'])
            print('username', username)
            
            user = User.objects.create_user(
                username=username,  # Generated username
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            login(request, user)  # Log the user in after successful signup
            messages.success(request, "Signup successful!")
            return redirect('/')
        else:
            print("outside")
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
            
    else:
    
        form = SignUpForm()
    
    return render(request, 'main/auth/signup.html', {'form': form})


# Log out user
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('homepage')