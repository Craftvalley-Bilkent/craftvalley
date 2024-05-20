from datetime import date, datetime
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import base64

def customer_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.session.get('user_type') != 'Customer':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def get_categories():
    query = """
    SELECT 
        mc.main_category_name, 
        sc.sub_category_name 
    FROM 
        Main_Category mc
    JOIN 
        Sub_Category sc ON mc.main_category_id = sc.main_category_id
    ORDER BY 
        mc.main_category_name, sc.sub_category_name;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    all_categories = []
    current_category = None
    current_sub_categories = []

    for row in rows:
        category_name, sub_category_name = row
        if current_category != category_name:
            if current_category:
                all_categories.append({
                    'category_name': current_category,
                    'sub_categories': [{'sub_category_name': sub} for sub in current_sub_categories]
                })
            current_category = category_name
            current_sub_categories = []
        current_sub_categories.append(sub_category_name)

    # Append the last category
    if current_category:
        all_categories.append({
            'category_name': current_category,
            'sub_categories': [{'sub_category_name': sub} for sub in current_sub_categories]
        })

    return all_categories

@csrf_exempt
@customer_only
def showProducts(request):
    user_id = request.session.get("user_id")
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'postRating':
            product_id = request.POST.get('product_id')
            rating_value = request.POST.get('rating')
            user_id = user_id
            with connection.cursor() as cursor:
                product_data = [(user_id, product_id, rating_value)]
                sql_query = "INSERT INTO Rate(customer_id, product_id, star) VALUES (%s, %s, %s)"
                for data in product_data:
                    cursor.execute(sql_query, data)

        elif action == 'addToCart':
            product_id = request.POST.get('productId')
            amount = request.POST.get('amount')
            user_id = user_id
            with connection.cursor() as cursor:
                cursor.callproc('CartAdder', (user_id, product_id, amount))
                
            connection.commit()
        elif action == 'addToWishlist':
            product_id = request.POST.get('productId')
            situation = request.POST.get('situation')
            user_id = user_id
            with connection.cursor() as cursor:
                if situation == "remove":
                    cursor.execute("DELETE FROM Wish WHERE product_id = %s AND customer_id = %s", [product_id, user_id])
                else:
                    cursor.execute("INSERT INTO Wish(customer_id, product_id) VALUES(%s, %s)", [user_id, product_id])
    
        elif action == 'reportBusiness':
            product_id = request.POST.get('productId')
            reason = request.POST.get('reason')
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Has_Reported (customer_id, small_business_id, report_description, report_date)
                    VALUES (%s, (SELECT small_business_id FROM Add_Product WHERE product_id = %s), %s, NOW())
                """, [user_id, product_id, reason])
            return JsonResponse({'message': 'Report submitted successfully'})

    #TEST
    temp_query = "SELECT COUNT(*) AS numOfProducts FROM Product"
    action = ""
    business_name = ""
    min_price = ""
    max_price = ""

    if request.method == 'GET':
        action = request.GET.get('action')
        
        if action != 'base':
            business_name = request.GET.get('business_name')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            product_name = request.GET.get('product_name')
            recipient_name = request.GET.get('recipient')
            material_name = request.GET.get('material')

            temp_query = """SELECT COUNT(*) AS numOfProducts FROM Product
            JOIN Add_Product ON Product.product_id = Add_Product.product_id
            JOIN Small_Business ON Add_Product.small_business_id = Small_Business.user_id
            LEFT JOIN Made_By ON Product.product_id = Made_By.product_id
            LEFT JOIN Is_For ON Product.product_id = Is_For.product_id
            WHERE 1 = 1
            """

            if business_name:
                temp_query += " AND Small_Business.business_name LIKE('%" + business_name + "%')"
            if min_price:                  
                temp_query += " AND Product.price >= " + min_price
            if max_price:                  
                temp_query += " AND Product.price <= " + max_price 
            if product_name:
                temp_query += " AND Product.title LIKE('%" + product_name + "%')"
            if recipient_name:
                temp_query += " AND Is_For.recipient_id = '" + recipient_name + "'"
            if material_name:
                temp_query += " AND Made_By.material_id = '" + material_name + "'"  

    with connection.cursor() as cursor:
        cursor.execute(temp_query)
        row = cursor.fetchone()
    
    total_products = row[0]

    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        if action == 'isFiltered':
            cursor.callproc("ProductFilter", (per_page, start_index, business_name, float(min_price or 0), float(max_price or 99999999.99), 0, user_id, product_name, recipient_name, material_name))
        elif action == 'isSorted':
            sort_method = request.GET.get('sortMethod')
            cursor.callproc("ProductFilter", (per_page, start_index, business_name, float(min_price or 0), float(max_price or 99999999.99), int(sort_method), user_id, product_name, recipient_name, material_name))
        else:
            cursor.callproc("ProductPrinter", (per_page, start_index, user_id))
        
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
            'isWished': row[9],
            'busName': row[8]
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    all_categories = get_categories()

    with connection.cursor() as cursor:
        cursor.execute("SELECT recipient_id, recipient_name FROM Recipient")
        recipients = cursor.fetchall()
        
        cursor.execute("SELECT material_id, material_name FROM Material")
        materials = cursor.fetchall()
    
    return render(request, 'user/mainPageUser.html', {'products': all_products, 'categories': all_categories, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products, 'recipients': recipients, 'materials': materials})

