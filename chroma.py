
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from mongo import MongoSoftware

load_dotenv()


def initChroma():
    # api_key = os.getenv("API_KEY")
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory="db/"))
    # openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=api_key,
    #                                                         model_name="text-embedding-ada-002")
    # moviesCollection = client.get_or_create_collection(
    #     name="Movies", embedding_function=openai_ef)
    moviesCollection = client.get_or_create_collection(
        name="Movies")
    return moviesCollection


def createEmbeddings(mongo, moviesCollection):
    all_movies = mongo.movies.find({})

    titles = []
    genres = []
    ratings = []
    tags = []

    for movie in all_movies:
        genre_str = " ".join(movie.get('genres', []))
        tags_str = " ".join(movie.get('tags', []))

        titles.append(movie.get('title', ''))
        genres.append(genre_str)
        ratings.append(movie.get('rating', ''))
        tags.append(tags_str)

    movies_data = [f"{title} {genre} {rating} {tag}" for title,
                   genre, rating, tag in zip(titles, genres, ratings, tags)]

    metadata_list = [{"source": "mongo db"}] * len(movies_data)

    moviesCollection.add(
        documents=movies_data,
        metadatas=metadata_list,
        ids=[f"id{index}" for index in range(len(movies_data))])

    del mongo


if __name__ == "__main__":
    mongo = MongoSoftware()
    moviesCollection = initChroma()
    createEmbeddings(mongo, moviesCollection)
