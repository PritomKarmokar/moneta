from rest_framework import serializers

class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

class UpdateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)