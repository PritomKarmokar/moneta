from rest_framework import serializers

from expenses.models import Category

class CreateExpenseSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=50)
    amount = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=255)

    def validate_category(self, value):
        request = self.context["request"]
        user = request.user

        category = Category.objects.filter(
            name__iexact=value,
            user=user
        ).first()

        if not category:
            raise serializers.ValidationError(
                detail="This Category Type does not exist for this user",
                code="CDNE_404"
            )

        return category
