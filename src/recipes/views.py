from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q, Avg
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .models import User, Recipe, Ingredient, Rating
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    RecipeSerializer,
    RatingSerializer,
    IngredientSerializer
)
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def index(request):
    return HttpResponse("Hello, dear people. You're at the RECIPES index page."
                        "Please refer to the README file in the project to learn about available "
                        "endpoints and how to use them.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        custom_permission_classes = []
        if self.action == 'create':
            custom_permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            custom_permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            custom_permission_classes = [IsAdminUser]
        return [permission() for permission in custom_permission_classes]


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Recipe Creation
class CreateRecipeAPIView(generics.CreateAPIView):
    permission_classes = (IsLoggedInUserOrAdmin,)
    serializer_class = RecipeSerializer


# Recipe Rating (you cannot rate your own recipes).
class CreateRatingAPIView(generics.CreateAPIView):
    permission_classes = (IsLoggedInUserOrAdmin,)
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
View for listing recipes, implementing multiple options:
- Listing all recipes;
- List user's own recipes;
- Filter recipes with minimum and maximum number of ingredients;
- Search recipes by fields containing provided search string: name, text, ingredients;
- Every listed recipe also contains an average rating;
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recipes(request):
    # Extract query parameters.
    list_own = bool(request.GET.get('list_own', 'False')) is True
    ingredients_min = int(request.GET.get('ingredients_min', '0'))
    ingredients_max = int(request.GET.get('ingredients_max', '1000'))  # Use a large number as the default max.
    search = request.GET.get('search', '')

    # Start with all recipes or only those belonging to the user.
    if list_own:
        recipes = Recipe.objects.filter(user_id=request.user.id)
    else:
        recipes = Recipe.objects.all()

    # Filter by the number of ingredients.
    recipes = recipes.annotate(ingredient_count=Count('ingredients')).filter(
        ingredient_count__gte=ingredients_min,
        ingredient_count__lte=ingredients_max
    )

    # Apply search filter if 'search' string is provided.
    if search:
        search_query = (
                Q(name__icontains=search) |
                Q(recipe__icontains=search) |
                Q(ingredients__name__icontains=search)
        )
        recipes = recipes.filter(search_query).distinct()

    # Calculate average ratings for the filtered recipes, and map those values to a recipe id.
    ratings = Rating.objects.filter(recipe__in=recipes).values('recipe_id').annotate(average_rating=Avg('stars'))
    ratings_dict = {rating['recipe_id']: rating['average_rating'] for rating in ratings}

    # Serialize and return the queryset.
    serializer = RecipeSerializer(recipes, many=True)
    serialized_data = serializer.data
    # Manually add the 'average_rating' field to each serialized recipe.
    for recipe_data in serialized_data:
        recipe_data['average_rating'] = ratings_dict.get(recipe_data["id"], None)
    return JsonResponse(data=serialized_data, safe=False)


# Get the most used ingredients (top 5).
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_used_ingredients(request):
    # Query the top 5 ingredients with their recipe counts.
    top_ingredients = Ingredient.objects.annotate(num_recipes=Count('recipe')).order_by('-num_recipes')[:5]
    # Serialize the queryset.
    serializer = IngredientSerializer(top_ingredients, many=True)
    serialized_data = serializer.data
    # Manually add the 'num_recipes' field to the serialized data.
    for ingredient_data, ingredient in zip(serialized_data, top_ingredients):
        ingredient_data['num_recipes'] = ingredient.num_recipes
    return JsonResponse(data=serialized_data, safe=False)
