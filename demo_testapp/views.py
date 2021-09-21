from urllib.parse import quote_plus

from django.contrib.auth import authenticate, get_user_model, login
from .models import EasyCartUsersInfo, EasyCart, Category, Product, UsersProductsCartInfo, UsersProductsWishlistInfo
from django.contrib import messages
import requests
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup



#BASE_URL = 'https://chennai.craigslist.org/search/?query={}'


def home(request,optional_parameter=id):
    return render(request, 'home.html')

def allCategories(request,optional_parameter=id):
    messages.info(request,'Please Register/Signin to Continue shopping...')
    return render(request,"demo_testapp/categories.html")

def categories(request,optional_parameter=id):
    category = Category.objects.all()
    return render(request, "demo_testapp/userInfo.html",{'category':category})

def register(request):
    if(request.method == 'POST'):
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        userName = request.POST['userName']
        password = request.POST['password']
        email = request.POST['email']
        mobileNo = request.POST['mobileNo']
        city = request.POST['city']
        users = EasyCart.objects.create_user(firstName=firstName, lastName=lastName,userName=userName,password=password,email=email,mobileNo=mobileNo,city=city)
        users.save()
        messages.info(request, 'Your registration is successful! please login to shop on EasyCart')
        return render(request, 'demo_testapp/signin.html')
    else:
        return render(request, 'demo_testapp/register.html')


def authenticate(self, email=None, password=None):
    try:
        # Try to find a user matching your username
        user = EasyCart.objects.get(email=email)

        #  Check the password is the reverse of the username
        if check_password(password, user.password):
            # Yes? return the Django user object
            return user
        else:
            # No? return None - triggers default login failed
            return None
    except EasyCart.DoesNotExist:
        # No user was found, return None - triggers default login failed
        return None

# Required for your backend to work properly - unchanged in most scenarios
def get_user(self, user_id):
    try:
        return EasyCart.objects.get(pk=user_id)
    except EasyCart.DoesNotExist:
        return None

def signin(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if (user is not None):
            login(request, user)
            #messages.info(request, 'Hi ' + user.firstName)
            category = Category.objects.all()
            print(category)
            return render(request, "demo_testapp/userInfo.html", {'user':user,'category':category})
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, "demo_testapp/signin.html")

def contactUs(request,optional_parameter=id):
    return render(request,"demo_testapp/contactUs.html")

def logout(request,optional_parameter=id):
    auth.logout(request)
    messages.info(request,"You have been succesfully logged out!")
    return render(request, "demo_testapp/signin.html" )

def productForm(request, id):
    if (request.method == 'GET'):
        product = Product.objects.get(id=id)
        return render(request,"demo_testapp/productform.html",{'product': product})
    else:
        return render(request, 'demo_testapp/new_search.html')



def addToCart(request,id):
    category = Category.objects.all()
    product = Product.objects.get(id=id)
    cartInfo = UsersProductsCartInfo.objects.create_cart(user=request.user,category=product.category.nameOfCategory,nameOfProduct=product.nameOfProduct,image=product.image,price=product.price,quantity=product.quantity)
    UsersProductsCartInfo.save(cartInfo)
    messages.info(request,"Selected item has been successfully added to your Cart!")
    return render(request,'demo_testapp/userInfo.html',{'category':category})

def cart(request,id):
    obj = UsersProductsCartInfo.objects.filter(user=request.user)
    return render(request,'demo_testapp/cart.html')

def cart(request,optional_parameter=id):
    userProducts = UsersProductsCartInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.filter(nameOfProduct=userProd.nameOfProduct)
        for x in products:
            productsList.append(x)
    return render(request,'demo_testapp/cart.html',{'productsList':productsList})


def removeFromCart(request,id):
    product = Product.objects.get(id=id)
    productInCart = UsersProductsCartInfo.objects.filter(nameOfProduct=product.nameOfProduct)
    for p in productInCart:
        if(p.user.id == request.user.id):
            UsersProductsCartInfo.delete(p)
            break
    messages.info(request, "Selected item has been successfully removed from your Cart!")
    #below code is same as in cart function, might change later
    userProducts = UsersProductsCartInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.get(nameOfProduct=userProd.nameOfProduct)
        productsList.append(products)
    return render(request, 'demo_testapp/cart.html', {'productsList': productsList})

