# Artificial Intelligence Nanodegree

## Diagonal Sudoku Solver

[image1]: ./images/sudoku_screenshot.gif "Sudoku Screenshot"

### Project Overview 

In this project, we write code to implement two extensions of our Sudoku solver. The first one will be to implement the technique called "naked twins". The second one will be to modify our existing code to solve a diagonal sudoku. The goals are to implement the naked twins function and write an AI agent that will solve the Diagonal Sudoku game and experience constraint propagation in both implementations. 

Some additional features have been added in this implementation. Although that was not requested for this project, some suggestions were made by the Udacity reviewer and they have been added as improvements: 

* Added quick testers [Effective assertions](https://wiki.python.org/moin/UsingAssertionsEffectively)
* Added logging calls [Basic logging tutorial](https://docs.python.org/3/howto/logging.html)
* Modularize the code. The original naked_twins() function was written in a single function, and after the review has been split in find_twins() and eliminate_twins()
* Implement hidden_twins() as a new solver strategy 
    * [Reference1](https://www.sudokuoftheday.com/techniques/hidden-pairs-triples/)
    * [Reference2](http://www.sudokudragon.com/tutorialhiddentwins.htm)

Please note that the grid to solve is provided in the code itself within the `solution.py` file. 

#### Question 1: Naked twins 

Q: How do we use constraint propagation to solve the naked twins problem?  
A: By removing the two candidate numbers from its peers. It's a good way of improving the efficiency of the algorithm: initially, we use constraint propagation assigning the one possible value to the box that only can have that value (a big constraint), and consequently removing that value from its peers. Eventually, instead of roughly search, we can find the naked-twins values and do the same. Obviously a search strategy has a great cost in terms of performance, however, we can reduce the puzzle and improve the efficiency if we find more constraints as finding the boxes with the same two digits, this way we can reduce the number of iterations.   

#### Question 2: Diagonal Sudoku

Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Making the unit list bigger by adding the diagonal we are increasing the number of peers to check, that means more restrictions, so more constraint. Initially, we had 27 units, after considering the diagonal we have 29, so the peers for those boxes on the path diagonal increase from 20 (not considering the diagonal) to 26. 

Example: 

Number of peers of A1 (in diagonal):  26
Number of peers of B1 (not in diagonal):  20
Number of peers of D4 (in diagonal):  26

It would seem that we as our list is bigger and we have more boxes to check for peers, the performance might be slow, but it is not, as we are dramatically reducing the number of possibilities for each box, and so improving the performance of the algorithm. 

**Further documentation for this project can be found in this [resource](Solve_any_Sudoku_with_AI.ipynb) notes taken from [http://norvig.com/sudoku.html]**

![Sudoku Screenshot][image1]

### Modules

* `solution.py` - Sudoku Solver
* `solution_test.py` - Test lib for solution by running `python solution_test.py`.
* `PySudoku.py` - This is code for visualizing the solution.
* `visualize.py` - This is code for visualizing the solution.

### Install and Environment required

[Install](https://github.com/udacity/AIND-Sudoku)

* Download the aind-universal.yml (on this repo)
* conda env create -f aind-universal.yml to create the environment
* Activate the environment:
        * run source activate aind (OSX & Linux)
        * run activate aind (Windows)  

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

[Usage] python solution.py

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py
