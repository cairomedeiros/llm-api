from rest_framework import serializers

class OpenAIRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=500)