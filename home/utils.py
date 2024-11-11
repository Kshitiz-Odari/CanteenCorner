from django.db.models import Count, Avg
from .models import ReviewRating, Items

def user_based_collaborative_filtering(target_user):
    # Get items rated by the target user
    target_user_ratings = ReviewRating.objects.filter(user=target_user)

    # If the target user hasn't rated any items, return an empty list
    if not target_user_ratings.exists():
        return []

    # Find similar users who have rated at least one common item highly (>= 3)
    similar_users = (
        ReviewRating.objects
        .exclude(user=target_user)  # Exclude the target user
        .filter(item__in=target_user_ratings.values('item'), rating__gte=3)  # Filter by items rated by target user and high rating
        .values('user')
        .annotate(common_items=Count('item'))
        .filter(common_items__gte=2)  # Only include users with at least 2 common items rated
        .order_by('-common_items')  # Order by the number of common items rated
    )

    # Check for similar users found
    print("Similar Users:", similar_users)

    # Get items rated by similar users but not by the target user
    items_rated_by_similar_users = (
        Items.objects
        .filter(ratings__user__in=[user['user'] for user in similar_users])  # Items rated by similar users
        .exclude(ratings__user=target_user)  # Exclude items rated by target user
        .annotate(avg_rating=Avg('ratings__rating'))  # Annotate with average rating from similar users
        .order_by('-avg_rating')  # Sort by highest average rating
        .distinct()
    )

    # Check items rated by similar users
    print("Items rated by similar users:", items_rated_by_similar_users)

    # Return the recommended items
    recommended_items = items_rated_by_similar_users[:10]  # Limit the recommendations to top 10, for example

    # Check final recommended items
    print("Recommended Items:", recommended_items)

    return recommended_items
