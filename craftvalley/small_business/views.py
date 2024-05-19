from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

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
    user_id = request.user.id  
    per_page = 10 
    start_index = 0 
    
    with connection.cursor() as cursor:
        cursor.callproc('ProductPrinter', [per_page, start_index])
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
def view_balance_history(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Balance_Record
            WHERE record_id IN (SELECT record_id FROM Business_Has_Record WHERE small_business_id = %s)
        """, [request.user.id])
        balance_history = cursor.fetchall()

    return render(request, 'small_business/balance_history.html', {'balance_history': balance_history})

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