@customer_only
def showCart(request):
    all_categories = get_categories()
    user_id = request.session.get("user_id")
    cart_items = []
    total_price = 0.0
    balance = 0.0
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT balance 
            FROM Customer 
            WHERE user_id = %s
        """, [user_id])
        balance = cursor.fetchone()[0]

        cursor.execute("""
            SELECT P.product_id, P.title, P.description, P.price, C.count, P.images 
            FROM Add_To_Shopping_Cart C
            JOIN Product P ON C.product_id = P.product_id
            WHERE C.customer_id = %s
        """, [user_id])
        raw_cart_items = cursor.fetchall()

        for item in raw_cart_items:
            product_id, title, description, price, count, images = item
            total = price * count
            total_price += float(total)
            cart_items.append((product_id, title, description, price, count, images, total))

    context = {
        'categories': all_categories,
        'cart_items': cart_items,
        'balance': balance,
        'total_price': total_price,
    }
    
    return render(request, "user/shoppingCart.html", context)

@csrf_exempt
@customer_only
def process_purchase(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        data = json.loads(request.body)
        balance = data.get('balance')
        total_price = data.get('total_price')

        if balance < total_price:
            return JsonResponse({'success': False, 'error': 'Insufficient balance'})

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Customer 
                    SET balance = balance - %s
                    WHERE user_id = %s
                """, [total_price, user_id])

                cursor.execute("""
                    INSERT INTO Balance_Record (record_date, record_type, record_amount)
                    VALUES (NOW(), 'purchase', %s)
                """, [-total_price])

                cursor.execute("""
                    INSERT INTO Customer_Has_Record (customer_id, record_id)
                    VALUES (%s, LAST_INSERT_ID())
                """, [user_id])

                cursor.execute("""
                    SELECT product_id, count
                    FROM Add_To_Shopping_Cart
                    WHERE customer_id = %s
                """, [user_id])
                cart_items = cursor.fetchall()

                business_balance_updates = {}

                for item in cart_items:
                    product_id, count = item
                    cursor.execute("""
                        SELECT AP.small_business_id, P.price
                        FROM Add_Product AP
                        JOIN Product P ON AP.product_id = P.product_id
                        WHERE AP.product_id = %s
                    """, [product_id])
                    small_business_id, price = cursor.fetchone()

                    total_item_price = price * count
                    if small_business_id in business_balance_updates:
                        business_balance_updates[small_business_id] += total_item_price
                    else:
                        business_balance_updates[small_business_id] = total_item_price

                    cursor.execute("""
                        INSERT INTO Transaction (product_id, customer_id, small_business_id, transaction_date, count, transaction_status)
                        SELECT %s, %s, AP.small_business_id, NOW(), %s, 'Completed'
                        FROM Add_Product AP
                        WHERE AP.product_id = %s
                    """, [product_id, user_id, count, product_id])

                    cursor.execute("""
                        UPDATE Product
                        SET amount = amount - %s
                        WHERE product_id = %s
                    """, [count, product_id])

                for business_id, amount in business_balance_updates.items():
                    cursor.execute("""
                        UPDATE Small_Business
                        SET balance = balance + %s
                        WHERE user_id = %s
                    """, [amount, business_id])
                    print("ok1")

                    cursor.execute("""
                        INSERT INTO Balance_Record (record_date, record_type, record_amount)
                        VALUES (NOW(), 'sale', %s)
                    """, [amount])
                    print("ok2")

                    cursor.execute("""
                        INSERT INTO Business_Has_Record (small_business_id, record_id)
                        VALUES (%s, LAST_INSERT_ID())
                    """, [business_id])
                    print("ok3")

                cursor.execute("""
                    DELETE FROM Add_To_Shopping_Cart
                    WHERE customer_id = %s
                """, [user_id])

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@customer_only
def remove_from_cart(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        data = json.loads(request.body)
        product_id = data.get('product_id')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT count FROM Add_To_Shopping_Cart
                WHERE customer_id = %s AND product_id = %s
            """, [user_id, product_id])
            amount = cursor.fetchone()[0]
            cursor.execute("""
                DELETE FROM Add_To_Shopping_Cart
                WHERE customer_id = %s AND product_id = %s
            """, [user_id, product_id])

            cursor.execute(""" 
                UPDATE Product
                SET amount = amount + %s 
                WHERE product_id = %s
            """, [amount, product_id])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@customer_only
def add_balance(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        data = json.loads(request.body)
        amount = data.get('amount')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Customer 
                SET balance = balance + %s
                WHERE user_id = %s
            """, [amount, user_id])

            cursor.execute("""
                INSERT INTO Balance_Record (record_date, record_type, record_amount)
                VALUES (NOW(), 'deposit', %s)
            """, [amount])

            cursor.execute("""
                INSERT INTO Customer_Has_Record (customer_id, record_id)
                VALUES (%s, LAST_INSERT_ID())
            """, [user_id])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@customer_only