def moveToCart(request,id):
    product = Product.objects.get(id=id)
    productInWishlist = UsersProductsWishlistInfo.objects.filter(nameOfProduct=product.nameOfProduct)
    for p in productInWishlist:
        if (p.user.id == request.user.id):
            UsersProductsWishlistInfo.delete(p)
            break
    cartInfo = UsersProductsCartInfo.objects.create_cart(user=request.user,
                                                                     category=product.category.nameOfCategory,
                                                                     nameOfProduct=product.nameOfProduct,
                                                                     image=product.image, price=product.price,
                                                                     quantity=product.quantity)
    UsersProductsCartInfo.save(cartInfo)
    messages.info(request, "Selected item has been successfully moved to your Cart!")
    # below code is same as in cart function, might change later
    userProducts = UsersProductsWishlistInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.filter(nameOfProduct=userProd.nameOfProduct)
        for x in products:
            productsList.append(x)
    return render(request, 'demo_testapp/wishlist.html', {'productsList': productsList})

def addToWishlist(request,id):
    category = Category.objects.all()
    product = Product.objects.get(id=id)
    wishlistInfo = UsersProductsWishlistInfo.objects.create_wishlist(user=request.user,category=product.category.nameOfCategory,nameOfProduct=product.nameOfProduct,image=product.image,price=product.price,quantity=product.quantity)
    UsersProductsWishlistInfo.save(wishlistInfo)
    messages.info(request,"Selected item has been successfully added to your Wishlist!")
    return render(request,'demo_testapp/userInfo.html',{'category':category})

def wishlist(request,id):
    obj = UsersProductsWishlistInfo.objects.filter(user=request.user)
    return render(request,'demo_testapp/wishlist.html')

def wishlist(request,optional_parameter=id):
    userProducts = UsersProductsWishlistInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.filter(nameOfProduct=userProd.nameOfProduct)
        for x in products:
            productsList.append(x)
    return render(request,'demo_testapp/wishlist.html',{'productsList':productsList})

def moveToWishlist(request,id):
    product = Product.objects.get(id=id)
    productInCart = UsersProductsCartInfo.objects.filter(nameOfProduct=product.nameOfProduct)
    for p in productInCart:
        if (p.user.id == request.user.id):
            UsersProductsCartInfo.delete(p)
            break
    wishlistInfo = UsersProductsWishlistInfo.objects.create_wishlist(user=request.user,
                                                                     category=product.category.nameOfCategory,
                                                                     nameOfProduct=product.nameOfProduct,
                                                                     image=product.image, price=product.price,
                                                                     quantity=product.quantity)
    UsersProductsWishlistInfo.save(wishlistInfo)
    messages.info(request, "Selected item has been successfully moved to your Wishlist!")
    # below code is same as in cart function, might change later
    userProducts = UsersProductsCartInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.get(nameOfProduct=userProd.nameOfProduct)
        productsList.append(products)
    return render(request, 'demo_testapp/cart.html', {'productsList': productsList})

def removeFromWishlist(request,id):
    product = Product.objects.get(id=id)
    productInWishlist = UsersProductsWishlistInfo.objects.filter(nameOfProduct=product.nameOfProduct)
    for p in productInWishlist:
        if (p.user.id == request.user.id):
            UsersProductsWishlistInfo.delete(p)
            break
    messages.info(request, "Selected item has been successfully removed from your Wishlist!")
    # below code is same as in cart function, might change later
    userProducts = UsersProductsWishlistInfo.objects.filter(user=request.user)
    productsList = []
    for userProd in userProducts:
        products = Product.objects.get(nameOfProduct=userProd.nameOfProduct)
        productsList.append(products)
    return render(request, 'demo_testapp/wishlist.html', {'productsList': productsList})


def new_search(request,optional_parameter=id):

    if(request.method == 'POST'):
        searchCategory = request.POST['search']
        categoryinDB = Category.objects.get(nameOfCategory = searchCategory)
        categoryId = categoryinDB.id
        subCategory = Category.objects.filter(parent_id = categoryId)
        subCatProducts = []
        for sub in subCategory:
            print("subid", sub.id)
            #print(sub.parent_id)
        if subCategory:
            for sub in subCategory:
                product = Product.objects.filter(category= sub)
                subCatProducts.append(product)
            if (categoryinDB is not None) and (subCatProducts is not None):
                print(categoryinDB.id)
                print("list loop", subCatProducts)
                return render(request, 'demo_testapp/new_search.html', {'cat':categoryinDB,'subCategory':subCategory,'id':1,'subCatProducts': subCatProducts,'searchCategory':searchCategory})
        else:
            product = Product.objects.filter(category= categoryinDB)
            if (categoryinDB is not None) and (product is not None):
                print(categoryinDB.id)
                print("if loop", product)
                # print(product.nameOfProduct[0])
                return render(request, 'demo_testapp/new_search.html',{'cat': categoryinDB, 'searchCategory': searchCategory, 'product': product})

        # else:
        #     messages.info(request,"No such category found")
        #     return render(request, 'demo_testapp/userInfo.html')

    else:
        return render(request, 'demo_testapp/userInfo.html')


def payment(request,optional_parameter=id):
    return render(request, 'demo_testapp/payment.html')