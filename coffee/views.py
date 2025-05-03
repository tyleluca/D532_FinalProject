from django.shortcuts import render
from .models import Transaction, Store, Product
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Sum, F
import random
import json

def home(request):
    # Home welcome page.  No special logic on this page.
    return render(request, 'home.html')

def transaction_list(request):
    # User filters on one or many stores or products and chooses a date range.  Website then renders all transactions with these criteria. 
    selectedStoreLocation = request.GET.getlist("storeLocation")
    selectedProductDetail = request.GET.getlist("productDetail")
    startDate = request.GET.get("start_date")
    endDate = request.GET.get("end_date")

    if "" in selectedStoreLocation:
        selectedStoreLocation = []

    if "" in selectedProductDetail:
        selectedProductDetail = []

    transactions = Transaction.objects.none()

    if selectedStoreLocation or selectedProductDetail or startDate or endDate:
        transactions = Transaction.objects.all()
    
        if selectedStoreLocation:
            transactions = transactions.filter(storeId__storeLocation__in=selectedStoreLocation)
        if selectedProductDetail:
            transactions = transactions.filter(productId__productDetail__in=selectedProductDetail)
        if startDate:
            transactions = transactions.filter(transactionDatetime__date__gte=parse_date(startDate))
        if endDate:
            transactions = transactions.filter(transactionDatetime__date__lte=parse_date(endDate))

        transactions = transactions.select_related("storeId", "productId").order_by("-transactionDatetime")

    storeLocations = Store.objects.values_list("storeLocation", flat=True).distinct().order_by("storeLocation")
    products = Product.objects.all().order_by('productCategory', 'productType', 'productDetail')

    return render(request, "transaction_list.html", {
        "transactions": transactions,
        "storeLocations": storeLocations,
        "productDetails": products,
        "start_date": startDate,
        "end_date": endDate,
    })

def purchase_coffee(request):
    # User selects a store, product, and quantity, and the website then uploads this data to the transaction table.
    stores = Store.objects.all()
    products = Product.objects.all().order_by('productCategory', 'productType', 'productDetail')
    qty = 0

    if request.method == 'POST':

        selectedStoreLocation = request.POST.get('storeLocation')
        selectedProductDetail = request.POST.get('productDetail')
        qty = int(request.POST.get('quantity'))

        if selectedStoreLocation and selectedProductDetail and qty:
            store = Store.objects.get(storeLocation=selectedStoreLocation)
            product = Product.objects.get(productDetail=selectedProductDetail)
            unitPrice = round(random.uniform(2, 5), 2)

            Transaction.objects.create(
                storeId=store,
                productId=product,
                transactionQty=qty,
                unitPrice=unitPrice,
                transactionDatetime = timezone.localtime(timezone.now())
                )

            
    return render(request, 'purchase_coffee.html', {
        'stores': stores,
        'products': products,
        'quantity': qty
    })

def add_product(request):
    # Adding product to product table from user input
    if request.method == 'POST':
        productCategory = request.POST.get('productCategory')
        productType = request.POST.get('productType')
        productDetail = request.POST.get('productDetail')

        if productCategory and productType and productDetail:
            Product.objects.create(
                productCategory=productCategory,
                productType=productType,
                productDetail=productDetail
            )
    products = Product.objects.all().order_by('productCategory', 'productType')

    return render(request, 'add_product.html', {
        'products': products
    })

def sales_dashboard(request):

    # Bar chart: Total sales by product category
    category_sales = (
        Transaction.objects
        .values('productId__productCategory')
        .annotate(total_sales=Sum(F('transactionQty') * F('unitPrice')))
        .order_by('-total_sales')
    )

    # Bar chart: Total sales by product type
    type_sales = (
        Transaction.objects
        .values('productId__productType')
        .annotate(total_sales=Sum(F('transactionQty') * F('unitPrice')))
        .order_by('-total_sales')
    )

    category_labels = json.dumps([cat['productId__productCategory'] for cat in category_sales])
    category_values = json.dumps([float(cat['total_sales']) for cat in category_sales])

    type_labels = json.dumps([type['productId__productType'] for type in type_sales])
    type_values = json.dumps([float(type['total_sales']) for type in type_sales])

    return render(request, 'sales_dashboard.html', {
        'category_labels': category_labels,
        'category_values': category_values,
        'type_labels': type_labels,
        'type_values': type_values
    })