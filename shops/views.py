from django.http import  JsonResponse
from django.shortcuts import redirect, render
from .forms import CustomUserForm, OrderForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Product

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from .serializers import  VariantPriceSerializer
from rest_framework.permissions import IsAuthenticated




def home(request):
  category=Catagory.objects.filter(status=0)
  products=Product.objects.filter(trending=1)
  return render(request,"shops/new/index.html",{"products":products,"category":category})
  
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shops/new/register.html",{'form':form})
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("home")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shops/new/login.html")
    
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"shops/new/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
    
def product_details(request,cname,pname,product_id):
        products=Product.objects.filter(name=pname,status=0).first()
        
        variants = ProductVariant.objects.filter(product_id=product_id)
        
        color_objects = Color.objects.filter(id__in=variants.values('color'))
        size_objects = Size.objects.filter(id__in=variants.values('size'))
        thickness_objects = Thickness.objects.filter(id__in=variants.values('thickness'))  

        return render(request,"shops/new/products/products_details.html",{
              'products':products,
              'color_names_list':color_objects,
              'size_names_list':size_objects,
              'thickness_names_list':thickness_objects,
              'variants':variants,   
        })  
    
    
def shop(request):
   catagory=Catagory.objects.filter(status=0)
   return render(request, "shops/new/shop.html",{"catagory":catagory})

def cont(request):
   return render(request, "shops/new/cont.html")


def about(request):
   return render(request, "shops/new/about.html")

class FavView(APIView):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product_id = request.data.get('product_id',None)
            product_qty = request.data.get('product_qty',None)
            color = request.data.get('color_id',None)
            size = request.data.get('size_id',None)
            thickness = request.data.get('thickness_id',None)
            price = request.data.get('price_id',None)
            
            product_status=Product.objects.get(id=product_id)
        
            variant = ProductVariant.objects.get(size=size, color=color, thickness=thickness)
          
            if product_status:
              if Fav.objects.filter(user=request.user.id,product_id=product_id,variant=variant):
                return JsonResponse({'status':'Product Already in Wish List'}, status=200) 
              else:
                if variant.quantity >= int(product_qty):
                        Fav.objects.create(user=request.user,product_id=product_id,product_qty=product_qty,variant=variant,price=price)
                        return JsonResponse({'status':'Product Added to Wish List'}, status=200) 
                else:
                        return JsonResponse({'status': 'error', 'message': 'Not enough quantity available'})
              
                    
        else:
            return JsonResponse({'status':'Login to wish List'}, status=200) 
          

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Fav.objects.filter(user=request.user)
    return render(request,"shops/new/fav.html",{"fav":fav})
  else:
    messages.info(request, 'Please login to view your Wishlist items.')
    return redirect("/")
 
def remove_fav(request,fid):
  item=Fav.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
  
 
def remove_cart(request,cid):
  cartitem=PlexCart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
  
def cart_page(request):
  
  if request.user.is_authenticated:
    cart=PlexCart.objects.filter(user=request.user)
    return render(request,"shops/new/cart.html",{"cart":cart})
  else:
    messages.info(request, 'Please login to view your Cart items.')
    return redirect("/")
    
class CartView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      product_id = request.data.get('product_id',None)
      product_qty = request.data.get('product_qty',None)
      color = request.data.get('color_id',None)
      size = request.data.get('size_id',None)
      thickness = request.data.get('thickness_id',None)
      price = request.data.get('price_id',None)
      
      product_status=Product.objects.get(id=product_id)
      
      variant = ProductVariant.objects.get(size=size, color=color, thickness=thickness)
      
      if product_status:
        if PlexCart.objects.filter(user=request.user.id,product_id=product_id,variant=variant):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
          
        else:   
            if variant.quantity >= int(product_qty):
              PlexCart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty,variant=variant,price=price)
              return JsonResponse({'status':'Product Added to Cart'}, status=200)
            else:
              return JsonResponse({'status': 'error', 'message': 'Not enough quantity available'})      
    else:
       return JsonResponse({'status':'Login to Add Cart'}, status=200)      
          
 
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

    
def checkout(request):
  if request.user.is_authenticated:
    cart=PlexCart.objects.filter(user=request.user)
    form=OrderForm()
    if request.method=='POST':
      form=OrderForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request,"Order placed successfully!")
        
    return render(request,"shops/new/checkout.html",{"cart":cart,"form":form})
  else:
    return redirect("/")
  


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = None
    return render(request, 'shops/new/search_results.html',{'results': results})

class VariantPriceView(APIView):
    
    def post(self, request, *args, **kwargs):
      product_id = request.data.get('product_id',None)
      color_id = request.data.get('color_id',None)
      size_id = request.data.get('size_id',None)
      thickness_id = request.data.get('thickness_id',None)
      
      filtered_variants = ProductVariant.objects.filter(product=product_id,color=color_id,size=size_id,thickness=thickness_id)
      serializer = VariantPriceSerializer(filtered_variants, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)


def order(request):
    user = request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    country = request.POST['country']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcod']
    phone = request.POST['phone']
    notes = request.POST['notes']
    
    cart = PlexCart.objects.filter(user=request.user).all()
    total_price = sum(item.total_cost for item in cart)
    
    ord_dt = Plexiorder.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        address=address,
        country=country,
        city=city,
        zipcode=zipcode,
        phone=phone,
        notes=notes,
        state=state,
        total_price=total_price,
    )
    
    for item in cart:
        product = item.product
        variant = item.variant
        p_qty = item.product_qty
        price = item.price
        
    OrderItem.objects.create(order=ord_dt, product=product, variant=variant, product_qty=p_qty, price=price) 
    PlexCart.objects.filter(user=request.user).delete()
    messages.success(request,"Your Order Placed Successfully...")     
    return redirect("/")
      
def my_order(request):
  if request.user.is_authenticated:
    orders= Plexiorder.objects.filter(user=request.user)
    return render(request,"shops/new/my_order.html",{'orders':orders})
  else:
    messages.info(request, 'Please login to view your orders.')
    return redirect("/")

     
def orderview(request, pid):
  orders= Plexiorder.objects.filter(id=pid, user=request.user)
  orderitems = OrderItem.objects.filter(order__in=orders.all())
  return render(request, "shops/new/order_view.html", {'orders': orders,'orderitems':orderitems})
  
    