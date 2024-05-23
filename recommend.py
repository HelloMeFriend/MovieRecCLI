import pandas as pd
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# https://files.grouplens.org/datasets/movielens/ml-25m.zip
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
def clean_title(title):
        return re.sub("[^a-zA-Z0-9 ]", "", title)

# Creating search engine method
def search(title):
    
    movies["clean_title"] = movies["title"].apply(clean_title)

    vectorizer = TfidfVectorizer(ngram_range=(1,2))

    tfidf = vectorizer.fit_transform(movies["clean_title"])

    title = clean_title(title)
    title_vector = vectorizer.transform([title])
    cosine_similarities = cosine_similarity(title_vector, tfidf).flatten()
    indices = np.argpartition(cosine_similarities, -5)[-5:] # Gives the 5 most similar titles to searched term
    results = movies.iloc[indices][::-1]
    return results

def recommendations(movieId):
    similar_users = ratings[(ratings["movieId"] == movieId) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["title"]]