def showTransactions(request):
    user_id = request.session.get("user_id")
    all_categories = get_categories()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'returnProduct':
            product_id = request.POST.get('productId')
            trans_date = request.POST.get('transDate')
            trans_id = request.POST.get('transId')
            bus_id = request.POST.get('busId')
            trans_date = datetime.strptime(trans_date, '%m-%d-%Y').date()

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT count, price
                    FROM Transaction T
                    JOIN Product P ON T.product_id = P.product_id
                    WHERE T.transaction_id = %s
                """, [trans_id])
                count, price = cursor.fetchone()
                total_refund = count * price

                cursor.execute("""
                    UPDATE Transaction
                    SET transaction_status = 'Returned'
                    WHERE transaction_id = %s
                """, [trans_id])

                cursor.execute("""
                    UPDATE Product
                    SET amount = amount + %s
                    WHERE product_id = %s
                """, [count, product_id])

                cursor.execute("""
                    UPDATE Customer
                    SET balance = balance + %s
                    WHERE user_id = %s
                """, [total_refund, user_id])

                cursor.execute("""
                    INSERT INTO Balance_Record (record_date, record_type, record_amount)
                    VALUES (NOW(), 'refund', %s)
                """, [total_refund])

                cursor.execute("""
                    INSERT INTO Customer_Has_Record (customer_id, record_id)
                    VALUES (%s, LAST_INSERT_ID())
                """, [user_id])

                cursor.execute("""
                    UPDATE Small_Business
                    SET balance = balance - %s
                    WHERE user_id = %s
                """, [total_refund, bus_id])

                cursor.execute("""
                    INSERT INTO Balance_Record (record_date, record_type, record_amount)
                    VALUES (NOW(), 'sale reversal', %s)
                """, [-total_refund])

                cursor.execute("""
                    INSERT INTO Business_Has_Record (small_business_id, record_id)
                    VALUES (%s, LAST_INSERT_ID())
                """, [bus_id])

        if action == 'rateProduct':
            product_id = request.POST.get('productId')
            rate = request.POST.get('rate')
            user_id = request.session.get("user_id")
            with connection.cursor() as cursor:
                cursor.callproc('RateProduct', (user_id, product_id, rate))

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS numOfProducts FROM Transaction WHERE customer_id = %s", [user_id])
        row = cursor.fetchone()
    
    total_products = row[0]
    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM UserTransactions WHERE customer_id = %s ORDER BY transaction_id DESC LIMIT %s OFFSET %s", [user_id, per_page, start_index])
        rows = cursor.fetchall()

    all_products = []
    for row in rows:
        transaction_date = datetime.strptime(row[7], '%m-%d-%Y').strftime('%m-%d-%Y')
        product = {
            'product_id': row[0],
            'title': row[1],
            'images': base64.b64encode(row[2]).decode() if row[2] else None,
            'description': row[3],
            'price': row[4],
            'business_id': row[5],
            'business_name': row[6],
            'transaction_date': transaction_date,
            'amount': row[8],
            'status': row[9],
            'rating': row[10],
            'transaction_id': row[12]
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))
    return render(request, "user/transactions.html", {'categories': all_categories, 'products': all_products, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products})

@customer_only
def showCategoryProducts(request, category, subcategory):
    user_id = request.session.get("user_id")
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'postRating':
            product_id = request.POST.get('product_id')
            rating_value = request.POST.get('rating')
            user_id = user_id
            with connection.cursor() as cursor:
                product_data = [(user_id, product_id, rating_value)]
                sql_query = "INSERT INTO Rate(customer_id, product_id, star) VALUES (%s, %s, %s)"
                for data in product_data:
                    cursor.execute(sql_query, data)

        elif action == 'addToCart':
            product_id = request.POST.get('productId')
            amount = request.POST.get('amount')
            user_id = user_id
            with connection.cursor() as cursor:
                cursor.callproc('CartAdder', (user_id, product_id, amount))
                
            connection.commit()
        elif action == 'addToWishlist':
            product_id = request.POST.get('productId')
            situation = request.POST.get('situation')
            user_id = user_id
            with connection.cursor() as cursor:
                if situation == "remove":
                    cursor.execute("DELETE FROM Wish WHERE product_id = %s AND customer_id = %s", [product_id, user_id])
                else:
                    cursor.execute("INSERT INTO Wish(customer_id, product_id) VALUES(%s, %s)", [user_id, product_id])

        elif action == 'reportBusiness':
            product_id = request.POST.get('productId')
            reason = request.POST.get('reason')
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Has_Reported (customer_id, small_business_id, report_description, report_date)
                    VALUES (%s, (SELECT small_business_id FROM Add_Product WHERE product_id = %s), %s, NOW())
                """, [user_id, product_id, reason])
            return JsonResponse({'message': 'Report submitted successfully'})

    temp_query = """SELECT COUNT(*) AS numOfProducts 
                    FROM Product 
                    JOIN In_Category ON Product.product_id = In_Category.product_id
                    JOIN Sub_Category ON In_Category.sub_category_id = Sub_Category.sub_category_id 
                    JOIN Main_Category ON In_Category.main_category_id = Main_Category.main_category_id 
                    WHERE Main_Category.main_category_name = %s 
                    AND Sub_Category.sub_category_name = %s"""
    query_params = [category, subcategory]

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

            query_params = [category, subcategory]

            if business_name:
                temp_query += " AND Small_Business.business_name LIKE %s"
                query_params.append(f'%{business_name}%')
            if min_price:
                temp_query += " AND Product.price >= %s"
                query_params.append(min_price)
            if max_price:
                temp_query += " AND Product.price <= %s"
                query_params.append(max_price)

    with connection.cursor() as cursor:
        cursor.execute(temp_query, query_params)
        row = cursor.fetchone()

    total_products = row[0]

    per_page = 16
    total_pages = (total_products + per_page - 1) // per_page 
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)

    with connection.cursor() as cursor:
        if action == 'isSorted':
            sort_method = request.GET.get('sortMethod')
            cursor.callproc("CategoryProductFilter", (per_page, start_index, business_name, float(min_price or 0), float(max_price or 99999999.99), int(sort_method), user_id, category, subcategory))
        else:
            cursor.callproc("CategoryProductFilter", (per_page, start_index, business_name, float(min_price or 0), float(max_price or 99999999.99), 0, user_id, category, subcategory))
        
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
            'isWished': row[9],
            'busName': row[8]
        }
        all_products.append(product)

    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    all_categories = get_categories()

    with connection.cursor() as cursor:
        cursor.execute("SELECT recipient_id, recipient_name FROM Recipient")
        recipients = cursor.fetchall()
        
        cursor.execute("SELECT material_id, material_name FROM Material")
        materials = cursor.fetchall()
    
    return render(request, 'user/categoryPage.html', {'products': all_products, 'categories': all_categories, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages, 'numOfProducts': total_products, 'category': category, 'subcategory': subcategory, 'recipients': recipients, 'materials': materials})

