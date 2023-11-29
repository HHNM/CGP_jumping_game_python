
GRAVITY = 0.6
SCREEN_THRESH = 200
MAX_PLATFORM = 20

FPS = 60
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 672 


TITLE = 'Jumping AI via Evolutionary Cartesian Genetic Programming'

# how many levels back are allowed for inputs in CGP
LEVEL_BACK = 20

# number of cols (nodes) in a single-row CGP
N_COLS = 100   


# if True, then additional information will be printed
VERBOSE = False
# gap (Horizontal space) between a pair of platforms
MAX_PLATFORM_GAP = 150
# minimum length of a PLATFORM
MIN_PLATFORM_LENGTH = 97
# parameters of evolutionary strategy: MU+LAMBDA
MU = 2
LAMBDA = 8
N_GEN = 300  # max number of generations

# parameters of cartesian genetic programming
MUT_PB = 0.3  # mutate probability
N_COLS = 100   # number of cols (nodes) in a single-row CGP
LEVEL_BACK = 80  # how many levels back are allowed for inputs in CGP

# Postprocessing
# if True, then the evolved math formula will be simplified and the corresponding
# computational graph will be visualized into files under the 'pp' directory
PP_FORMULA = True
PP_FORMULA_NUM_DIGITS = 5
PP_FORMULA_SIMPLIFICATION = True
PP_GRAPH_VISUALIZATION = True