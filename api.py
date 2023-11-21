from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.config import Settings

app = Flask(__name__)
CORS(app)

client = chromadb.Client(
    Settings(chroma_db_impl="duckdb+parquet", persist_directory="db/"))
moviesCollection = client.get_or_create_collection(
    name="Movies")


@app.route('/recommend_movies', methods=['POST'])
def recommend_movies():
    data = request.get_json()

    if 'query' not in data:
        return jsonify({'error': 'Missing "query" parameter'}), 400

    query = data['query']

    result = moviesCollection.query(
        query_texts=[query],
        n_results=3
    )

    documents = [doc for sublist in result.get(
        'documents', []) for doc in sublist]

    return jsonify({'result': documents})


if __name__ == '__main__':
    app.run(debug=True)
