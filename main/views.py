from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib import messages 
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import hashlib
from django.contrib import auth
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from .models import Review, OrderItem, Product, ShippingAddress, Store, Category, SubCategory, SubsCategory, Order, Templates, UserStore, ContactUs, ImageBlog
from .forms import StoreForm, StoreEditForm, CategoryForm, SubCategoryForm, SubsCategoryForm, ProductForm, OrderItemForm, ShippingAddressForm,ReviewForm, TemplateForm, ContactUsForm, ImageForm


@never_cache
def Index(request):
    stores = Store.objects.filter(confirmed = 1).order_by('id')
    return render (request,'user/list-store.html',{'stores':stores})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def Dashboard(request):
    count_category = Category.objects.filter(user_id = request.user.pk).count()
    count_subcategory = SubCategory.objects.filter(user_id = request.user.pk).count()
    count_subscategory = SubsCategory.objects.filter(user_id = request.user.pk).count()
    count_product = Product.objects.filter(user_id = request.user.pk).count()
    count_order = Product.objects.filter(user_id = request.user.pk).count()
    count_user = UserStore.objects.filter(store_id = request.user.store_id,is_user_store = 1).count()
    count_review = Review.objects.filter(store_id = request.user.store_id).count()
    count_review_perfect = Review.objects.filter(store_id = request.user.store_id,rating = 5).count()
    count_review_poor = Review.objects.filter(store_id = request.user.store_id,rating = 1).count()
    return render (request,'dashboard.html',{'count_review_poor':count_review_poor,'count_review_perfect':count_review_perfect,'count_review':count_review,'count_user':count_user,'count_order':count_order,'count_product':count_product,'count_category':count_category,'count_subcategory':count_subcategory,'count_subscategory':count_subscategory})

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def DashboardUser(request):
    count_order = Order.objects.filter(user_id = request.user.pk).count()
    count_review = Review.objects.filter(user_id = request.user.pk).count()
    return render (request,'user/screen/dashboard.html',{'count_order':count_order,'count_review':count_review})

