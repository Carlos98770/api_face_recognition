from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('dados','name', 'image','id')
        read_only_fields = ('dados',)

class ImageBase64Serializer(serializers.Serializer):
    image = serializers.CharField(write_only=True)  # String base64 codificada da imagem