@csrf_exempt
@customer_only
def wishlist_view(request):
    user_id = request.session.get("user_id")

    all_categories = get_categories()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT P.product_id, P.title, P.description, P.price, W.customer_id
            FROM Product P
            JOIN Wish W ON P.product_id = W.product_id
            WHERE W.customer_id = %s
        """, [user_id])
        wishlist_items = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        amount = request.POST.get('amount')

        if action == 'addToCart':
            with connection.cursor() as cursor:
                cursor.execute("CALL CartAdder(%s, %s, %s)", [user_id, product_id, amount])
                cursor.execute("DELETE FROM Wish WHERE customer_id = %s AND product_id = %s", [user_id, product_id])
            return JsonResponse({'success': True})

        elif action == 'removeFromWishlist':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Wish WHERE customer_id = %s AND product_id = %s", [user_id, product_id])
            return JsonResponse({'success': True})
        
    return render(request, 'user/wishlist.html', {'categories': all_categories, 'wishlist_items': wishlist_items})

@csrf_exempt
@customer_only
def show_balance_records(request):
    user_id = request.session.get("user_id")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Balance_Record BR
            JOIN Customer_Has_Record CHR ON BR.record_id = CHR.record_id
            WHERE CHR.customer_id = %s
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
            JOIN Customer_Has_Record CHR ON BR.record_id = CHR.record_id
            WHERE CHR.customer_id = %s
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

    return render(request, 'user/balanceRecords.html', {
        'balance_records': balance_records, 
        'current_page': current_page, 
        'total_pages': total_pages, 
        'page_range': page_range
    })

