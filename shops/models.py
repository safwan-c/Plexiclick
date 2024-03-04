from django.db import models
from django.contrib.auth.models import User
import datetime
import os

 
def getFileName(request,filename):
  now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename="%s%s"%(now_time,filename)
  return os.path.join('uploads/',new_filename)
 
class Catagory(models.Model):
  name=models.CharField(max_length=150,null=False,blank=False)
  image=models.ImageField(upload_to=getFileName,null=False,blank=False)
  description=models.TextField(max_length=500,null=True,blank=True)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  created_at=models.DateTimeField(auto_now_add=True)
 
  def __str__(self) :
    return self.name
  

class Size(models.Model):
    name = models.CharField(max_length=50)
  
    def __str__(self) :
      return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) :
      return self.name

    

class Thickness(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) :
      return self.name

class Product(models.Model):
  category=models.ForeignKey(Catagory,on_delete=models.CASCADE)
  name=models.CharField(max_length=150,null=False,blank=False)
  product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  description=models.TextField(max_length=500,null=True,blank=True)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
  created_at=models.DateTimeField(auto_now_add=True)
  
  def __str__(self) :
    return self.name
  
class ProductVariant(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  product_image=models.ImageField(upload_to=getFileName,null=False,blank=False)
  size = models.ForeignKey(Size, on_delete=models.CASCADE)
  color = models.ForeignKey(Color, on_delete=models.CASCADE)
  thickness = models.ForeignKey(Thickness, on_delete=models.CASCADE)
  quantity=models.IntegerField(null=False,blank=False)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  
class PlexCart(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)

  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at=models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return f'{self.user.username} - {self.product.name}'
      
  @property
  def total_cost(self):
    return self.product_qty*self.price
    

class Fav(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at=models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return f'{self.user.username} - {self.product.name}'
 
   
class Plexiorder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state= models.CharField(max_length=111)
    zipcode=models.CharField(max_length=111)
    phone=models.CharField(max_length=111, default="")
    notes=models.CharField(max_length=200)
    total_price=models.FloatField(null=False)
    orderstatus=(
                ('Pending','Pending'),
                ('Out For Shipping','Out For Shipping'),
                ('Completed','Completed'),
                )
    status=models.CharField(max_length=150,choices=orderstatus, default='pending')
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
      
class OrderItem(models.Model):
    order= models.ForeignKey(Plexiorder, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)




