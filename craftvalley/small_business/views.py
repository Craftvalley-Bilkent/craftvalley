from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

#@login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db import connection
from decimal import Decimal, InvalidOperation

#@login_required
def create_product(request):
    recipients, materials, categories = [], [], []

    if request.method == 'POST':
        title = request.POST['title']
        recipient_id = request.POST['recipient']
        material_id = request.POST['materials']
        category_id = request.POST['category']
        subcategory_id = request.POST['subcategory']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        
       
        try:
            price = Decimal(price)
        except InvalidOperation:
            messages.error(request, 'Price must be a valid decimal number.')
            return redirect('create_product')
        
        if not amount.isdigit():
            messages.error(request, 'Amount must be a valid integer.')
            return redirect('create_product')
        
        amount = int(amount)

        try:
            image = request.FILES['image']
            image_data = image.read()

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Product (title, description, price, amount, images)
                    VALUES (%s, %s, %s, %s, %s)
                """, [title, description, price, amount, image_data])

                product_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO Add_Product (product_id, small_business_id, post_date)
                    VALUES (%s, %s, NOW())
                """, [product_id, request.session.get("user_id")])

                cursor.execute("""
                    INSERT INTO Is_For (product_id, recipient_id)
                    VALUES (%s, %s)
                """, [product_id, recipient_id])

                cursor.execute("""
                    INSERT INTO Made_By (product_id, material_id)
                    VALUES (%s, %s)
                """, [product_id, material_id])

                cursor.execute("""
                    INSERT INTO In_Category (sub_category_id, main_category_id, product_id)
                    VALUES (%s, %s, %s)
                """, [subcategory_id, category_id, product_id])

                messages.success(request, 'Product created successfully!')
                return redirect('list_products')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            print(f'Error: {e}') 

    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT recipient_id, recipient_name FROM Recipient")
            recipients = cursor.fetchall()
            
            cursor.execute("SELECT material_id, material_name FROM Material")
            materials = cursor.fetchall()
            
            cursor.execute("SELECT main_category_id, main_category_name FROM Main_Category")
            categories = cursor.fetchall()

    return render(request, 'small_business/create_product.html', {
        'recipients': recipients,
        'materials': materials,
        'categories': categories
    })

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT sub_category_id, sub_category_name FROM Sub_Category WHERE main_category_id = %s", [category_id])
        subcategories = cursor.fetchall()
    return JsonResponse({'subcategories': [{'sub_category_id': sub[0], 'sub_category_name': sub[1]} for sub in subcategories]})

#@login_required
def list_products(request):
    user_name = request.session.get("user_name")

    with connection.cursor() as cursor:
        cursor.callproc("BusinessProducts", (user_name, ))
        rows = cursor.fetchall()

    products = []
    for row in rows:
        new_row = row[:7] + (base64.b64encode(row[7]).decode() if row[7] else None, ) + row[8:]
        products.append(new_row)

    return render(request, 'small_business/list_products.html', {'products': products})


#@login_required
def edit_product(request, product_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        images = request.FILES.get('images')

        try:
            with connection.cursor() as cursor:
                if images:
                    images_data = images.read()
                    cursor.execute("""
                        UPDATE Product
                        SET title = %s, description = %s, price = %s, amount = %s, images = %s
                        WHERE product_id = %s
                    """, [title, description, price, amount, images_data, product_id])
                else:
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
def update_product_amount(request, product_id):
    if request.method == 'POST':
        amount = request.POST['amount']

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Product
                    SET amount = %s
                    WHERE product_id = %s
                """, [amount, product_id])

                messages.success(request, 'Product amount updated successfully!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        
        return redirect('list_products')

def show_balance_records(request):
    user_id = request.session.get("user_id")
    user_type = request.session.get('user_type')
    
    # Ensure the user is a small business
    if user_type != 'Small_Business':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Balance_Record BR
            JOIN Business_Has_Record BHR ON BR.record_id = BHR.record_id
            WHERE BHR.small_business_id = %s
        """, [user_id])
        row = cursor.fetchone()
    
    total_records = row[0]

    per_page = 10
    total_pages = (total_records + per_page - 1) // per_page
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT BR.record_date, BR.record_type, BR.record_amount
            FROM Balance_Record BR
            JOIN Business_Has_Record BHR ON BR.record_id = BHR.record_id
            WHERE BHR.small_business_id = %s
            ORDER BY BR.record_id DESC
            LIMIT %s OFFSET %s
        """, [user_id, per_page, start_index])
        rows = cursor.fetchall()

    balance_records = []
    for row in rows:
        record = {
            'record_date': row[0].strftime('%Y-%m-%d'),
            'record_type': row[1],
            'record_amount': row[2],
        }
        balance_records.append(record)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    return render(request, 'small_business/balance_records.html', {
        'balance_records': balance_records, 
        'current_page': current_page, 
        'total_pages': total_pages, 
        'page_range': page_range
    })
