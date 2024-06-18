from rest_framework import serializers
 
 
class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=25)