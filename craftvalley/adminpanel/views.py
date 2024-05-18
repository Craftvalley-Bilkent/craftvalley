from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

def raw_sql_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        else:
            return None

def admin_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.user_type != 'Admin':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

# @login_required
# @admin_only
def admin_dashboard(request):
    reported_businesses = raw_sql_query("""
        SELECT B.user_id, B.business_name, C.user_id, H.report_description, H.report_date
        FROM Small_Business as B, Customer as C, Has_Reported as H
        WHERE B.user_id = H.small_business_id AND C.user_id = H.customer_id
    """)

    popular_products = raw_sql_query("""
        SELECT product_id, title, total_sales
        FROM (
            SELECT P.product_id, P.title, SUM(T.count) AS total_sales
            FROM Product P
            JOIN Transaction T ON P.product_id = T.product_id
            GROUP BY P.product_id, P.title
            ORDER BY total_sales DESC
        ) AS popular_products
    """)

    user_trends = raw_sql_query("""
        SELECT user_id, user_name, COUNT(*) AS activity_count
        FROM (
            SELECT U.user_id, U.user_name
            FROM User U
            JOIN Transaction T ON U.user_id = T.customer_id
            UNION ALL
            SELECT U.user_id, U.user_name
            FROM User U
            JOIN Has_Reported HR ON U.user_id = HR.customer_id
        ) AS user_activity
        GROUP BY user_id, user_name
        ORDER BY activity_count DESC
    """)

    platform_performance = raw_sql_query("""
        SELECT 
            (SELECT COUNT(*) FROM User) AS total_users, 
            (SELECT COUNT(*) FROM Product) AS total_products, 
            (SELECT COUNT(*) FROM Transaction) AS total_transactions
    """)

    date_from = request.GET.get('date_from', '2023-01-01')
    date_to = request.GET.get('date_to', datetime.now().strftime('%Y-%m-%d'))

    most_least_sold_products = raw_sql_query("""
        SELECT P.product_id, P.title, SUM(T.count) AS total_sales
        FROM Product P
        JOIN Transaction T ON P.product_id = T.product_id
        WHERE T.transaction_date BETWEEN %s AND %s
        GROUP BY P.product_id, P.title
        ORDER BY total_sales DESC
    """, [date_from, date_to])

    most_least_sold_businesses = raw_sql_query("""
        SELECT B.user_id, B.business_name, SUM(T.count) AS total_sales
        FROM Small_Business B
        JOIN Transaction T ON B.user_id = T.small_business_id
        WHERE T.transaction_date BETWEEN %s AND %s
        GROUP BY B.user_id, B.business_name
        ORDER BY total_sales DESC
    """, [date_from, date_to])

    avg_sales_per_product = raw_sql_query("""
        SELECT P.product_id, P.title, AVG(T.count) AS average_sales
        FROM Product P
        JOIN Transaction T ON P.product_id = T.product_id
        WHERE T.transaction_date BETWEEN %s AND %s
        GROUP BY P.product_id, P.title
    """, [date_from, date_to])

    context = {
        'reported_businesses': reported_businesses,
        'popular_products': popular_products,
        'user_trends': user_trends,
        'platform_performance': platform_performance[0] if platform_performance else None,
        'most_least_sold_products': most_least_sold_products,
        'most_least_sold_businesses': most_least_sold_businesses,
        'avg_sales_per_product': avg_sales_per_product,
        'date_from': date_from,
        'date_to': date_to,
    }

    return render(request, 'adminpanel/dashboard.html', context)

# @login_required
# @admin_only
def ban_business(request, business_id):
    admin_id = request.user.id  # Assuming the logged-in user is an admin
    ban_duration = "Indefinite"
    raw_sql_query("""
        INSERT INTO Ban (admin_id, small_business_id, ban_duration, ban_date)
        VALUES (%s, %s, %s, NOW())
    """, [admin_id, business_id, ban_duration])
    return redirect('admin_dashboard')

# @login_required
# @admin_only
def ban_details(request, business_id):
    ban_details = raw_sql_query("""
        SELECT B.user_id, B.business_name, Ban.ban_duration, Ban.ban_date
        FROM Small_Business as B, Ban
        WHERE B.user_id = Ban.small_business_id AND Ban.small_business_id = %s
    """, [business_id])
    if ban_details:
        return JsonResponse({'business_id': ban_details[0][0], 'business_name': ban_details[0][1], 'ban_duration': ban_details[0][2], 'ban_date': ban_details[0][3]})
    else:
        return JsonResponse({'error': 'No ban details found.'})
