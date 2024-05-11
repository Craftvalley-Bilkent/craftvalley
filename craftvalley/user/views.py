from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import base64

# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)

#TEST
def delete_all_products():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Product")
#TEST
def showProducts(request):
    #TEST
    image_path_1 = 'first_product_image.jpg'
    image_path_2 = 'second_product_image.jpg'

    with open(image_path_1, 'rb') as image_file_1:
        image_data_1 = image_file_1.read()

    with open(image_path_2, 'rb') as image_file_2:
        image_data_2 = image_file_2.read()

    delete_all_products()
    product_data = [
        (1, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (2, 'First Product', 'Very good product', 12.5, 78, image_data_2),
        (5, 'Second Product', 'Bad product >:(', 250, 74, image_data_1),
        (8, 'First Product', 'Very good product', 12.5, 78, image_data_2),
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
            'images': base64.b64encode(row[5]).decode() if row[5] else None,
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    return render(request, 'user/mainPageUser.html', {'products': all_products, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})