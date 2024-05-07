from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)

def showProducts(request):
    all_products = [
        {'name': f'Product {i}', 'description': f'Description for Product {i}', 'price': i * 10}
        for i in range(1, 101)  
    ]
    
    # Pagination logic
    per_page = 16
    total_products = len(all_products)
    total_pages = (total_products + per_page - 1) // per_page  # Calculate total pages
    current_page = int(request.GET.get('page', 1))
    start_index = max(0, (current_page - 1) * per_page)
    end_index = min(start_index + per_page, total_products)
    products = all_products[start_index:end_index]

    # Generate page range for pagination links
    page_range = range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))

    return render(request, 'user/mainPageUser.html', {'products': products, 'page_range': page_range, 'current_page': current_page, 'total_pages': total_pages})

