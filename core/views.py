from django.shortcuts import render, redirect
from django.forms import ModelForm
from .forms import PickupRequestForm
from django.core.mail import send_mail
from .models import PickupRequest
# import openai  # <--- This line should be commented out or removed if you're not using OpenAI
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback

# Add the Google Generative AI import
import google.generativeai as genai # <--- Ensure this import is present

def homepage(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def reqs(request):
    return render(request, 'reqs.html')

def pickup(request):
    if request.method == 'POST':
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                'E-Waste Pickup Confirmation',
                f"Dear {form.cleaned_data['name']},\n\nThank you for your e-waste pickup request. We will reach out soon.",
                'malthumkarvarun@gmail.com',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return render(request, 'reqs.html')
        else:
            return render(request, 'pickup.html', {'form': form})
    else:
        form = PickupRequestForm()
    return render(request, 'pickup.html', {'form': form})

def list_pickup_requests(request):
    requests = PickupRequest.objects.all().order_by('-created_at')
    return render(request, 'list_pickup_requests.html', {'pickup_requests': requests})

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            # Configure the Gemini API with your key
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Initialize the generative model
            # You can choose different models like 'gemini-pro', 'gemini-1.5-pro-latest' etc.
            model = genai.GenerativeModel('gemini-1.5-flash') 

            # Start a chat session (optional, but good for multi-turn conversations)
            chat_session = model.start_chat(history=[])

            # Send the user message and get a response
            response = chat_session.send_message(user_message)
            
            # Extract the chatbot's reply
            # Gemini's response is typically accessed via .text
            chatbot_reply = response.text 
            
            return JsonResponse({'response': chatbot_reply})

        except Exception as e:
            print(f"Error in chatbot_response: {e}")
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)