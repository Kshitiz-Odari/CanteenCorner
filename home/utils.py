from django.db.models import Count, Avg
from .models import ReviewRating, Items

def user_based_collaborative_filtering(target_user):
    # Get items rated by the target user
    target_user_ratings = ReviewRating.objects.filter(user=target_user)

    # returns empoty if no rate
    if not target_user_ratings.exists():
        return []

    # Find similar users who have rated at least one common item highly, needs at least 2 high rated dishes common for recommendation
    similar_users = (
        ReviewRating.objects
        .exclude(user=target_user)
        .filter(item__in=target_user_ratings.values('item'), rating__gte=3)  # Filter by items rated by target user and high rating
        .values('user')
        .annotate(common_items=Count('item'))
        .filter(common_items__gte=2)  # Only include users with at least 2 common items rated
        .order_by('-common_items')
    )


    print("Similar Users:", similar_users)


    items_rated_by_similar_users = (
        Items.objects
        .filter(ratings__user__in=[user['user'] for user in similar_users])
        .exclude(ratings__user=target_user)
        .annotate(avg_rating=Avg('ratings__rating'))
        .order_by('-avg_rating')
        .distinct()
    )

    print("Items rated by similar users:", items_rated_by_similar_users)

    recommended_items = items_rated_by_similar_users[:10]  # Limit the recommendations to top 10, for example


    print("Recommended Items:", recommended_items)

    return recommended_items
