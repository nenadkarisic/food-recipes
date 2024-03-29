from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


# Create your models here.
class User(AbstractUser):
    username = models.CharField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    recipe = models.TextField(null=False)
    ingredients = models.ManyToManyField(Ingredient)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)


class Rating(TimeStampedModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars')
        ]
    )

    def __str__(self):
        return "{} - {} - {}".format(self.recipe, self.user, self.stars)

    class Meta:
        unique_together = [['user', 'recipe']]
        # This ensures a user can only rate a recipe once
