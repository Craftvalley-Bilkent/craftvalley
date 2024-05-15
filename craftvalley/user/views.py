from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.db import connection
import base64
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)


# Add product
def add_product(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        amount = request.POST['amount']
        image = request.FILES['image'] if 'image' in request.FILES else None
        
        # Execute SQL queries to insert product into Product table
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Product (title, description, price, amount, images) "
                "VALUES (%s, %s, %s, %s, %s)",
                [title, description, price, amount, image.read() if image else None]
            )
            # Retrieve the last inserted product_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            product_id = cursor.fetchone()[0]
            
            # Insert product_id and Small Business ID into Add_Product table
            small_business_id = get_small_business_id_for_user(request.user)
            cursor.execute(
                "INSERT INTO Add_Product (product_id, small_business_id, post_date) "
                "VALUES (%s, %s, CURDATE())",
                [product_id, small_business_id]
            )
            
            # Insert initial amount into Add_Amount table
            cursor.execute(
                "INSERT INTO Add_Amount (product_id, small_business_id, amount) "
                "VALUES (%s, %s, %s)",
                [product_id, small_business_id, amount]
            )
        
        return redirect('product_list')
    else:
        return render(request, 'user/add_product.html')
#TEST
def delete_all_products():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Product")

def delete_users():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM User")
        cursor.execute("INSERT INTO User (user_id, user_name, email, password, user_type, address, phone_number, active) VALUES (1, 'CustomerName', 'customer@example.com', 'customer_password', 'customer', '123 Customer St, City', '1234567890', 1)")
        cursor.execute("INSERT INTO Customer (user_id, picture, payment_info, balance) VALUES (1, NULL, 'Credit Card: XXXX-XXXX-XXXX-XXXX', 0.00)")

@csrf_exempt
def showProducts(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'postRating':
            productId = request.POST.get('product_id')
            ratingValue = request.POST.get('rating')
            userId = 1
            delete_users()
            with connection.cursor() as cursor:
                product_data = [(userId, productId, ratingValue)]
                sql_query = "INSERT INTO Rate(customer_id, product_id, star) VALUES (%s, %s, %s)"
                for data in product_data:
                    cursor.execute(sql_query, data)

        elif action == 'addToCart':
            productId = request.POST.get('productId')
            userId = 1
            delete_users()
            with connection.cursor() as cursor:
                cursor.callproc('CartAdder', (userId, productId))
                
            connection.commit()

    image_path_1 = 'first_product_image.jpg'
    image_path_2 = 'second_product_image.jpg'

    with open(image_path_1, 'rb') as image_file_1:
        image_data_1 = image_file_1.read()

    with open(image_path_2, 'rb') as image_file_2:
        image_data_2 = image_file_2.read()

    delete_all_products()
    product_data = [
        (1, 'Second Product', 'Bad product >:(', 250, 74, 4, 2, image_data_1),
        (2, 'First Product', 'Very good product', 12.5, 78, 0.5, 1, image_data_2),
        (5, 'Second Product', 'Bad product >:(', 250, 74, 1, 0, image_data_1),
        (8, 'First Product', 'Very good product', 12.5, 78, 4.5, 62, image_data_2),
        (10, 'Second Product', 'Bad product >:(', 250, 74, 4.8, 782, image_data_1),
        (11, 'First Product', 'Very good product', 12.5, 78, 4.5, 32, image_data_2),
        (6, 'Second Product', 'Bad product >:(', 250, 74, 4.7, 32, image_data_1),
        (7, 'First Product', 'Very good product', 12.5, 78, 4.5, 14, image_data_2),
        (12, 'Second Product', 'Bad product >:(', 250, 74, 4.5, 13, image_data_1),
        (19, 'First Product', 'Very good product', 12.5, 78, 4.5, 152, image_data_2),
        (20, 'Second Product', 'Bad product >:(', 250, 74, 4.5, 152, image_data_1),
        (87, 'First Product', 'Very good product', 12.5, 78, 4.5, 155, image_data_2),
        (24, 'Second Product', 'Bad product >:(', 250, 74, 4.5, 1, image_data_1),
        (59, 'First Product', 'Very good product', 12.5, 78, 4, 12, image_data_2),
        (67, 'Second Product', 'Bad product >:(', 250, 74, 5, 15, image_data_1),
        (53, 'First Product', 'Very good product', 12.5, 78, 1, 17, image_data_2),
        (644, 'Second Product', 'Bad product >:(', 250, 74, 4, 12, image_data_1),
        (57, 'First Product', 'Very good product', 12.5, 78, 4, 112, image_data_2),
        (6111, 'Second Product', 'Bad product >:(', 250, 74, 0, 100, image_data_1),
        (5000, 'First Product', 'Very good product', 12.5, 78, 0, 102, image_data_2)
    ]
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO Product(product_id, title, description, price, amount, rating, number_of_rating, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        for data in product_data:
            cursor.execute(sql_query, data)
    #TEST

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS numOfProducts FROM Product WHERE amount > 0")
        row = cursor.fetchone()
    
    total_products = row[0]

    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)
    end_index = min(start_index + per_page, total_products)

    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM Product WHERE amount > 0 ORDER BY product_id DESC LIMIT %s OFFSET %s"
        cursor.execute(sql_query, (per_page, start_index))
        rows = cursor.fetchall()
    
    all_products = []
    for row in rows:
        product = {
            'product_id': row[0],
            'title': row[1],
            'description': row[2],
            'price': row[3],
            'amount': row[4],
            'rating': row[5],
            'number_of_rating': row[6],
            'images': base64.b64encode(row[7]).decode() if row[7] else None,
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    all_categories = [
        {'category_name': 'category1'},
        {'category_name': 'category2'},
        {'category_name': 'category3'},
        {'category_name': 'category4'},
        {'category_name': 'category5'},
        {'category_name': 'category6'},
        {'category_name': 'category7'},
        {'category_name': 'category8'}
    ]

    return render(request, 'user/mainPageUser.html', {'products': all_products, 'categories': all_categories, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})

def showCart(request):
    return render(request, "user/shoppingCart.html")