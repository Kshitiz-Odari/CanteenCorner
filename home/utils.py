from .models import Items  # Import the Items model from your Django app
import sqlite3
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise import accuracy
import math


def round_up_to_three_decimal_places(num):
    return math.ceil(num * 1000) / 1000


def recommend_with_algorithm(target_user_id):

    connection = sqlite3.connect('E:/Restro&Bar/db.sqlite3')
    cursor = connection.cursor()


    cursor.execute("SELECT user_id, item_id, rating FROM home_reviewrating")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=['user_id', 'item_id', 'rating'])


    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

    trainset = data.build_full_trainset()
    algo = SVD()

    algo.fit(trainset)

    predictions = algo.test(trainset.build_testset())
    rmse = accuracy.rmse(predictions)
    print(f"RMSE on the training set: {rmse}")

    user_rated_items = df[df['user_id'] == target_user_id]['item_id'].unique()
    recommendations = []

    items = Items.objects.all()


    for item in items:
        item_id = item.id
        item_name = item.name
        item_image = item.image.url if item.image else '{% static "default_image.png" %}'

        if item_id not in user_rated_items:
            predicted_rating = algo.predict(target_user_id, item_id).est
            rounded_rating = round_up_to_three_decimal_places(predicted_rating)
            recommendations.append({
                'name': item_name,
                'image': item_image,
                'price': item.price,
                'predicted_rating': rounded_rating,
            })

    recommendations.sort(key=lambda x: x['predicted_rating'], reverse=True)


    connection.close()

    return recommendations[:8]
