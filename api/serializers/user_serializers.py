from rest_framework import serializers
from bson import ObjectId

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId")

class UserSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    user_name = serializers.CharField(max_length=25)