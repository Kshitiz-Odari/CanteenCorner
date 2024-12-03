from django.db.models import Count, Avg
from .models import ReviewRating, Items

def user_based_collaborative_filtering(target_user):
    target_user_ratings = ReviewRating.objects.filter(user=target_user)

    # Return an empoty list if the user has no ratings
    if not target_user_ratings.exists():
        return []

    # Find similar users who have rated at least one common item highly, and have at least 2 common high-rated items
    similar_users = (
        ReviewRating.objects
        .exclude(user=target_user)
        .filter(item__in=target_user_ratings.values('item'), rating__gte=3)
        .values('user')
        .annotate(common_items=Count('item'))
        .filter(common_items__gte=2)
        .order_by('-common_items')
    )

    similar_user_ids = [user['user'] for user in similar_users]

    # If no similar users are found, return empty
    if not similar_user_ids:
        return []

    # Get items rated by similar users with high ratings, excluding items already rated by the target user
    items_rated_by_similar_users = (
        Items.objects
        .filter(ratings__user__in=similar_user_ids, ratings__rating__gte=4)
        .exclude(ratings__user=target_user)
        .annotate(avg_rating=Avg('ratings__rating'))
        .order_by('-avg_rating')
        .distinct()
    )

    recommended_items = items_rated_by_similar_users[:10]


    print("Similar Users:", similar_user_ids)
    print("Recommended Items:", [item.name for item in recommended_items])

    return recommended_items
