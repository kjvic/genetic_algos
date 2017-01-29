from Genetic import Genetic
"""
Goal: Use Genetic.Genetic to find a series of 
number / symbol / ... / number
args such that you end up with an expression for some target number.
"""

# The legend used for decoding
NUMBERS = {'0000':0, '0001':1, '0010':2, '0011':3, '0100':4,
           '0101':5, '0110':6, '0111':7, '1000':8, '1001':9}
SYMBOLS = {'1010':'plus', '1011':'minus', '1100':'times', '1101':'divideby'}

def expr_for(num):
    """
    Goal: find a series of number / symbol / ... / number
    such that you end up with an expression for the target number.
    This function returns a function which accomplishes this goal
    when interfaced with the Genetic class.
    """
    def _fitness(chromosome):
        segmented = segment(chromosome)
        decoded = decode(segmented)
        print "num = {}, decoded = {}".format(num, decoded)
        if num == decoded:
            print "Solution found\n"
            return 1
        else:
            print "fitness = {}\n".format(1.0/(1 + abs(num - decoded)))
            return 1.0/(1 + abs(num - decoded))
    return _fitness

def segment(chromosome):
    """
    Segments the chromosome bitstring into groups of 4:
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    becomes ['abcd', 'efgh']
    """
    # truncate chromosome if it's not a multiple of 4
    rem = len(chromosome) % 4
    chromosome = chromosome[0:len(chromosome)-rem]
    # lump groups of 4 into temp; then append to segmented
    segmented = []
    for i in range(len(chromosome)/4):
        temp = ''
        for j in range(4):
            temp += str(int(chromosome[i*4 + j]))
        segmented.append(temp)
    return segmented

def decode(chromosome):
    """
    Given a list of lumps of four bits, e.g. ['0000', '1010']
    decode each lump into a character, and then parse the expression
    formed by the entire list
    """
    expr = sanitize(chromosome)
    # stop when there's only 1 term left (i.e. stop when the expr is eval'd)
    while len(expr) > 1:
        expr[0] = eval_trio(expr[0], expr[1], expr[2])
        expr.pop(1)
        expr.pop(1) # would be expr.pop(2), but we just popped 1
    return expr[0]

def sanitize(chromosome):
    """
    Under this model, we expect number-symbol-number-symbol...number
    Ignore any lumps that break this pattern.
    """
    expr = []
    expecting_number = True
    for lump in chromosome:
        if expecting_number and (lump in NUMBERS.keys()):
            expr.append(NUMBERS[lump])
            expecting_number = False
        elif (not expecting_number) and (lump in SYMBOLS.keys()):
            expr.append(SYMBOLS[lump])
            expecting_number = True
    # Don't want unfinished expressions like '1 + ...' left at the end
    if expecting_number and len(expr):
        expr.pop()
    print expr
    return expr

def eval_trio(operand1, infix_operator, operand2):
    """Evaluates a trio of recognized symbols."""
    if infix_operator == 'plus':
        return operand1 + operand2
    elif infix_operator == 'minus':
        return operand1 - operand2
    elif infix_operator == 'times':
        return operand1 * operand2
    elif infix_operator == 'divideby':
        if operand1 == operand2:
            return 1
        if operand2 == 0:
            return operand1
        else:
            return float(operand1) / float(operand2)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--population-size", default = 10,
                      help="The number of chromosomes in the population")
    parser.add_option("-c", "--chromosome-size", default = 44,
                      help="The number of bits per chromosome (multiple of 4)")
    parser.add_option("-t", "--target", default = 5,
                      help="The target number to be expressed")
    parser.add_option("-n", "--num_generations", default = 10,
                      help="The number of generations to simulate")
    (options, args) = parser.parse_args()

    population_size = options.population_size
    chromosome_size = options.chromosome_size
    target          = options.target
    num_generations = options.num_generations

    # Runs until it finds a solution
    fitness_func = expr_for(target)
    god = Genetic(fitness_func, chromosome_size, population_size)
    god.find_sol()

    # Runs for a set num_generations
    num_generations = 10
    fitness_func = expr_for(target)
    mother_nature = Genetic(fitness_func, chromosome_size, population_size)
    for _ in range(num_generations):
        population = mother_nature.generation()

