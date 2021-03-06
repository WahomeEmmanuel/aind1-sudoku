# Imports
import logging
from  builtins import any as b_any

# Declare vars and constants
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


# Good logging practice
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='sudoku_solver.log',
                    filemode='w')
logger = logging.getLogger(__name__)
logger.info('Start...')


# Functions for Sudoku Solver #################


# Forward declaration

def cross(A, B):
    "Cross product of elements in A and elements in B to name the boxes"
    return [s+t for s in A for t in B]


# Define boxes, rows and cols units that will compose the grid
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Define the diagonal units 
diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))]] + [[rows[i]+cols[::-1][i] for i in range(len(rows))]]


# Add the diagonal units to the unit list
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def test():
    """    
    Some unit tests
    """

    try:

        assert len(boxes) == 81, "Less or more boxes than 81"
        assert len(unitlist) == 29 # 27 + 2 (diagonal boxes)
        assert len(peers['A1']) == 26
        assert len(peers['B1']) == 20
        # Box D4 in diagonal
        assert peers['D4'] == set(['E4', 'A1', 'I4', 'D1', 'H4', 'E6', 'D8', 'B4', 'D9', 'F4', 'C3', 'E5', 'D5', 'F5', 'F6', 'G7', 'G4', 'D6', 'D2', 'D7', 'A4', 'C4', 'D3', 'B2', 'I9', 'H8'])
        # Box B1 not in diagonal
        assert peers['B1'] == set(['A1', 'A3', 'B9', 'B5', 'F1', 'D1', 'I1', 'B4', 'E1', 'B3', 'C3', 'B6', 'G1', 'B8', 'B7', 'C2', 'H1', 'A2', 'B2', 'C1'])
           
        logger.info('All tests passed.')

    except Exception as err:
        logger.error("test(): Fatal error running tests")                          

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values

    try: 

        if values[box] == value:
            return values

        values[box] = value
        if len(value) == 1:
            assignments.append(values.copy())

        #logger.info(values)
        #logger.info('\n')    

        return values


    except Exception as err:
        logger.error("assign_value(): Fatal error assigning value")   



def find_naked_twins(values): 
    """Find values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        naked_twins (list): a list of lists containing each pair of naked twins. Example [[A1, B1], [D4, E5], [H4, C4]]
    """

    try: 
        
        # Create a list of boxes with the boxes with two values (candidates for naked twins)
        _twins = [box for box in values.keys() if len(values[box]) == 2]
       
    
        # Find the naked twins and create a list of lists
        naked_twins = [[box1, box2] for box1 in _twins for box2 in peers[box1] if set(values[box1]) == set(values[box2])]
        
        logger.info("find_naked_twins(): naked_twins_list... " + str(naked_twins) + "\n")
             
        return naked_twins
    
    except Exception as err:

        logger.error("find_naked_twins(): Fatal error finding naked-twins")


def eliminate_naked_twins(naked_twins, values): 

    """Eliminate values using the naked twins strategy.
    Args:
        naked_twins (list): a list of lists containing each pair of naked twins. Example [[A1, B1], [D4, E5], [H4, C4]]
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    
    Returns:
        values(dict): the values dictionary with the naked twins eliminated from peers.
    """

    try:

        for i in range(len(naked_twins)):
            box1 = naked_twins[i][0]  # From the previous example : box1 = naked_twins[0][0] --> A1
            box2 = naked_twins[i][1]  # From the previous example : box1 = naked_twins[0][0] --> B1

            logger.info("box1 = " + box1 + "\n")
            logger.info("box2 = " + box2 + "\n")


            # Join the two sets 
            common_peers = set(peers[box1]) & set(peers[box2])

            logger.info("naked_twins(): common_peers = " + str(common_peers) + "\n")
         

            # Remove the naked twins as candidates from the common peers
            for peer in common_peers:
            
                if len(values[peer]) > 1: # if the values contained in the box, peer to naked-twins are 2 or more....
                    
                    _to_remove = values[box1]

                    logger.info("box1 : " + box1 + " these values : " + str(_to_remove) + " will be removed from peer's value " + peer + " : " + str(values[peer]) + "\n")
               
                    for k in _to_remove: 
                        
                        logger.info("naked_twins(): k value = " + str(k) + ", peer = " + peer + ", and values in peer were = " + values[peer])
                        values = assign_value(values, peer, values[peer].replace(k, '')) # remove the value from the peer
                        logger.info("naked_twins(): now peer's value = " + values[peer] + "\n")

                        
        return values

    except Exception as err: 

        logger.error("eliminate_twins(): Fatal error eliminating naked-twins \n")
   

