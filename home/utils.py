from django.db.models import Count
from .models import ReviewRating, Items

def user_based_collaborative_filtering(target_user):
    target_user_ratings = ReviewRating.objects.filter(user=target_user)

    if not target_user_ratings.exists():
        return []

    similar_users = ReviewRating.objects.exclude(user=target_user).filter(
    item__in=target_user_ratings.values('item'),
    rating__gte=3
).values('user').annotate(common_items=Count('item')).order_by('-common_items')


    print("Similar Users:", similar_users)

    items_rated_by_similar_users = Items.objects.filter(
        ratings__user__in=similar_users.values('user')
    ).exclude(ratings__user=target_user).distinct()

    print("Items rated by similar users:", items_rated_by_similar_users)

    recommended_items = items_rated_by_similar_users.exclude(
        ratings__user=target_user
    ).distinct()

    print("Recommended Items:", recommended_items)

    return recommended_items
