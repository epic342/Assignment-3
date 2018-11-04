from abc import ABCMeta, abstractmethod


class GraphManager(object):
    def __init__(self, graph_behaviour):
        self.behaviour = graph_behaviour

    def make_graph(self, statistics):
        # if isinstance(self.behaviour, AbstractGraphBuilder):
        self.behaviour.initialize()
        self.behaviour.insert()
        self.behaviour.create(statistics)
        # else:
        #     print("The graph you specified did not get made")


class AbstractGraphBuilder(metaclass=ABCMeta):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def create(self, statistics):
        pass
