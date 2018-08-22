from collections import OrderedDict
class Problem():
    def __init__(self):
        space = OrderedDict()
        #space['epochs'] = (5, 500)
        #bechmark specific parameters
        space['epochs'] = (5, 40)
        #space['nhidden'] = (1, 100)
        space['nhidden'] = (1, 4)
        space['nunits'] = (1, 300)
        #network parameters
        space['activation'] = ['relu', 'elu', 'selu', 'tanh']
        space['batch_size'] = (8, 1024)
        space['dropout'] = (0.0, 1.0)
        space['optimizer'] = ['sgd', 'rmsprop', 'adagrad', 'adadelta', 'adam', 'adamax', 'nadam']
        # common optimizer parameters
        #space['clipnorm'] = (1e-04, 1e01)
        #space['clipvalue'] = (1e-04, 1e01)
        # optimizer parameters
        space['learning_rate'] = (1e-04, 1e01)
        #space['momentum'] =  (0, 1e01)
        #space['decay'] =  (0, 1e01)
        #space['nesterov'] = [False, True]
        #space['rho'] = (1e-04, 1e01)
        #space['epsilon'] = (1e-08, 1e01)
        #space['beta1'] = (1e-04, 1e01)
        #space['beta2'] = (1e-04, 1e01)

        self.space = space
        self.params = self.space.keys()
        self.starting_point = [5, 1, 1, 'relu', 8, 0.0, 'sgd', 1] #1.0, 0.5, 0.01, 0, 0, False, 0.9, 1e-08, 0.9, 0.999]

if __name__ == '__main__':
    instance = Problem()
    print(instance.space)
    print(instance.params)
