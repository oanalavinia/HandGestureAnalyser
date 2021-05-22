from scripts import queries as qrs
from scripts.recommendation import recommendation as rec


class Movie(object):
    def __init__(self, gestures_handler):
        self.gestures_handler = gestures_handler
        self.queries_handler = qrs.Queries(self.gestures_handler)
        self.gesture = None
        self.selected_movie_id = None

    def get_gesture(self, gesture):
        if gesture == 'one':
            self.gesture = 1
        elif gesture == 'two':
            self.gesture = 2
        elif gesture == 'three':
            self.gesture = 3
        elif gesture == 'four':
            self.gesture = 4
        elif gesture == 'five':
            self.gesture = 5

    def get_selected_movie_id(self, movie_ids):
        if self.gesture is not None and 1 <= self.gesture <= 5:
            return int(movie_ids[self.gesture - 1])

        return None

    def get_recommendations(self, str_gesture, movie_ids):
        self.reset_object()
        self.get_gesture(str_gesture)
        movie_id = self.get_selected_movie_id(movie_ids)
        movie_name = rec.get_movie_name_by_movie_id(movie_id)

        rec_movies = []
        if isinstance(movie_id, int):
            rec_ids = rec.get_recommendation_ids_on_id(movie_id)
            for id in rec_ids:
                rec_movies.append(rec.get_movie_name_by_database_id(id[0]))

        return rec_movies, movie_name

    def get_rec_system(self):
        return rec

    def reset_object(self):
        self.gesture = None
        self.selected_movie_id = None
