from atexit import register
from django.contrib import admin
from .models import *
 
 

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id','name', 'image', 'description')

class ProductAdmin(admin.ModelAdmin):
  list_display = ('id','name')
  def id(self, obj):
        return obj.id 

class SizeAdmin(admin.ModelAdmin):
     list_display = ['id','name']

class ThicknessAdmin(admin.ModelAdmin):
     list_display = ['id','name']

class ColorAdmin(admin.ModelAdmin):
     list_display = ['id','name']

class ProductVariantsAdmin(admin.ModelAdmin):
    #  list_display = ['id','product','quantity','price']
     list_display = ['id','product_id','product_image','color_id','size_id','thickness_id','quantity','price']
     
     def product_id(self, obj):
        return obj.product.id 
     def size_id(self, obj):
        return obj.size.id 
     def color_id(self, obj):
        return obj.color.id
     def thickness_id(self, obj):
        return obj.thickness.id
     

class CartAdmin(admin.ModelAdmin):
  list_display = ('id','product','price','product_qty','created_at')
  def product_id(self, obj):
    return obj.product.id 
  def size_id(self, obj):
    return obj.size.id 
  def color_id(self, obj):
    return obj.color.id
  def thickness_id(self, obj):
    return obj.thickness.id
    
class FavAdmin(admin.ModelAdmin):
  list_display = ('id','product')
  
class OrderAdmin(admin.ModelAdmin):
  list_display= ['id','first_name']
  
  
class OrderItemAdmin(admin.ModelAdmin):
  list_display= ['id']
  
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Plexiorder,OrderAdmin)
admin.site.register(Catagory,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(PlexCart,CartAdmin)
admin.site.register(Fav,FavAdmin)
admin.site.register(ProductVariant,ProductVariantsAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Thickness,ThicknessAdmin)











