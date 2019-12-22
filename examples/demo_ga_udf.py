# step1: define your own operator:
def selection_tournament(self, tourn_size):
    FitV = self.FitV
    sel_index = []
    for i in range(self.size_pop):
        aspirants_index = np.random.choice(range(self.size_pop), size=tourn_size)
        sel_index.append(max(aspirants_index, key=lambda i: FitV[i]))
    self.Chrom = self.Chrom[sel_index, :]  # next generation
    return self.Chrom


# %% step2: import package and build ga, as usual.
import numpy as np
from sko.GA import GA, GA_TSP

demo_func = lambda x: x[0] ** 2 + (x[1] - 0.05) ** 2 + (x[2] - 0.5) ** 2
ga = GA(func=demo_func, n_dim=3, size_pop=100, max_iter=500, lb=[-1, -10, -5], ub=[2, 10, 2],
        precision=[1e-7, 1e-7, 1])

# %% step3: register your own operator
ga.register(operator_name='selection', operator=selection_tournament, tourn_size=3)
# %% Or import the operators scikit-opt already defined.
from sko.operators import ranking, selection, crossover, mutation

ga.register(operator_name='ranking', operator=ranking.ranking). \
    register(operator_name='crossover', operator=crossover.crossover_2point). \
    register(operator_name='mutation', operator=mutation.mutation)

# %% Run ga
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)

# %% Plot the result
import pandas as pd
import matplotlib.pyplot as plt

Y_history = pd.DataFrame(ga.all_history_Y)
fig, ax = plt.subplots(2, 1)
ax[0].plot(Y_history.index, Y_history.values, '.', color='red')
Y_history.min(axis=1).cummin().plot(kind='line')
plt.show()
