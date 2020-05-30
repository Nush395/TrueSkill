import os
from src.utils.maths import Gaussian
from abc import ABC, abstractmethod
from src.trueskill.constants import MU, SIGMA


class DataSource(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect_to_source(self):
        pass

    @abstractmethod
    def load_player_ratings(self, player_name):
        pass

    @abstractmethod
    def update_player_rating(self, player_name, new_skill):
        pass

    @abstractmethod
    def bulk_update_player_ratings(self, ratings):
        pass

    @abstractmethod
    def save_player_ratings(self):
        pass


class CsvSource(DataSource):
    def __init__(self, data_dir='.'):
        super().__init__()
        self.DATA_SOURCE = 'true_skills.csv'
        self.data = {}
        self.connect_to_source(data_dir=data_dir)

    def connect_to_source(self, data_dir='.'):
        if os.path.exists(os.path.join(data_dir, self.DATA_SOURCE)):
            with open(os.path.join(data_dir, self.DATA_SOURCE), 'r') as f:
                line = f.readline().strip('\n')
                while line:
                    name, mu, sigma = line.split(',')
                    mu, sigma = float(mu), float(sigma)
                    rating = Gaussian(mu=mu, sigma=sigma)
                    self.data[name] = rating
                    line = f.readline().strip('\n')

    def load_player_ratings(self, player_name):
        if player_name not in self.data:
            self.data[player_name] = Gaussian(mu=MU,
                                              sigma=SIGMA)
        return self.data[player_name]

    def update_player_rating(self, player_name, new_skill):
        self.data[player_name] = new_skill

    def bulk_update_player_ratings(self, ratings):
        self.data.update(ratings)

    def save_player_ratings(self, data_dir='.'):
        with open(os.path.join(data_dir, self.DATA_SOURCE), 'w+') as f:
            for name in self.data:
                rating = self.data[name]
                f.write(f"{name},{rating.mu},{rating.sigma}\n")