def naked_twins(values):
    """Find & Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Remove the naked-twins 
    return eliminate_naked_twins(find_naked_twins(values), values)


def find_hidden_twins(values):
    """ Find all instances of hidden twins
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the hidden twins eliminated from peers.
    """
      
    try: 
        # Create a list of boxes with the boxes with two values (candidates for naked twins)
        _twins = [box for box in values.keys() if len(values[box]) >= 2]
        logger.info("hidden_twins(): ALL CANDIDATES: " + str(_twins) + "\n") 

        for box1 in _twins: 
            for box2 in peers[box1]:
                if len(set(values[box1]))==2 and len(set(values[box1]) & set(values[box2]))==2 and set(values[box1]) != set(values[box2]):
                    logger.info("hidden_twins() boxes: " + str(box1 + box2) + str(set(values[box1])) + str(set(values[box2])) + "\n") 
                    logger.info("hidden_twins() boxes: " + str(box1 + box2) + str(set(values[box1]) & set(values[box2])) + "\n")
                    
                               


        return values           
        

        
    
    except Exception as err:

        logger.error("find_hidden_twins(): Fatal error finding hidden-twins")



def eliminate_hidden_twins(hidden_twins_list, values): 

    """Eliminate values using the naked twins strategy.
    Args:
        naked_twins (list): a list of lists containing each pair of hidden/naked twins. Example [[A1, B1], [D4, E5], [H4, C4]]
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    
    Returns:
        values(dict): the values dictionary with the naked twins eliminated from peers.
    """

    try:

        logger.info("hidden_twins() INITIAL VALUES : " + str(values) + "\n")
       
        for i in range(len(_twins_list)):

            box1 = _twins_list[i][0]  # From the previous example : box1 = naked_twins[0][0] --> A1
            box2 = _twins_list[i][1]  # From the previous example : box1 = naked_twins[0][0] --> B1

            logger.info("box1 = " + box1 + "\n")
            logger.info("box2 = " + box2 + "\n")

            # Build a set with the common peers, the intersection of both peers
            common_peers = set(peers[box1]) & set(peers[box2])
            logger.info("hidden_twins(): common_peers = " + str(common_peers) + "\n")

            hidden_pair = set(values[box1]) & set(values[box2])
            hidden_pair = list(hidden_pair)
            logger.info("hidden_twins(): hidden_pair = " + str(hidden_pair) + "\n")

            common_peers = [values[k] for k in common_peers] 

            if not(b_any(hidden_pair[0] in x for x in common_peers) or b_any(hidden_pair[1] in x for x in common_peers)):
                # logger.info("hidden_twins(): hidden_pair FOUND!!! = " + str(hidden_pair) + "\n")
                # logger.info("hidden_twins(): hidden_pair FOUND!!! not in common_peers = " + str(common_peers) + "\n")
            
                assign_value(values, box1, hidden_pair[0] + hidden_pair[1])
                assign_value(values, box2, hidden_pair[0] + hidden_pair[1])

                logger.info("hidden_twins(): assigned = " + hidden_pair[0] + hidden_pair[1] +  " in " + box1 + " and " + box2 + "\n")
                
                logger.info("hidden_twins() UPDATED VALUES : " + str(values) + "\n")         

        return values

    except Exception as err: 

        logger.error("eliminate_twins(): Fatal error eliminating naked-twins \n")
   



def hidden_twins(values):
    """Find & Eliminate values using the hidden twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the hidden twins eliminated from peers.
    """

    # Find all instances of hidden twins
    # Remove the hidden-twins 

        
    # return eliminate_hidden_twins(find_hidden_twins(values), values) 
    return find_hidden_twins(values)             



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81, "Wrong number of boxes on the grid"
    return dict(zip(boxes, chars))




def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    

def eliminate(values):
    """
    Remove the value
    """

    try: 
        
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_values:
            digit = values[box]
            for peer in peers[box]:
                # values[peer] = values[peer].replace(digit,'')

                # def assign_value(values, box, value):
                # logger.info("eliminate(): removed " +  values[peer])   
                values = assign_value(values, peer, values[peer].replace(digit, ''))
        return values

     
    except Exception as err:
        logger.error("eliminate(): Fatal error eliminating the value")      

def only_choice(values):
    """
    """

    try: 
        for unit in unitlist:
            for digit in cols:
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    # values[dplaces[0]] = digit
                    values = assign_value(values, dplaces[0], digit)

        return values

    except Exception as err:
        logger.error("only_choice(): Fatal error only_choice")       

def reduce_puzzle(values):
    """
    """
    stalled = False
    # auxlist = [] # for testing find_ methods

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Use the Hidden Twins Strategy
        values = hidden_twins(values)
              
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False:
        return False ## Failed earlier
    
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':

    test()

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

    logging.info('Exit')
