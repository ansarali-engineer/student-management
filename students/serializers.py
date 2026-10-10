from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "email", "age"]
        read_only_fields = ["id"]

    def validate_age(self, value):
        if value < 1:
            raise serializers.ValidationError("Age must be at least 1.")
        if value > 120:
            raise serializers.ValidationError("Age must be 120 or less.")
        return value
