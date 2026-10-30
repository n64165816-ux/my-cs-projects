SELECT count(title) FROM movies WHERE id IN (SELECT movie_id FROM ratings WHERE rating = 10.0);-- 4. Number of movies with a 10.0 rating
