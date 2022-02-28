import copy

from player import Player
import numpy
import numpy as np
import random
import csv


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"


    def roulette(self, items, n):
        total = float(sum(w.fitness for w in items))
        results = []
        i = 0
        w, v = items[0].fitness, items[0]
        while n:
            x = total * (1 - numpy.random.random() ** (1.0 / n))
            total -= x
            while x > w:
                x -= w
                i += 1
                w, v = items[i].fitness, items[i]
            w -= x
            results.append(v)
            n -= 1
        return results

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)

        # TODO (Additional: Learning curve)

        
        result = self.roulette(players, num_players)
        
        players.sort(key=lambda x: x.fitness, reverse=True)
        
        fitnesses = np.array([x.fitness for x in players])
        max_fitness = np.max(fitnesses)
        min_fitness = np.min(fitnesses)
        avg_fitness = round(np.average(fitnesses))
        print(' - max: {}\n - min: {}\n - avg: {}'.format(max_fitness, min_fitness, avg_fitness))
        # writing data on a csv file
        with open(r'fitness_data_for_plotting.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([min_fitness, avg_fitness, max_fitness])
        return result

    def sus(self, players, num_players):
        sum_of_fitness = np.sum([x.fitness for x in players])
        step_size = sum_of_fitness / num_players

        # creating the ruler
        ruler = np.arange(num_players) * step_size
        random_number = np.random.uniform(0, step_size)
        ruler = ruler + random_number

        selected_players = []
        for r in ruler:
            i = 0
            f = 0
            while f < r:
                f += players[i].fitness
                i += 1
            selected_players.append(players[i - 1])
        return selected_players

    def mutate_array(self, array, prob, std, r):
        seed = random.randint(0, 1000000000)
        rs = np.random.RandomState(seed)

        # change weights
        mutation_mask = rs.random(array.shape) < prob
        while np.sum(mutation_mask) == 0:
            mutation_mask = rs.random(array.shape) < prob
        mutation = mutation_mask * rs.normal(0, std, array.shape)
        array += mutation


    def mutate(self, child):
        mutation_prob = 0.6
        mutation_std = 0.9
        r = np.random.rand()
        self.mutate_array(child.nn.w0, mutation_prob, mutation_std, r)
        self.mutate_array(child.nn.b0, mutation_prob, mutation_std, r)
        self.mutate_array(child.nn.w1, mutation_prob, mutation_std, r)
        self.mutate_array(child.nn.b1, mutation_prob, mutation_std, r)

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            #new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            new_players = []
            candidates = self.sus(prev_players, num_players)
            for c in candidates:
                child = self.clone_player(c)
                self.mutate(child)
                new_players.append(child)
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
