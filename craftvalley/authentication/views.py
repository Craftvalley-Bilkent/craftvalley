from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register')
        
        hashed_password = hash_password(password)
        
        with connection.cursor() as cursor:
            # Check if username exists
            cursor.execute("SELECT * FROM User WHERE user_name = %s", [username])
            if cursor.fetchone():
                messages.error(request, "Username already exists.")
                return redirect('register')
            
            # Check if email exists
            cursor.execute("SELECT * FROM User WHERE email = %s", [email])
            if cursor.fetchone():
                messages.error(request, "Email already exists.")
                return redirect('register')
            
            # Check if phone number exists
            cursor.execute("SELECT * FROM User WHERE phone_number = %s", [phone_number])
            if cursor.fetchone():
                messages.error(request, "Phone number already exists.")
                return redirect('register')

            # Insert new user
            cursor.execute(
                "INSERT INTO User (user_name, email, password, user_type, phone_number, active) VALUES (%s, %s, %s, %s, %s, %s)",
                [username, email, hashed_password, 'user', phone_number, 1]
            )
            messages.success(request, "Registration successful.")
            return redirect('login')
    return render(request, 'authentication/registration.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = hash_password(request.POST['password'])
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE user_name = %s AND password = %s", [username, password])
            user = cursor.fetchone()
            if user:
                request.session['user_id'] = user[0]
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
    return render(request, 'authentication/login.html')
