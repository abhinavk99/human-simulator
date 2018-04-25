import random

class Markov(object):
    """Markov chain
    """

    def __init__(self):
        """Initialize an empty directed graph
        """
        self.states = {}

    def add_state(self, state):
        """Add a state to the Markov chain
        """
        if (isinstance(state, State)):
            self.states[state.value] = state
        else:
            raise TypeError('Adding non State object to Markov chain')

    def get_rand_state(self):
        """Get a random state from the Markov chain
        """
        random_val = random.choice(tuple(self.states))
        return self.states[random_val]


class State(object):
    """Node in a Markov chain
    """

    def __init__(self, value):
        """Initialize a new state with no transitions
        """
        self.value = value
        self.transitions = {}

    def add_transition(self, transition):
        """Add a transition to the state
        """
        if (isinstance(transition, Transition)):
            self.transitions[transition.dest.value] = transition
        else:
            raise TypeError('Adding non Transition object as an edge')

    def counts(self):
        """Gets the weights of the outgoing edges
        """
        return (self.transitions[t_val].count for t_val in self.transitions)

    def get_next(self):
        """Randomly picks an outgoing edge
        """
        weights = self.counts()
        n = random.randint(1, sum(weights))
        for dest_val in self.transitions:
            tr = self.transitions[dest_val]
            if n <= tr.count:
                return tr
            else:
                n -= tr.count

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Transition(object):
    """Weighted edge in a Markov chain
    """

    def __init__(self, dest, count, value):
        """Initialize a transition to a destination
        """
        self.dest = dest
        self.count = count
        self.value = value