import pandas as pd
from mongo import MongoSoftware
from logger import Logger
import math

FILES_PATH = "./data"
CHUNK_SIZE = 1000


def add_movies(mongo, df_movies):
    to_insert = []

    for index, row in df_movies.iterrows():
        to_insert.append(
            {
                "id": row["movieId"],
                "title": row["title"],
                "genres": row["genres"].split("|"),
            }
        )

        if index % CHUNK_SIZE == 0:
            mongo.movies.insert_many(to_insert)
            to_insert = []
            Logger.ok(f"Inserted {index} rows")

    mongo.movies.insert_many(to_insert)
    Logger.ok("Inserted all rows")

    Logger.info("Done")


def add_ratings(mongo, df_ratings):
    ratings = df_ratings.groupby("movieId")["rating"].mean()

    for index, row in ratings.items():
        mongo.movies.update_one({"id": index}, {"$set": {"rating": row}})
        Logger.ok(f"Inserted {index} rows")


def add_tags(mongo, df_tags):
    tags = df_tags.groupby("movieId")["tag"].apply(set)

    for index, row in tags.items():
        mongo.movies.update_one({"id": index}, {"$set": {"tags": list(row)}})
        Logger.ok(f"Inserted {index} rows")


def build_df(df_movies, df_ratings, df_tags):
    df = df_movies.copy()

    ratings = df_ratings.groupby("movieId")["rating"].mean()
    df = df.join(ratings, on="movieId")

    tags = df_tags.groupby("movieId")["tag"].apply(set)
    df = df.join(tags, on="movieId")

    df.loc[df["tag"].isnull(), "tag"] = df.loc[df["tag"].isnull(), "tag"].apply(lambda x: set())

    return df


def add_full_movies(mongo, df):
    to_insert = []

    for index, row in df.iterrows():
        to_insert.append(
            {
                "id": row["movieId"],
                "title": row["title"],
                "genres": row["genres"].split("|"),
                "rating": row["rating"],
                "tags": list(row["tag"]),
            }
        )

        if index % CHUNK_SIZE == 0:
            mongo.movies.insert_many(to_insert)
            to_insert = []
            Logger.ok(f"Inserted {index} rows")

    mongo.movies.insert_many(to_insert)
    Logger.ok("Inserted all rows")

    Logger.info("Done")


def build_index(mongo):
    mongo.movies.create_index([("id", 1)])
    mongo.movies.create_index([("title", "text")])


if __name__ == "__main__":
    mongo = MongoSoftware()
    build_index(mongo)

    # movieId, title, genres
    df_movies = pd.read_csv(f"{FILES_PATH}/movies.csv")
    # add_movies(mongo, df_movies)

    # userId, movieId, rating, timestamp
    df_ratings = pd.read_csv(f"{FILES_PATH}/ratings.csv")
    # add_ratings(mongo, df_ratings)

    # userId, movieId, tag, timestamp
    df_tags = pd.read_csv(f"{FILES_PATH}/tags.csv")
    # add_tags(mongo, df_tags)

    df = build_df(df_movies, df_ratings, df_tags)
    add_full_movies(mongo, df)

    del mongo
