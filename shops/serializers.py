from rest_framework import serializers  
from .models import ProductVariant,PlexCart,Fav
  
class VariantPriceSerializer(serializers.ModelSerializer):
    class Meta:  
        model = ProductVariant 
        fields = ('__all__')  
        
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlexCart
        fields = ('__all__')
        
        
class FavItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fav
        fields = ('__all__')