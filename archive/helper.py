from archive.negamax import NegamaxEngine
from archive.random import RandomEngine
from archive.firstMove import FirstMoveEngine
from archive.lastMove import LastMoveEngine
from archive.config import Config

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