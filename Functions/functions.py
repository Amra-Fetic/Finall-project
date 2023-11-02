
""" is top actor """

def is_top_actor(actor_list, top_actors_list):
    """
    Check if any actor in the given list is among the top actors.

    Parameters:
    - actor_list (list): A list of actors to check.
    - top_actors_list (list): A list of top actors.

    Returns:
    - str: 'yes' if any actor in actor_list is among the top actors, 'no' otherwise.
    """
    for actor in actor_list:
        if actor in top_actors_list:
            return 'yes'
    return 'no'

""" is top director """

    def is_top_director(director_list, top_director_list):
    """
    Check if any director in the given list is among the top directors.

    Parameters:
    - director_list (list): A list of directors to check.
    - top_directors_list (list): A list of top directors.

    Returns:
    - str: 'yes' if any director in director_list is among the top directors, 'no' otherwise.
    """
    for director in director_list:
        if director in top_director_list:
            return 'yes'
    return 'no'



"""Finding the closest match"""


    def find_closest_match(query, options):
    """
    Find the closest match to a given query in a list of options.

    Parameters:
    - query (str): The query string to find a close match for.
    - options (list): A list of strings representing the available options.

    Returns:
    - str or None: The closest match to the query, or None if no close match is found.
    """
    close_matches = get_close_matches(query, options, n=1, cutoff=0.8)
    if close_matches:
        return close_matches[0]
    else:
        return None


""" MOVIE RECOMENDER """

def movie_recommender():
    """
    Recommends similar movies based on user input of a recently watched movie and its director.

    This function prompts the user for the title of a recently watched movie and its director.
    It then finds the closest matches for the provided input in the dataset of movies.
    If a match is found, the function uses TF-IDF vectorization and cosine similarity to recommend
    the top 5 similar movies with matching genres.

    Returns:
    - None
    """
    movie_title = input("What movie did you like watching recently the most: ")
    movie_director = input("From which director? ")

    # Check for closest matches in movie titles and directors
    closest_movie_title = find_closest_match(movie_title, data_cleaned['Movie Name'])
    closest_director = find_closest_match(movie_director, data_cleaned['Director'])

    print("Closest match for movie title:", closest_movie_title)
    print("Closest match for director:", closest_director)

    if closest_movie_title is not None and closest_director is not None:
        # Get the index of the movie in the dataset
        movie_index = data_cleaned[(data_cleaned['Movie Name'] == closest_movie_title) & (data_cleaned['Director'] == closest_director)].index
        if not movie_index.empty:
            movie_index = movie_index[0]
        else:
            movie_index = None

        print("Index in the dataset:", movie_index)

        if movie_index is not None:
            # Extract the genre of the input movie
            input_genre = data_cleaned.loc[movie_index, 'Genre']

            # Create a TF-IDF vectorizer to convert movie descriptions to numerical vectors
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(data_cleaned['Description'].fillna(''))

            # Compute the cosine similarity between movies based on descriptions
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            # Get the pairwise similarity scores with other movies
            sim_scores = list(enumerate(cosine_sim[movie_index]))

            # Sort the movies based on similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the top 5 similar movies with matching genres
            top_movies_indices = [i[0] for i in sim_scores[1:6]]
            similar_genre_movies = data_cleaned.iloc[top_movies_indices]

            # Filter movies by matching genre
            similar_genre_movies = similar_genre_movies[similar_genre_movies['Genre'].apply(lambda x: any(genre in input_genre for genre in x))]

            print("You liked", closest_movie_title, "from", closest_director)
            print("You may also enjoy these similar movies:")
            display(similar_genre_movies[['Movie Name', 'Description', 'Genre']])
        else:
            print("Movie not found in the dataset.")
    else:
        print("Movie not found in the dataset.")