from deephyper.problem import NaProblem
from deephyper.benchmark.nas.linearRegMultiVar.load_data import load_data
from deepspace.tabular import OneLayerSpace


Problem = NaProblem()

Problem.load_data(load_data)

Problem.search_space(OneLayerSpace)

Problem.hyperparameters(batch_size=100, learning_rate=0.1, optimizer="adam", num_epochs=1)

Problem.loss("mse")

Problem.metrics(["r2"])

Problem.objective("val_r2")


# Just to print your problem, to test its definition and imports in the current python environment.
if __name__ == "__main__":
    print(Problem)
