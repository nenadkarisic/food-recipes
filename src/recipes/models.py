from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class User(TimeStampedModel):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    username = models.CharField(max_length=30, null=False)
    email = models.EmailField(null=False)


class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=30, null=False)


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    recipe = models.TextField(null=False)
    ingredients = models.ManyToManyField(Ingredient)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # TODO: Add logic for returning average star rating


class Rating(TimeStampedModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    # You might also want to add a timestamp for when the rating was given

    class Meta:
        unique_together = [['user', 'recipe']]
        # This ensures a user can only rate a recipe once


# TODO: WHat is the default built-in ID format for these models, is it INT od UUID?
# https://stackoverflow.com/questions/18064973/id-field-in-model-django


