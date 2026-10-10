from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Age must be at least 1."),
            MaxValueValidator(120, message="Age must be 120 or less."),
        ]
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
