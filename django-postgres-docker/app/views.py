from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Add a simple index view
def index(request):
    return HttpResponse("Welcome to the index page.")

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('index')
        # No need for else: pass, form with errors will be rendered below
    else:
        form = UserCreationForm()
    return render(request, 'app/registro.html', {'form': form})


@csrf_exempt
@require_POST
def register_api(request):
    """
    API endpoint for user registration.
    Expects POST request with JSON body:
    {
        "username": "...",
        "email": "...", # Optional
        "password": "...", # Changed to password1 in curl, adjust view
        "password2": "..."
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        # Read 'password' from JSON (as sent by curl in the last attempt)
        password = data.get('password') # Read the first password field from JSON
        password2 = data.get('password2') # Read the second password field from JSON

        # Check if required fields are present
        if not username or not password or not password2:
             return JsonResponse({'status': 'error', 'message': 'Missing username or password fields.'}, status=400)

        # Check if passwords match BEFORE passing to form
        if password != password2:
            # Return the specific error if they don't match here
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

        # Prepare data for UserCreationForm - it expects 'password1' and 'password2'
        form_data = {
            'username': username,
            'password1': password,  # Use the value read from JSON key 'password' for form field 'password1'
            'password2': password2  # Use the value read from JSON key 'password2' for form field 'password2'
        }
        # If your form requires email, add it:
        # email = data.get('email')
        # if email:
        #     form_data['email'] = email

        form = UserCreationForm(form_data)

        if form.is_valid():
            user = form.save()
            return JsonResponse({'status': 'success', 'message': 'User registered successfully.', 'user_id': user.id}, status=201)
        else:
            # Collect form errors (these might include password complexity rules etc.)
            errors = form.errors.get_json_data()
            # Customize error message if needed, or just return Django's errors
            return JsonResponse({'status': 'error', 'message': 'Registration failed due to validation errors.', 'errors': errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Error during API registration: {e}") # Log the error server-side
        return JsonResponse({'status': 'error', 'message': 'An unexpected server error occurred.'}, status=500)
