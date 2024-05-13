from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from .models import SmallBusiness, Product


# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)

def small_business_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Small_Business WHERE user_id = %s", [user_id])
        business = cursor.fetchone()
    return render(request, 'user/profile.html', {'business': business})

def add_product(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        images = request.FILES['images'].read()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Product (title, description, price, amount, images) VALUES (%s, %s, %s, %s, %s)",
                [title, description, price, amount, images]
            )
            product_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO Add_Product (product_id, small_business_id, post_date) VALUES (%s, %s, NOW())",
                [product_id, user_id]
            )
        return redirect('list_products', user_id=user_id)
    user_id = request.GET.get('user_id')
    return render(request, 'user/add_product.html', {'user_id': user_id})

def list_products(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Product WHERE product_id IN (SELECT product_id FROM Add_Product WHERE small_business_id = %s)",
            [user_id]
        )
        products = cursor.fetchall()
    return render(request, 'user/list_products.html', {'products': products, 'user_id': user_id})

def edit_product(request, product_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        images = request.FILES['images'].read()

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Product SET title = %s, description = %s, price = %s, amount = %s, images = %s WHERE product_id = %s",
                [title, description, price, amount, images, product_id]
            )
        return redirect('list_products', user_id=request.POST['user_id'])
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Product WHERE product_id = %s", [product_id])
            product = cursor.fetchone()
        return render(request, 'user/edit_product.html', {'product': product})

def delete_product(request, product_id):
    user_id = request.POST['user_id']
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM Product WHERE product_id = %s AND product_id IN (SELECT product_id FROM Add_Product WHERE small_business_id = %s)",
            [product_id, user_id]
        )
    return redirect('list_products', user_id=user_id)

def balance_history(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT br.record_date, br.record_type, br.record_amount
            FROM Balance_Record br
            JOIN Business_Has_Record bhr ON br.record_id = bhr.record_id
            WHERE bhr.small_business_id = %s
            """,
            [user_id]
        )
        balance_records = cursor.fetchall()
    return render(request, 'user/balance_history.html', {'balance_records': balance_records})