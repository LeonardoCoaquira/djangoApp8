from rest_framework import serializers, viewsets
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'pub_date']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()

    class Meta:
        model = Producto
        fields = ['id', 'categoria', 'nombre', 'precio', 'stock', 'pub_date']

    def create(self, validated_data):
        categoria_data = validated_data.pop('categoria')
        categoria_serializer = CategoriaSerializer(data=categoria_data)
        if categoria_serializer.is_valid():
            categoria = categoria_serializer.save()
            producto = Producto.objects.create(categoria=categoria, **validated_data)
            return producto
        else:
            raise serializers.ValidationError(categoria_serializer.errors)