@never_cache
def AgreeAdmin(request):
    return render (request,'agree-admin.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def StoreListView(request):
    stores = Store.objects.filter(user_id = request.user.id)
    if stores:
        store = Store.objects.get(user_id = request.user.id)
    else:
        return redirect(reverse('store_create'))
    return render(request, 'screen/StoreListScreen.html',{'store':store})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def StoreCreateView(request):
    if request.user.is_admin_store == 1:
        stores = Store.objects.filter(user_id = request.user.id)
        if stores:
            messages.error(request,'کاربر عزیز شما وبلاگ خود را ایجاد کرده اید.')
            return redirect(reverse('store-details'))
        else:
            form = StoreForm
            if request.method == 'POST':
                form = StoreForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    store = Store.objects.get(user_id = request.user.id)
                    UserStore.objects.filter(pk = request.user.id).update(store_id = store.pk)
                    return redirect(reverse('store-details'))
                else:
                    messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    else:
        return redirect(reverse('login-admin-store'))
    return render(request, 'screen/StoreCreateScreen.html',{'form':form})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def StoreEditView(request, pk): 
    store = Store.objects.get(pk = pk)
    context ={'store':store} 
    obj = get_object_or_404(Store, pk = pk) 
    form = StoreEditForm(request.POST or None, request.FILES or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        Store.objects.filter(pk=pk).update(confirmed = 0)
        return redirect(reverse('store-list'))
    context["form"] = form 
    return render(request, "screen/StoreEditScreen.html", context) 

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def StoreDetailsView(request):
    stores = Store.objects.filter(user_id = request.user.id)
    if stores:
        store = Store.objects.get(user_id = request.user.id)
        cate = Category.objects.filter(store_id = store.pk)
        if not cate:
            categ = 0
        else:
            categ = 1
    else:
        return redirect(reverse('store_create'))
    return render(request, 'screen/StoreDetailsScreen.html',{'store':store,'categ':categ})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def CategoryCreateView(request,pk):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('category-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('category-create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/CategoryCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def CategoryListView(request):
    category = Category.objects.filter(user = request.user.id)
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    context = {'category':category,'subcategory':subcategory}
    return render(request, 'screen/CategoryListScreen.html',context)

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def CategoryDeleteView(request,pk):
    pro = Product.objects.filter(category_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = Category.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('category-list'))
    return render(request, 'screen/CategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def CategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(Category, pk = pk) 
    form = CategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('category-list'))
    context["form"] = form 
    return render(request, "screen/CategoryEditScreen.html", context) 

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def SubCategoryCreateView(request,pk,store_id):
    form = SubCategoryForm
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('subcategory-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('subcategory-create', args=[pk,store_id]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/SubCategoryCreateScreen.html',{'form':form,'pk':pk,'store_id': store_id})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def SubCategoryListView(request):
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/SubCategoryListScreen.html',{'subcategory':subcategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def SubCategoryDeleteView(request,pk):
    pro = Product.objects.filter(subcategory_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = SubCategory.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('subcategory-list'))
    return render(request, 'screen/SubCategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def SubCategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(SubCategory, pk = pk) 
    form = SubCategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('subcategory-list'))
    context["form"] = form 
    return render(request, "screen/SubCategoryEditScreen.html", context) 

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def SubsCategoryCreateView(request,pk,store_id):
    form = SubsCategoryForm
    if request.method == 'POST':
        form = SubsCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('subscategory-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('subscategory-create', args=[pk,store_id]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/SubsCategoryCreateScreen.html',{'form':form,'pk':pk,'store_id': store_id})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def SubsCategoryListView(request):
    subscategory = SubsCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/SubsCategoryListScreen.html',{'subscategory':subscategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def SubsCategoryDeleteView(request,pk):
    pro = Product.objects.filter(subscategory_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = SubsCategory.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('subscategory-list'))
    return render(request, 'screen/SubsCategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def SubsCategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(SubsCategory, pk = pk) 
    form = SubsCategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('subscategory-list'))
    context["form"] = form 
    return render(request, "screen/SubsCategoryEditScreen.html", context) 

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def ProductCreateView(request,pk):
    cat = Category.objects.filter(store_id = request.user.store_id)
    imageone = ImageBlog.objects.all().order_by('id')
    form = ProductForm(request=request)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('product-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('product-create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/ProductCreateScreen.html',{'form':form,'pk':pk,'imageone':imageone})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ProductListView(request):
    product = Product.objects.filter(user_id = request.user.id)
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/ProductListScreen.html',{'product':product,'subcategory':subcategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ProductDeleteView(request,pk):
    pro = OrderItem.objects.filter(product_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = Product.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('product-list'))
    return render(request, 'screen/ProductListScreen.html',{'delete_cat':delete_cat})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def ProductEditView(request, pk): 
    product = Product.objects.get(pk = pk)
    context ={'product':product} 
    form = ProductForm(request=request)
    obj = get_object_or_404(Product, pk = pk) 
    form = ProductForm(request.POST or None,request.FILES or None, instance = obj, request=request)     
    if form.is_valid(): 
        form.save() 
        Product.objects.filter(pk=pk).update(confirmed = 0)
        return redirect(reverse('product-list'))
    context["form"] = form 
    return render(request, "screen/ProductEditScreen.html", context) 

@never_cache
def load_subcategorys(request):
    category_id = request.GET.get('category_id')
    subcategory = SubCategory.objects.filter(category_id=category_id,store_id = request.user.store_id).all()
    return render(request, 'subcategory_dropdown_list_options.html', {'subcategory': subcategory})

@never_cache
def load_subscaegorys(request):
    subcategory_id = request.GET.get('subcategory_id')
    subscategory = SubsCategory.objects.filter(subcategory_id=subcategory_id,store_id = request.user.store_id).all()
    return render(request, 'subscategory_dropdown_list_options.html', {'subscategory': subscategory})

@never_cache
@csrf_exempt
def ProductListStoreView(request,pk):
    search = request.POST.get('search')
    if search:
        products = Product.objects.filter(store = pk,name__contains = search,confirmed = 1)
        store = Store.objects.get(pk = pk)
        category = Category.objects.filter(store = pk)
        subcategory = SubCategory.objects.filter(store = pk)
        subscategory = SubsCategory.objects.filter(store = pk)
    else:
        products = Product.objects.filter(store = pk,confirmed = 1)
        store = Store.objects.get(pk = pk)
        category = Category.objects.filter(store = pk)
        subcategory = SubCategory.objects.filter(store = pk)
        subscategory = SubsCategory.objects.filter(store = pk)
    return render(request, 'user/index.html',{'products':products,'category':category,'store':store,'subcategory':subcategory,'subscategory':subscategory})

@never_cache
def ListStoreView(request):
    stores = Store.objects.filter(confirmed = 1)
    return render(request, 'user/list-store.html',{'stores':stores})

@never_cache
@csrf_exempt
def ProductDetailsStoreView(request,pk,store_id,slug):
    nxt = request.GET.get("next", None)
    select_rating = Review.objects.filter(product_id = pk)
    products = Product.objects.get(pk = pk)
    store = Store.objects.get(pk = products.store.pk)
    fill_select_review = Review.objects.filter(user_id = request.user.id, product_id = pk)
    if request.method == 'POST':
        id_product = request.POST.get('product')
        id_datecreate = request.POST.get('datecreate')
        id_datecreatealt = request.POST.get('datecreatealt')
        id_comment = request.POST.get('comment')
        id_rating = request.POST.get('rating')
        if id_rating and id_comment:
            if not fill_select_review:
                if not request.user.id:
                    if nxt:
                        return redirect(nxt)
                    else:
                        return redirect(reverse('login-user-store', args=[store_id]))
                else:
                    Review.objects.create(comment = id_comment,rating = id_rating,store_id=request.user.store_id,product_id=id_product,datecreate=id_datecreate,datecreatealt=id_datecreatealt,user_id=request.user.id)
                    rev_avg = Review.objects.filter(store_id = store_id,product_id = pk).aggregate(Avg('rating')).get('rating__avg', 0.00)
                    Product.objects.filter(store_id = store_id,pk=pk).update(rating = rev_avg)
    return render(request, 'user/screen/product-details-screen.html',{'select_rating':select_rating,'products':products,'store':store})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginUserStore/')
def AddProductDetailsStoreView(request,pk,store_id,slug):
    products = Product.objects.get(pk = pk)
    store = Store.objects.get(pk = products.store.pk)
    form = OrderItemForm
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        id_product = request.POST['product']
        id_totalPrice = request.POST['totalPrice']
        id_datecreate = request.POST['datecreate']
        id_datecreatealt = request.POST['datecreatealt']
        id_price = request.POST['price']
        id_countInOrder = request.POST['countInOrder']
        sumprice = int(id_price) * int(id_countInOrder)
        if request.user.id:
            filter_product = OrderItem.objects.filter(product_id = pk,user_id=request.user.id,isfinal=False)
            order_filter = Order.objects.filter(user_id=request.user.id,isfinal=False)
            if not order_filter:
                Order.objects.create(store_id=request.user.store_id,totalPrice=sumprice,datecreate=id_datecreate,datecreatealt=id_datecreatealt,device=0,user_id=request.user.id)
            if filter_product:
                export_count = OrderItem.objects.get(product_id = pk,user_id=request.user.id,isfinal=False)
                if export_count:
                    print(export_count)
                    value_count = 0
                    value_count = int(export_count.countInOrder) + int(id_countInOrder)
                    OrderItem.objects.filter(product_id = pk,user_id=request.user.id).update(product_id=id_product,countInOrder=value_count,totalPrice=sumprice,datecreate=id_datecreate,datecreatealt=id_datecreatealt,price=id_price,user_id=request.user.id)
            else:
                id_order = Order.objects.get(user_id=request.user.id,isfinal=False)
                OrderItem.objects.create(store_id=id_order.store_id,product_id=id_product,order_id=id_order.pk,countInOrder=id_countInOrder,totalPrice=sumprice,datecreate=id_datecreate,datecreatealt=id_datecreatealt,price=id_price,device=0,user_id=request.user.id)
        if 'Order_create' in request.POST:
            return redirect(reverse('product-details-store', args=[pk,store_id]))
        elif 'Save_review' in request.POST:
            return redirect(reverse('category-create', args=[pk]))

    nxt = request.GET.get("next", None)
    fill_select_review = Review.objects.filter(user_id = request.user.id, product_id = pk)
    if 'Review_save' in request.POST:
        id_comment = request.POST.get('comment')
        id_rating = request.POST.get('rating')
        if id_rating and id_comment:
            if not fill_select_review:
                if not request.user.id:
                    if nxt:
                        return redirect(nxt)
                    else:
                        return redirect(reverse('login-user-store'))
                else:
                    Review.objects.create(comment = id_comment,rating = id_rating,store_id=request.user.store_id,product_id=id_product,datecreate=id_datecreate,datecreatealt=id_datecreatealt,user_id=request.user.id)
                    rev_avg = Review.objects.filter(store_id = store_id,product_id = pk).aggregate(Avg('rating')).get('rating__avg', 0.00)
                    Product.objects.filter(store_id = store_id,pk=pk).update(rating = rev_avg)
    return render(request, 'user/screen/product-details-screen.html',{'products':products,'form':form,'store':store})

@never_cache
def ProductListOrdersView(request,pk):
    if request.user.id:
        order = OrderItem.objects.filter(user_id=request.user.id).values_list('product',flat=True)[:1]
        if order:
            store = Store.objects.get(pk = pk)
            order_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False).count()
            order_item_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
            order_sum_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
            Order.objects.filter(user_id=request.user.id,isfinal=False).update(totalPrice = sum(order_item_count.values_list(F('price') * F('countInOrder'), flat=True)))
        else:
            return redirect(reverse('product-list-store', args=[pk]))
        orders_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
        orders = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
        if orders:
            shop = Order.objects.filter(user_id=request.user.id,isfinal=False).get(user_id=request.user.id,isfinal=False)
    context = {'orders':orders,'store':store,'orders_count':orders_count,'shop':shop,'order_count':order_count,'order_sum_count':order_sum_count}
    return render(request, 'user/screen/list-orders.html',context)

@never_cache
def ProductDeleteOrderView(request,pk,store_id,slug):
    if request.user.id:
        order = OrderItem.objects.filter(pk = pk,user_id=request.user.id,isfinal=False).delete()
        orderitem_fill = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
        if not orderitem_fill:
            Order.objects.filter(user_id=request.user.id).delete()
            return redirect(reverse('product-list-store', args=[store_id]))
        if order:
            return redirect(reverse('product-list-orders', args=[store_id]))
        return redirect(reverse('product-list-orders', args=[store_id]))
    return render(request, 'user/screen/list-orders.html')

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginUserStore/')
def ShoppingCreateView(request,pk):
    form = ShippingAddressForm
    select_address = ShippingAddress.objects.filter(user_id = request.user.id).exclude(address = None)
    select_add = request.POST.get('select_address')
    if select_add:
        ShippingAddress.objects.create(order_id = pk,selectaddress = select_add,user_id = request.user.id, store_id = request.user.store_id)
        select_address_get = ShippingAddress.objects.get(pk = select_add)
        if 'result_next' in request.POST:
            orders = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
            context = {'select_address_get':select_address_get,'select_address':select_address,'orders':orders,'disabled_page_two': 'disabled','disabled_page': 'disabled','py_page': '','result_page': 'show active','form':form,'pk':pk}
        fill_order_fill = ShippingAddress.objects.filter(order = pk)
        if fill_order_fill:
            fill_order = ShippingAddress.objects.get(order = pk)
            orders = OrderItem.objects.filter(order_id = pk,isfinal=False)
            order_sum_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
            context = {'select_address_get':select_address_get,'select_address':select_address,'order_sum_count':order_sum_count,'orders':orders,'fill_order':fill_order,'disabled_page_two': 'disabled','disabled_page': 'disabled','py_page': '','result_page': 'show active','form':form,'pk':pk}
        else:
            orders = OrderItem.objects.filter(order_id = pk,isfinal=False)
            context = {'disabled_page': '','select_address_get':select_address_get,'select_address':select_address,'orders':orders,'adress_page': 'show active','result_page': '','py_page': '','form':form,'pk':pk}       
    else:
        form = ShippingAddressForm
        context = {'adress_page': 'show active','form':form,'pk':pk}
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                if 'Save_Adress' in request.POST:
                    form.save()
                    context = {'disabled_page': 'disabled','py_page': 'show active','form':form,'pk':pk}
            else:
                messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
        if 'result_next' in request.POST:
            orders = OrderItem.objects.filter(user_id=request.user.id,isfinal=False)
            context = {'select_address':select_address,'orders':orders,'disabled_page_two': 'disabled','disabled_page': 'disabled','py_page': '','result_page': 'show active','form':form,'pk':pk}
        fill_order_fill = ShippingAddress.objects.filter(order = pk)
        if fill_order_fill:
            fill_order = ShippingAddress.objects.get(order = pk)
            orders = OrderItem.objects.filter(order_id = pk,isfinal=False)
            order_sum_count = OrderItem.objects.filter(user_id=request.user.id,isfinal=False).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
            context = {'select_address':select_address,'order_sum_count':order_sum_count,'orders':orders,'fill_order':fill_order,'disabled_page_two': 'disabled','disabled_page': 'disabled','py_page': '','result_page': 'show active','form':form,'pk':pk}
        else:
            orders = OrderItem.objects.filter(order_id = pk,isfinal=False)
            context = {'disabled_page': '','select_address':select_address,'orders':orders,'adress_page': 'show active','result_page': '','py_page': '','form':form,'pk':pk}
    return render(request, 'user/screen/shopping-orders.html',context)

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def ShoppingListUserOrdersView(request):
    orders = OrderItem.objects.filter(user_id = request.user.id)
    order = ShippingAddress.objects.filter(pk = pk)
    context = {'orders':orders,'order':order}
    return render(request, 'user/screen/shopping-orders-list-user.html',context)

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def ShoppingDetailsUserOrderView(request,pk,order_id):
    fill_order = ShippingAddress.objects.get(order_id = order_id)
    if fill_order.selectaddress:
        select_address_get = ShippingAddress.objects.get(pk = fill_order.selectaddress)
    else:
        select_address_get = ''
    fill_user = ShippingAddress.objects.filter(order_id = order_id).get(user_id=request.user.id)
    if fill_order:
        Order.objects.filter(pk= fill_order.order_id).update(isfinal=True,finalAt = timezone.now())
        orders = OrderItem.objects.filter(order_id = fill_order.order_id)
        for_orderitem = OrderItem.objects.filter(order_id= fill_order.order_id).values_list('order_id',flat=True)
        fill_ord_item = OrderItem.objects.filter(order_id= fill_order.order_id,isfinal=True).values_list('product_id',flat=True)
        for i in for_orderitem:
            OrderItem.objects.filter(order_id= i).update(isfinal=True)
            fill_count_item = OrderItem.objects.filter(order_id= i,isfinal=True).values('countInOrder')
        for s in fill_ord_item:
            fill_count_pro = Product.objects.filter(pk = s).values('countInStock')        
            for r in fill_count_pro:
                print('pro:',r['countInStock'])
        for g,e in zip(fill_count_item,fill_ord_item):
            print('order:',g['countInOrder'])
            countInStock = r['countInStock']-g['countInOrder']
            print(countInStock)
            Product.objects.filter(pk = e).update(countInStock = countInStock)     
            print('pro',e,':',countInStock)          

        order = ShippingAddress.objects.filter(pk = pk)
        order_sum_count = OrderItem.objects.filter(user_id=request.user.id,order_id=fill_order.order_id).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
        context = {'select_address_get':select_address_get,'order_sum_count':order_sum_count,'orders':orders,'order':order,'fill_order':fill_order}
    if fill_user:
        Order.objects.filter(pk= order_id).update(isfinal=True,finalAt = timezone.now())
        orders = OrderItem.objects.filter(order_id = order_id)
        for_orderitem = OrderItem.objects.filter(order_id= order_id).values_list('order_id',flat=True)
        for i in for_orderitem:
            OrderItem.objects.filter(order_id= i).update(isfinal=True)

        order = ShippingAddress.objects.filter(pk = order_id)
        order_sum_count = OrderItem.objects.filter(user_id=request.user.id,order_id=fill_user.order_id).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
        context = {'select_address_get':select_address_get,'order_sum_count':order_sum_count,'orders':orders,'order':order,'fill_order':fill_user}
    return render(request, 'user/screen/shopping-order-details.html',context)

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ShoppingDetailsUserOrderAdminView(request,pk):
    if ShippingAddress.objects.filter(pk = pk,address = None):
        select_address = ShippingAddress.objects.get(pk = pk,address = None)
    else:
        select_address = 0
    if select_address:
        fill_order = ShippingAddress.objects.get(pk = select_address.selectaddress)
    else:
        fill_order = ShippingAddress.objects.get(pk = pk)
    checkt = request.POST.get('checkt')
    if checkt:
        try:
            cret = ShippingAddress.objects.get(pk = pk)
            Order.objects.filter(pk = cret.order_id).update(isPaid = checkt,paidAt = timezone.now())
            return redirect(reverse('order_list_user', args=[cret.store_id]))
        except:
            messages.error(request,'یکی از گزینه های تسویه را انتخاب کنید و بعد دکمه ثبت را بزنید.')
    orders = OrderItem.objects.filter(order_id = fill_order.order_id)
    order = ShippingAddress.objects.filter(pk = pk)
    order_sum_count = OrderItem.objects.filter(user_id=request.user.id,order_id=fill_order.order_id).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
    context = {'order_sum_count':order_sum_count,'orders':orders,'order':order,'fill_order':fill_order}
    return render(request, 'screen/shopping-order-details-user-admin.html',context)

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def ShoppingDetailsUserOrderUserView(request,pk):
    if ShippingAddress.objects.filter(pk = pk,address = None):
        select_address = ShippingAddress.objects.get(pk = pk,address = None)
    else:
        select_address = 0
    if select_address:
        fill_order = ShippingAddress.objects.get(pk = select_address.selectaddress)
    else:
        fill_order = ShippingAddress.objects.get(pk = pk,user_id = request.user.id)
    checkt = request.POST.get('checkt')
    if checkt:
        try:
            cret = ShippingAddress.objects.get(pk = pk)
            Order.objects.filter(pk = cret.order_id).update(isDelivered = checkt,deliveredAt = timezone.now())
            return redirect(reverse('order_list_user_me', args=[cret.store_id]))
        except:
            messages.error(request,'یکی از گزینه های تسویه را انتخاب کنید و بعد دکمه ثبت را بزنید.')
    orders = OrderItem.objects.filter(order_id = fill_order.order_id,user_id = request.user.id)
    order = ShippingAddress.objects.filter(pk = pk,user_id = request.user.id)
    try:
        fill = ShippingAddress.objects.get(pk = pk)
        order_get = Order.objects.get(pk = fill.order_id)
    except:
        order_get = 0
    order_sum_count = OrderItem.objects.filter(user_id=request.user.id,order_id=fill_order.order_id).aggregate(total_amount=Sum(F('price') * F('countInOrder')))
    context = {'order_get':order_get,'order_sum_count':order_sum_count,'orders':orders,'order':order,'fill_order':fill_order}
    return render(request, 'user/screen/shopping-order-details-user.html',context)

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def OrderListUserView(request,pk):
    order = ShippingAddress.objects.filter(store_id = pk)
    orders = OrderItem.objects.filter(store_id = pk,isfinal=True)
    context = {'orders':orders,'order':order}
    return render(request, 'screen/OrderListUserScreen.html',context)

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def OrderListUserMeView(request,pk):
    orders = OrderItem.objects.filter(store_id = pk,isfinal=True,user_id = request.user.id)
    order = ShippingAddress.objects.filter(store_id = pk,user_id = request.user.id)
    context = {'orders':orders,'order':order}
    return render(request, 'screen/OrderListUserMeScreen.html',context)

@never_cache
@login_required(login_url='/accounts/LoginAdmin/')
def AdminDashboard(request):
    return render(request, 'admin/dashboard.html')
    
@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def TemplateCreateView(request):
    form = TemplateForm
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('template_list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('template_create'))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'admin/TemplateCreateScreen.html',{'form':form})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def TemplateListView(request):
    template = Templates.objects.all()
    return render(request, 'admin/TemplateListScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def TemplateCardView(request):
    template = Templates.objects.all()
    return render(request, 'screen/TemplateCardScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def TemplateDetailsView(request,pk):
    template = Templates.objects.get(pk=pk)
    template_pk = request.POST.get('template')
    if template_pk:
        Store.objects.filter(pk = request.user.store_id).update(templates_id = template_pk)
        return redirect(reverse('template_card'))
    return render(request, 'screen/TemplateDetailsScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ReviewListView(request):
    review_list = Review.objects.filter(store_id=request.user.store_id)
    return render(request, 'screen/ReviewListScreen.html',{'review_list':review_list})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ReviewDeleteView(request,pk):
    review_delete = Review.objects.filter(pk=pk).delete()
    if review_delete:
        return redirect(reverse('review_list'))
    return render(request, 'screen/ReviewListScreen.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def UserListView(request):
    user_list = UserStore.objects.filter(store_id=request.user.store_id,is_user_store = 1)
    return render(request, 'screen/UserListScreen.html',{'user_list':user_list})

@never_cache
@csrf_exempt
def ProductCategoryStoreView(request,pk,store_id,slug):
    list_product_category = Product.objects.filter(category_id = pk,confirmed = 1)
    fill_product_category = Product.objects.filter(category_id = pk,confirmed = 1).last()
    if fill_product_category:
        store = Store.objects.get(pk = fill_product_category.store_id)
    else:
        return redirect(reverse('product-list-store', args=[store_id]))
    return render(request, 'user/screen/card-category.html',{'list_product_category':list_product_category,'store':store})

@never_cache
@csrf_exempt
def ProductSubCategoryStoreView(request,pk,store_id,slug):
    list_product_category = Product.objects.filter(subcategory_id = pk,confirmed = 1)
    fill_product_category = Product.objects.filter(subcategory_id = pk,confirmed = 1).last()
    if fill_product_category:
        store = Store.objects.get(pk = fill_product_category.store_id)
    else:
        return redirect(reverse('product-list-store', args=[store_id]))
    return render(request, 'user/screen/card-category.html',{'list_product_category':list_product_category,'store':store})

@never_cache
@csrf_exempt
def ProductSubsCategoryStoreView(request,pk,store_id,slug):
    list_product_category = Product.objects.filter(subscategory_id = pk,confirmed = 1)
    fill_product_category = Product.objects.filter(subscategory_id = pk,confirmed = 1).last()
    if fill_product_category:
        store = Store.objects.get(pk = fill_product_category.store_id)
    else:
        return redirect(reverse('product-list-store', args=[store_id]))
    return render(request, 'user/screen/card-category.html',{'list_product_category':list_product_category,'store':store})

@never_cache
@login_required(login_url='/accounts/LoginAdmin/')
def ConfirmedStoreView(request):
    store_list = Store.objects.filter(confirmed = 0)
    return render(request, 'admin/StoreListScreen.html',{'store_list':store_list})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdmin/')
def ConfirmedEditStoreView(request,pk):
    store = Store.objects.get(pk = pk)
    checkt = request.POST.get('checkt')
    if checkt:
        try:
            Store.objects.filter(pk = pk).update(confirmed = 1)
            return redirect(reverse('confirmed_store_list'))
        except:
            messages.error(request,'دکمه تایید را بزنید.')
    return render(request, 'admin/StoreDetailsEditScreen.html',{'store':store})

@never_cache
@login_required(login_url='/accounts/LoginAdmin/')
def ConfirmedProductView(request):
    product_list = Product.objects.filter(confirmed = 0)
    return render(request, 'admin/ProductListScreen.html',{'product_list':product_list})

@never_cache
@login_required(login_url='/accounts/LoginAdmin/')
def ConfirmedEditProductView(request,pk):
    products = Product.objects.get(pk = pk)
    checkt = request.POST.get('checkt')
    if checkt:
        try:
            Product.objects.filter(pk = pk).update(confirmed = 1)
            return redirect(reverse('confirmed_product_list'))
        except:
            messages.error(request,'دکمه تایید را بزنید.')
    return render(request, 'admin/ProductDetailsEditScreen.html',{'products':products})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ContactUsCreateView(request,pk):
    contactus = ContactUs.objects.filter(store_id = pk)
    if contactus:
        return redirect(reverse('contactus_edit', args=[pk]))
    else:
        form = ContactUsForm
        if request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('dashboard'))
            else:
                messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/ContactUsCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ContactUsEditView(request, pk): 
    store = Store.objects.get(pk = pk)
    context ={'store':store} 
    obj = get_object_or_404(ContactUs, store_id = pk) 
    form = ContactUsForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('dashboard'))
    context["form"] = form 
    return render(request, "screen/ContactUsEditScreen.html", context) 

@never_cache
def ContactUsView(request,pk):
    contactus_fil = ContactUs.objects.filter(store_id = pk)
    if contactus_fil:
        contactus = ContactUs.objects.get(store_id = pk)
        store = Store.objects.get(pk = pk)
    else:
        return redirect(reverse('product-list-store', args=[pk]))
    return render(request, 'user/screen/ContactUsScreen.html',{'contactus':contactus,'store':store})

@never_cache
@csrf_exempt
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageCreateView(request,pk):
    form = ImageForm
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('image_list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('image_create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/ImageCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageListView(request):
    images = ImageBlog.objects.filter(user_id = request.user.id).order_by('-id')
    return render(request, 'screen/ImageListScreen.html',{'images':images})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageDeleteView(request,pk):
    delete = ImageBlog.objects.filter(pk=pk).delete()
    if delete:
        return redirect(reverse('image_list'))
    return render(request, 'screen/ImageListScreen.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageEditView(request, pk): 
    image = ImageBlog.objects.get(pk = pk)
    context ={'image':image} 
    form = ImageForm
    obj = get_object_or_404(ImageBlog, pk = pk) 
    form = ImageForm(request.POST or None,request.FILES or None, instance = obj)     
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('image_list'))
    context["form"] = form 
    return render(request, "screen/ImageEditScreen.html", context) 