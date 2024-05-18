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


# Add product
@csrf_exempt
def showProducts(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'postRating':
            productId = request.POST.get('product_id')
            ratingValue = request.POST.get('rating')
            userId = 3
            with connection.cursor() as cursor:
                product_data = [(userId, productId, ratingValue)]
                sql_query = "INSERT INTO Rate(customer_id, product_id, star) VALUES (%s, %s, %s)"
                for data in product_data:
                    cursor.execute(sql_query, data)

        elif action == 'addToCart':
            productId = request.POST.get('productId')
            amount = request.POST.get('amount')
            userId = 3
            with connection.cursor() as cursor:
                cursor.callproc('CartAdder', (userId, productId, amount))
                
            connection.commit()
        elif action == 'addToWishlist':
            productId = request.POST.get('productId')
            situation = request.POST.get('situation')
            userId = 3
            with connection.cursor() as cursor:
                if(situation == "remove"):
                    cursor.execute("DELETE FROM Wish Where product_id = " + str(productId) + " AND customer_id = " + str(userId))
                else:
                    cursor.execute("INSERT INTO Wish(customer_id, product_id) VALUES(" + str(userId) + ", " + str(productId) + ")")
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
                temp_query = temp_query + " AND Small_Business.business_name LIKE('% " + business_name + " %')  AND 2 = 2"
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
            cursor.callproc("ProductFilter", (per_page, start_index, business_name,  float(min_price or 0), float(max_price or 99999999.99), 0))
        elif (action == 'isSorted'):
            sortMethod = request.GET.get('sortMethod')
            cursor.callproc("ProductFilter", (per_page, start_index, business_name,  float(min_price or 0), float(max_price or 99999999.99), int(sortMethod)))
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

    sub_category = [{'sub_category_name': 'sub1'},{'sub_category_name': 'sub1'},{'sub_category_name': 'sub1'}]
    all_categories = [
        {'category_name': 'category1', 'sub_categories': sub_category},
        {'category_name': 'category2', 'sub_categories': sub_category},
        {'category_name': 'category3', 'sub_categories': sub_category},
        {'category_name': 'category4', 'sub_categories': sub_category},
        {'category_name': 'category5', 'sub_categories': sub_category},
        {'category_name': 'category6', 'sub_categories': sub_category},
        {'category_name': 'category7', 'sub_categories': sub_category},
        {'category_name': 'category8', 'sub_categories': sub_category}
    ]


    with connection.cursor() as cursor:
        cursor.execute("SELECT product_id FROM Wish WHERE customer_id = 3")
        rows = cursor.fetchall()

    all_wished_products = []
    for row in rows:
        wished_product = {
            'product_id': row[0],
        }
        all_wished_products.append(wished_product)
    i = 0
    j = 0
    while (j < len(all_wished_products)) and (i < len(all_products)):
        if(all_wished_products[j]['product_id'] == all_products[i]['product_id']):
            all_products[i]['isWished'] = 1
            i += 1
            j += 1
        else:
            i += 1
    
    return render(request, 'user/mainPageUser.html', {'products': all_products, 'categories': all_categories, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})

def showCart(request):
    return render(request, "user/shoppingCart.html")

def showTransactions(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS numOfProducts FROM Product WHERE user_id = 3")
        row = cursor.fetchone()
    
    total_products = row[0]
    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM UserTransactions WHERE customer_id = 3 ORDER BY P.product_id DESC LIMIT " + str(per_page) + " OFFSET "  + str(start_index))
        rows = cursor.fetchall()

    all_products = []
    for row in rows:
        product = {
            'product_id': row[0],
            'title': row[1],
            'images': base64.b64encode(row[2]).decode() if row[2] else None,
            'description': row[3],
            'price': row[4],
            'business_id': row[5],
            'business_name': row[6],
            'transaction_date': row[7],
            'amount': row[8],
            'status': row[9],
            'rating': row[10],
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    return render(request, "user/transactions.html", {'products': all_products, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})