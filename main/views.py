from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from .forms import CounsellorRegistrationForm
from .models import Client, Counsellor,Booking
def home(request):
    return render(request, 'home.html')

# def login_view(request):
#     user=None
#     error_message=None
#     if request.POST:
#         username=request.POST['username']
#         password=request.POST['password']
#         try:
#             user=User.objects.create_user(username=username, password=password)
#         except Exception as e:
#             error_message = str(e)
#     return render(request, 'login.html',{user:user,'error_message':error_message})

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Redirect based on profile type
            if hasattr(user, 'client'):
                return redirect('client_dashboard')
            elif hasattr(user, 'counsellor'):
                return redirect('counsellor_dashboard')
            else:
                messages.error(request, "No profile linked. Contact admin.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")
    #     if user is not None:
    #         login(request, user)
    #         if Client.objects.filter(username=user).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('client_dashboard')  # your URL name

    #         # 🔍 Check if the logged in user is a Counsellor
    #         elif Counsellor.objects.filter(username=user).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('counsellor_dashboard')  # your URL name

    #         # Optional: if neither, show error
    #         else:
    #             error_message = "User type not recognized."
          
    #     else:
    #         error_message = "Invalid username or password."

    # return render(request, 'login.html', {'error_message': error_message})


    #     if user is not None:
    #         login(request, user)
    #         if Client.objects.filter(username=user.username).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('client_dashboard')
    #         else:
    #             messages.error(request, "User type not recognized.")
    #             return redirect('login')

    #     # 2️⃣ Try Counsellor authentication via custom backend
    #     counsellor = authenticate(
    #         request,
    #         username=username,
    #         password=password,
    #         backend='myapp.backends.CounsellorBackend'
    #     )
    #     if counsellor:
    #         request.session['counsellor_id'] = counsellor.id
    #         messages.success(request, f"Welcome back, {counsellor.username}!")
    #         return redirect('counsellor_dashboard')

    #     # 3️⃣ If both fail
    #     messages.error(request, "Invalid username or password.")

    # return render(request, 'login.html')


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Registration successful! Welcome, client!')
            return redirect('login')  # Replace with your desired redirect
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': user_form})


def register_counselor(request):
    if request.method == 'POST':
        counselor_form = CounsellorRegistrationForm(request.POST)
        if counselor_form.is_valid():
            counselor_form.save()
            messages.success(request, 'Registration successful! Welcome, counsellor!')
            # user.set_password(counselor_form.cleaned_data['password1'])
            # user.save()
            return redirect('login')  # Redirect to login or dashboard
        else:
            print("Form errors:", counselor_form.errors)
    else:
      
        counselor_form = CounsellorRegistrationForm()
    return render(request, 'accounts/registercounsellor.html', {
        'counselor_form': counselor_form
    })


from django.shortcuts import render, redirect
from .forms import BookingForm

from django.contrib.auth.decorators import login_required

@login_required
def book_counsellor(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user  # assuming logged in user is Client
            booking.status = 'Pending'
            booking.save()
            return redirect('successsful')  # or any success page
    else:
        form = BookingForm()
    return render(request, 'book_counsellor.html', {'form': form})



# def recommend_articles(interest):
#     # You can replace this with your actual AI logic later
#     if 'stress' in interest.lower():
#         return ["5 Ways to Manage Stress", "Meditation Techniques for Relaxation"]
#     elif 'career' in interest.lower():
#         return ["Top Career Planning Tips", "How to Set Career Goals"]
#     else:
#         return ["How to Stay Positive Daily", "Benefits of Talking to a Therapist"]

@login_required
def client_dashboard(request):
    client = request.user  # get the logged-in client user
    message = None

    # When form is submitted
    if request.method == 'POST':
        new_interest = request.POST.get('new_interest')  # get new interest
        if new_interest:
            # If client has existing interests
            if client.interest:
                # Add new interest to existing list
                client.interest += f", {new_interest}"
            else:
                client.interest = new_interest  # First interest
            client.save()  # Save updated client
            message = "Interest added successfully!"

    # Split interests into a list
    if client.interest:
        interests = client.interest.split(",")
    else:
        interests = []

    # Generate article titles from interests
    articles = []
    for interest in interests:
        interest = interest.strip()
        if interest:
            articles.append(f"AI article about {interest}")

    # Get all bookings for this client
    bookings = Booking.objects.filter(client=client)

    # Get all counsellors
    counsellors = Counsellor.objects.all()

    return render(request, 'dashboards/client_dashboard.html', {
        'client': client,
        'interests': interests,
        'articles': articles,
        'bookings': bookings,
        'counsellors': counsellors,
        'message': message
    })


@login_required
def counsellor_dashbord(request):
    return render(request, 'dashboards/counsellor_dashboard.html')
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')  # Redirect to a logout confirmation page or home page