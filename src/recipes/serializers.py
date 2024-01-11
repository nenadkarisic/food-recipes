from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Ingredient, Recipe, Rating


# Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2',
                  'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

    def create(self, validated_data):
        ingredient = Ingredient.objects.create(**validated_data)
        ingredient.save()
        return ingredient


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    recipe = serializers.CharField(required=True)
    ingredients = serializers.ListField(required=True, write_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'recipe', 'ingredients', 'user']
        extra_kwargs = {'user': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientSerializer(instance.ingredients.all(), many=True).data
        return representation

    def validate(self, attrs):
        user = self.context['request'].user
        if Recipe.objects.filter(name=attrs['name'], user=user).exists():
            raise serializers.ValidationError("You have already created a recipe with this name.")
        return attrs

    def create(self, validated_data):
        ingredient_name_list = validated_data.pop('ingredients')
        ingredient_obj_list = []
        try:
            for ingredient_name in ingredient_name_list:
                # Check if named ingredient already exists in the database.
                ingredient_obj = Ingredient.objects.filter(name__exact=ingredient_name).first()
                # If not, we create, save it, and add it to the ingredients list.
                if not ingredient_obj:
                    new_ingredient = Ingredient.objects.create(name=ingredient_name)
                    new_ingredient.save()
                    ingredient_obj_list.append(new_ingredient)
                else:
                    ingredient_obj_list.append(ingredient_obj)
        except Exception as ex:
            raise ex
        recipe = Recipe.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        recipe.ingredients.set(ingredient_obj_list)
        recipe.save()
        return recipe


class RatingSerializer(serializers.ModelSerializer):
    recipe = serializers.IntegerField(required=True, write_only=True)
    stars = serializers.ChoiceField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars')
        ]
    )

    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'stars']
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, attrs):
        recipe_obj = Recipe.objects.filter(id=attrs['recipe']).first()
        if not recipe_obj:
            raise serializers.ValidationError("Recipe with provided ID wasn't found.")
        if self.context['request'].user.id == recipe_obj.user.id:
            raise serializers.ValidationError("You are not allowed to rate your own recipe.")
        user = self.context['request'].user
        if Rating.objects.filter(recipe=attrs['recipe'], user=user).exists():
            raise serializers.ValidationError("You have already rated this recipe.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        rating = Rating.objects.create(
            user=user,
            recipe_id=validated_data['recipe'],
            stars=validated_data['stars']
        )
        return rating
