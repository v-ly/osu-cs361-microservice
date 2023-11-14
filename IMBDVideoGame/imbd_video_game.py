import pandas as pd
import random
import json


class IMBDVideoGame:

    def __init__(self):
        self._dataset = pd.read_csv('./imbd_videogame_reviews.csv')
        self._scrub_dataset()
        self._dataset_results = self._dataset

    def _scrub_dataset(self):
        self._dataset.loc[self._dataset.genres == "\\N", 'genres'] = "Not Specified"
        self._dataset.loc[~self._dataset.startYear.str.isnumeric(), 'startYear'] = 0
        self._dataset['startYear'] = self._dataset.startYear.astype(int)

    def _constraint_genres(self, genres: str):
        self._dataset_results = self._dataset_results[self._dataset_results.genres.str.contains(genres)]

    def _constraint_start_year(self, start_range: int, end_range: int):
        self._dataset_results = self._dataset_results[
            (self._dataset_results.startYear >= start_range) & (self._dataset_results.startYear <= end_range)]

    def _constraint_average_rating(self, average_rating: int):
        self._dataset_results = self._dataset_results[(self._dataset_results.averageRating >= average_rating)]

    def _constraint_number_votes(self, num_votes: int):
        self._dataset_results = self._dataset_results[(self._dataset_results.numVotes >= num_votes)]

    def _constraint_is_adult(self, is_adult: int):
        self._dataset_results = self._dataset_results[(self._dataset_results.isAdult == is_adult)]

    def _reset_dataset_results(self):
        self._dataset_results = self._dataset

    def _set_constraints(self, frontend_constraints: json):
        # reset the dataset
        self._reset_dataset_results()

        # constraint json to dictionary
        _constraints = json.loads(frontend_constraints)

        # filter for each constraint
        if _constraints['genres'] != '':
            self._constraint_genres(_constraints['genres'])
        self._constraint_start_year(int(_constraints['startYear'][0]), int(_constraints['startYear'][1]))
        if _constraints['averageRating'] != 0:
            self._constraint_average_rating(_constraints['averageRating'])
        if _constraints['numVotes'] != 0:
            self._constraint_number_votes(_constraints['numVotes'])
        if _constraints['isAdult'] == 0:
            self._constraint_is_adult(_constraints['isAdult'])

        self._dataset_results.reset_index(inplace=True)

        return self._dataset_results

    def get_random(self, frontend_constraints: json):
        self._set_constraints(frontend_constraints)

        # print("Number of Mature Content in Dataset: ", self._dataset_results.isAdult.value_counts())

        dataset_size = self._dataset_results.shape[0]
        dataset_index = random.randint(0, dataset_size)

        results_df = self._dataset_results[self._dataset_results.index == dataset_index]

        results = {
            'primaryTitle': results_df['primaryTitle'].values[0],
            'genres': results_df['genres'].values[0],
            'startYear': int(results_df['startYear'].values[0]),
            'averageRating': float(results_df['averageRating'].values[0]),
            'numVotes': float(results_df['numVotes'].values[0]),
            'isAdult': int(results_df['isAdult'].values[0])
        }

        print("Results: ", results)

        return json.dumps(results)
