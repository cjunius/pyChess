from engines.negamax import NegamaxEngine
from engines.random import RandomEngine
from engines.firstMove import FirstMoveEngine
from engines.lastMove import LastMoveEngine
from config import Config

def get_engines(config: Config = Config()):
    return [NegamaxEngine(config=config), RandomEngine(config=config), FirstMoveEngine(config=config), LastMoveEngine(config=config)]

def get_negamax_engine(config: Config = Config()):
    return NegamaxEngine(config=config)

def get_random_engine(config: Config = Config()):
    return RandomEngine(config=config)

def get_firstmove_engine(config: Config = Config()):
    return FirstMoveEngine(config=config)

def get_lastmove_engine(config: Config = Config()):
    return LastMoveEngine(config=config)