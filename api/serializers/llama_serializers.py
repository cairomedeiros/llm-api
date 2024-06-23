from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()

class LlamaSerializer(serializers.Serializer):
    messages = serializers.ListField(child=MessageSerializer())