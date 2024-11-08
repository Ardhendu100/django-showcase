from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.hashers import make_password,check_password
from .forms import SignUpForm, ContactForm
from .models import ContactResponse
from django.core.mail import send_mail
from .backends import EmailBackend 
from django.conf import settings
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.utils import timezone
from datetime import timedelta
from .helpers import get_all_stock_urls, get_stock_price, fetch_stock_data
from .models import Stocks


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'main/home.html')
    else:
        return render(request, 'main/auth/login.html')


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
    if request.user.is_authenticated:
        return redirect('/')
        
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
    if request.user.is_authenticated:
        return redirect('/')
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
def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


def contactus(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactResponse.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            # Email content for admin
            admin_subject = "New Contact Us Query Received"
            admin_message = f"""
            You have received a new query from {form.cleaned_data['name']}.
            Here are the details:

            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Subject: {form.cleaned_data['subject']}
            Message: {form.cleaned_data['message']}
            """
            
            # Send email to admin
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                ['admin@example.com'],  # Replace with the actual admin email
                fail_silently=False,
            )
            
            
            # Email content for user
            user_subject = "Thank you for contacting us"
            user_message = f"""
            Dear {form.cleaned_data['name']},

            Thank you for reaching out! We have received your message and will get back to you shortly.

            Your message:
            {form.cleaned_data['message']}

            Best regards,
            Ardhendu
            """
            # Send confirmation email to the user
            send_mail(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']],
                fail_silently=False,
            )

            
            messages.success(request, 'Your message has been successfully sent.')
            
            return redirect('/contact-us')
        else:
            print("outside")
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
    else:
        form = SignUpForm()
        
    return render(request, 'main/contact.html', {'form': form})


@csrf_exempt  # Disable CSRF protection for simplicity (optional)
def chatbot(request):
    if request.method == 'POST':
        # Get user input from POST request
        data = json.loads(request.body)
        user_input = data.get('message', '')
       
        if user_input:
            # Send request to OpenAI API
            try:
                response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the GPT-3.5 Turbo model
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50 
                )
                answer = response.choices[0].message.content.strip()
                return JsonResponse({'message': answer})
            except Exception as e:
                print(f"Error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def users(request):
    user_list = User.objects.all()  # Fetch all users from the database
    return render(request, 'main/users/index.html', {'users': user_list})


# Send OTP
def generate_otp():
    return random.randint(100000, 999999)


@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            email = data.get("email")
            if email:
                if User.objects.filter(email=email).exists():
                    return JsonResponse({"error": "Email already registered"}, status=400)
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['otp_verified'] = False
                request.session['otp_created_at'] = timezone.now().isoformat()
                # Send email with the OTP
                send_mail(
                    'One Time Password (OTP) for Verification',
                    f"We are pleased to inform you that your One-Time Password (OTP) is: {otp}.\n\n"
                    "It is valid for 3 minutes only.\n\n"
                    "Please use this OTP to complete your verification process. For security reasons, do not share this OTP with anyone.",
                    'ShowCase',
                    [email],
                )

                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Email not provided"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            user_otp = data.get("otp")
            session_otp = request.session.get("otp")
            otp_created_at = request.session.get("otp_created_at")

            # Check if OTP is expired
            if otp_created_at:
                otp_creation_time = timezone.datetime.fromisoformat(otp_created_at)
                current_time = timezone.now()
                if current_time - otp_creation_time > timedelta(minutes=3):
                    return JsonResponse({"success": False, "error": "OTP has expired"})
            

            if user_otp and str(user_otp) == str(session_otp):
                request.session['otp_verified'] = True
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Please enter valid OTP"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def stocks(request):
    stock_list = Stocks.objects.all()
    return render(request, 'main/stocks/index.html', {'stocks': stock_list})


def get_stock(request):
    get_all_stock_urls()
    return JsonResponse({'status' : 200})


def get_meta_stock(request):
    get_stock_price()
    return JsonResponse({'status' : 200})


def fetch_stock_price(request, id):
    stock = Stocks.objects.get(id=id)
    if stock:
        fetch_stock_data(stock)
        return JsonResponse({
        'status': 200,
        'high_price': stock.high_price,
        'low_price': stock.low_price,
        'returns': stock.returns,
        'last_fetched_on': stock.last_fetched_on.strftime('%Y-%m-%d %H:%M:%S'),
    })
    
    