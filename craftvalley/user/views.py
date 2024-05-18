from django.shortcuts import render
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
            amount = request.POST.get('amount')
            userId = 1
            delete_users()
            with connection.cursor() as cursor:
                cursor.callproc('CartAdder', (userId, productId, amount))
                
            connection.commit()
        elif action == 'addToWishlist':
            productId = request.POST.get('productId')
            isActive = request.POST.get('isActive')
            userId = 1
            delete_users()
            with connection.cursor() as cursor:
                if(isActive == True):
                    cursor.execute("DELETE FROM Wish Where product_id = " + str(productId) + " AND customer_id = " + str(userId))
                else:
                    cursor.execute("INSERT INTO Wish(customer_id, product_id) VALUES(" + str(userId) + ", " + str(productId) + ")")
            
    image_path_1 = 'first_product_image.jpg'
    image_path_2 = 'second_product_image.jpg'

    with open(image_path_1, 'rb') as image_file_1:
        image_data_1 = image_file_1.read()

    with open(image_path_2, 'rb') as image_file_2:
        image_data_2 = image_file_2.read()

    delete_all_products()
    product_data = [
        (1, 'Second Product', 'Bad product >:(', 250, 0, image_data_1),
        (2, 'First Product', 'Very good product', 12.5, 0, image_data_2),
        (5, 'Second Product', 'Bad product >:(', 250, 0, image_data_1),
        (8, 'First Product', 'Very good product', 12.5, 0, image_data_2),
        (10, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (11, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (6, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (7, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (12, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (19, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (20, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (87, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (24, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (59, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (67, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (53, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (644, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (57, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (6111, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (5000, 'First Product', 'Very good product', 12.5, 78, image_data_2)
    ]
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO Product(product_id, title, description, price, amount, images) VALUES (%s, %s, %s, %s, %s, %s)"

        for data in product_data:
            cursor.execute(sql_query, data)
    #TEST
    temp_query = "SELECT COUNT(*) AS numOfProducts FROM Product"
    action = ""
    business_name = ""
    min_price = ""
    max_price = ""

    if request.method == 'GET':
        action = request.GET.get('action')
        
        if action == 'isFiltered':
            business_name = request.GET.get('business_name')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')

            temp_query = """SELECT COUNT(*) AS numOfProducts FROM Product
            JOIN Add_Product ON Product.product_id = Add_Product.product_id
            JOIN Small_Business ON Add_Product.small_business_id = Small_Business.user_id
            WHERE 1 = 1
            """

            if(business_name != ""):
                temp_query = temp_query + " AND Small_Business.business_name LIKE " + business_name + "AND 2 = 2"
            if(min_price != ""):                  
                temp_query = temp_query + " AND Product.price >= " + min_price + " AND 3 = 3"
            if(max_price != ""):                  
                temp_query = temp_query + " AND Product.price <= " + max_price

    with connection.cursor() as cursor:
        cursor.execute(temp_query)
        row = cursor.fetchone()
    
    total_products = row[0]

    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        if (action == 'isFiltered'):
            cursor.callproc("ProductFilter", (per_page, start_index, business_name,  float(min_price or 0), float(max_price or 99999999.99)))
        else:
            cursor.callproc("ProductPrinter", (per_page, start_index))
        
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
            'isWished': 0,
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


    with connection.cursor() as cursor:
        cursor.execute("SELECT product_id FROM Wish WHERE customer_id = 1")
        rows = cursor.fetchall()

    all_wished_products = []
    for row in rows:
        wished_product = {
            'product_id': row[0],
        }
        all_wished_products.append(wished_product)
    i = 0
    j = 0
    while (j < len(all_wished_products)) and i < 16:
        if(all_wished_products[j][0] == all_products[i][0]):
            all_products[i][8] = 1
            i += 1
            j += 1
        else:
            i += 1
    
    return render(request, 'user/mainPageUser.html', {'products': all_products, 'categories': all_categories, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})

def showCart(request):
    return render(request, "user/shoppingCart.html")