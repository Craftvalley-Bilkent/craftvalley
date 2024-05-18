from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile

#@login_required
def create_product(request):
    if request.method == 'POST':
        title = request.POST['title']
        recipient = request.POST['recipient']
        materials = request.POST['materials']
        category = request.POST['category']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Product (title, description, price, amount)
                    VALUES (%s, %s, %s, %s)
                """, [title, description, price, amount])

                product_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO Add_Product (product_id, small_business_id, post_date)
                    VALUES (%s, %s, NOW())
                """, [product_id,  request.session.get("user_id")])

                messages.success(request, 'Product created successfully!')
                return redirect('list_products')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            print(f'Error: {e}') 

    return render(request, 'small_business/create_product.html')

#@login_required
def list_products(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Product
            WHERE product_id IN (SELECT product_id FROM Add_Product WHERE small_business_id = %s)
        """, [ request.session.get("user_id")])
        products = cursor.fetchall()

    return render(request, 'small_business/list_products.html', {'products': products})

#@login_required
def edit_product(request, product_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Product
                    SET title = %s, description = %s, price = %s, amount = %s
                    WHERE product_id = %s
                """, [title, description, price, amount, product_id])

                messages.success(request, 'Product updated successfully!')
                return redirect('list_products')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Product WHERE product_id = %s
        """, [product_id])
        product = cursor.fetchone()

    return render(request, 'small_business/edit_product.html', {'product': product})

#@login_required
def delete_product(request, product_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Product WHERE product_id = %s
            """, [product_id])

            messages.success(request, 'Product deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error: {e}')

    return redirect('list_products')

#@login_required
def view_balance_history(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Balance_Record
            WHERE record_id IN (SELECT record_id FROM Business_Has_Record WHERE small_business_id = %s)
        """, [request.user.id])
        balance_history = cursor.fetchall()

    return render(request, 'small_business/balance_history.html', {'balance_history': balance_history})