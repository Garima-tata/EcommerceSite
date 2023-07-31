from math import ceil
from django.http import JsonResponse
from django.shortcuts import render, redirect
from SiteApp.models import  Product


# Create your views here.
def products(request):
    return render(request, 'products.html')

def home(request):
    current_user = request.user
    print(current_user)
    allProds = []
    carProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in carProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    
    product_qnt=0
    product_id=0
    product_price=0
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qnt = request.POST.get('prod_qnt')
        product_price = Product.objects.get(product_id=product_id).price
        print(product_id, product_qnt)
        
    return render(request, 'index.html', {'product_id':product_id, 'product_qnt':product_qnt,   'product_price':product_price, 'allProds':allProds})


# def CartController(request):
    
#     if request.method=='POST':
#         if request.user.is_authenticated:
#             prod_id = int(request.POST.get('prod_id'))
#             product_check = Product.objects.get(id=prod_id)
#             prod_qnt = int(request.POST.get('prod_qnt'))
#             cart = Cart.objects.create(user=request.user, Product=product_check, product_quantity=prod_qnt)
#             return JsonResponse({'status':'Product added to cart'})
#             # if(product_check):
#             #     if(Cart.objects.filter(user=request.user, Product=product_check)):
#             #         cart = Cart.objects.get(user=request.user, Product=product_check)
#             #         cart.product_quantity += 1
#             #         cart.save()
#             #         return JsonResponse({'status':'Product added to cart'})
#             #     else:
#             #         prod_qnt = int(request.POST.get('prod_qnt'))
#             #         if product_check.quantity >= prod_qnt:
#             #             cart = Cart.objects.create(user=request.user, Product=product_check, product_quantity=prod_qnt)
#                         # cart.save()
#                         # return JsonResponse({'status':'Product added to cart'})
#                     # else:
#                         # return ()
#             # else:
#             #     return JsonResponse({'status':'Product not found'})
#         else:
#             return JsonResponse({'status':'Please login first'})
#     return render(request, 'index.html', {'prod_qnt':prod_qnt})


# def cartItem(request):
#     if request.user.is_authenticated:
#     #     cart = Cart.objects.filter(user=request.user)
#     #     total = 0
#     #     for item in cart:
#     #         total += item.Product.price * item.product_quantity
#         return render(request, 'cartItem.html')
#     else:
#         return redirect('/SiteAuth/login')