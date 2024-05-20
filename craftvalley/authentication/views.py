from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import hashlib
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_phone_number(phone_number):
    return re.match(r'^\+?\d+$', phone_number)

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register_user')
        
        if not is_valid_phone_number(phone_number):
            messages.error(request, "Phone number must consist only of numbers with an optional + at the start.")
            return redirect('register_user')

        hashed_password = hash_password(password)
        
        with connection.cursor() as cursor:
            # Check if username exists
            cursor.execute("SELECT * FROM User WHERE user_name = %s", [username])
            if cursor.fetchone():
                messages.error(request, "Username already exists.")
                return redirect('register_user')
            
            # Check if email exists
            cursor.execute("SELECT * FROM User WHERE email = %s", [email])
            if cursor.fetchone():
                messages.error(request, "Email already exists.")
                return redirect('register_user')
            
            # Check if phone number exists
            cursor.execute("SELECT * FROM User WHERE phone_number = %s", [phone_number])
            if cursor.fetchone():
                messages.error(request, "Phone number already exists.")
                return redirect('register_user')

            # Insert new user
            cursor.execute(
                "INSERT INTO User (user_name, email, password, user_type, phone_number, active) VALUES (%s, %s, %s, %s, %s, %s)",
                [username, email, hashed_password, 'Customer', phone_number, 1]
            )
            user_id = cursor.lastrowid

            # Insert into Customer table with default values
            cursor.execute(
                "INSERT INTO Customer (user_id, payment_info, balance) VALUES (%s, %s, %s)",
                [user_id, '', 0.00]
            )

            messages.success(request, "Registration successful.")
            return redirect('login')
    return render(request, 'authentication/register_user.html')

def register_business(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        business_name = request.POST['business_name']
        title = request.POST['title']
        description = request.POST['description']

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register_business')
        
        if not is_valid_phone_number(phone_number):
            messages.error(request, "Phone number must consist only of numbers with an optional + at the start.")
            return redirect('register_user')

        hashed_password = hash_password(password)
        
        with connection.cursor() as cursor:
            # Check if username exists
            cursor.execute("SELECT * FROM User WHERE user_name = %s", [username])
            if cursor.fetchone():
                messages.error(request, "Username already exists.")
                return redirect('register_business')
            
            # Check if email exists
            cursor.execute("SELECT * FROM User WHERE email = %s", [email])
            if cursor.fetchone():
                messages.error(request, "Email already exists.")
                return redirect('register_business')
            
            # Check if phone number exists
            cursor.execute("SELECT * FROM User WHERE phone_number = %s", [phone_number])
            if cursor.fetchone():
                messages.error(request, "Phone number already exists.")
                return redirect('register_business')

            # Insert new user
            cursor.execute(
                "INSERT INTO User (user_name, email, password, user_type, phone_number, active) VALUES (%s, %s, %s, %s, %s, %s)",
                [username, email, hashed_password, 'Small_Business', phone_number, 1]
            )
            user_id = cursor.lastrowid

            # Insert new business
            cursor.execute(
                "INSERT INTO Small_Business (user_id, business_name, title, description, balance) VALUES (%s, %s, %s, %s, %s)",
                [user_id, business_name, title, description, 0.00]
            )

            messages.success(request, "Registration successful.")
            return redirect('login')
    return render(request, 'authentication/register_business.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = hash_password(request.POST['password'])
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE email = %s AND password = %s", [username, password])
            user = cursor.fetchone()     
            if user:
                user_id = user[0]
                user_type = user[4]
                
                if user_type == 'Small_Business':
                    cursor.execute("SELECT * FROM Ban WHERE small_business_id = %s", [user_id])
                    ban = cursor.fetchone()
                    if ban:
                        messages.error(request, "Your account has been banned.")
                        return redirect('banned')

                request.session['user_id'] = user[0]
                request.session['user_name'] = user[1]
                request.session['user_type'] = user_type

                if user_type == 'Customer':
                    messages.success(request, "Login successful.")
                    return redirect('user_main')
                elif user_type == 'Small_Business':
                    return redirect('small_business_profile')
                elif user_type == 'Admin':
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
    return render(request, 'authentication/login.html')

def banned(request):
    return render(request,'authentication/banned.html')

def small_business_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    with connection.cursor() as cursor:
        # Fetch business details
        cursor.execute("SELECT business_name, title, description FROM Small_Business WHERE user_id = %s", [user_id])
        business = cursor.fetchone()
        
        # Calculate total balance from transactions
        cursor.execute("""
            SELECT SUM(P.price * T.count) AS total_balance
            FROM Transaction T
            JOIN Product P ON T.product_id = P.product_id
            WHERE T.small_business_id = %s AND T.transaction_status = 'completed'
        """, [user_id])
        total_balance = cursor.fetchone()[0] or 0
    
    return render(request, 'authentication/small_business_profile.html', {'business': business, 'total_balance': total_balance})

def edit_business_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        business_name = request.POST['business_name']
        title = request.POST['title']
        description = request.POST['description']

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Small_Business SET business_name = %s, title = %s, description = %s WHERE user_id = %s",
                [business_name, title, description, user_id]
            )
        messages.success(request, "Profile updated successfully.")
        return redirect('small_business_profile')

    with connection.cursor() as cursor:
        cursor.execute("SELECT business_name, title, description FROM Small_Business WHERE user_id = %s", [user_id])
        business = cursor.fetchone()
    
    return render(request, 'authentication/edit_business_profile.html', {'business': business})

def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, email, phone_number FROM User WHERE user_id = %s", [user_id])
        user = cursor.fetchone()
    
    return render(request, 'authentication/user_profile.html', {'user': user})

def edit_user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        if not is_valid_phone_number(phone_number):
            messages.error(request, "Phone number must consist only of numbers with an optional + at the start.")
            return redirect('edit_user_profile')

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE User SET user_name = %s, email = %s, phone_number = %s WHERE user_id = %s",
                [username, email, phone_number, user_id]
            )
        messages.success(request, "Profile updated successfully.")
        return redirect('user_profile')

    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, email, phone_number FROM User WHERE user_id = %s", [user_id])
        user = cursor.fetchone()
    
    return render(request, 'authentication/edit_user_profile.html', {'user': user})

def logout_view(request):
    # Clear session data
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return redirect('login')