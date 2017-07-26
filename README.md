# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: By removing the two candidate numbers from its peers. It's a good way of improving the efficiency of the algorithm: initially we use constraint propagation assigning the one possible value to the box that only can have that value (a big constraint), and consequently removing that value from its peers. Eventually instead of roughly search, we can find the naked-twins values and do the same. Obviously a search strategy has a great cost in terms of performance, however we can reduce the puzzle and improve the efficiency if we find more constraints as find the boxes with the same two digits, this way we can reduce the number of iterations.   

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Well, making the unitlist bigger by adding the diagonal we are increasing the number of peers to check, that means more restrictions, so more constraint. Initally we had 27 units, after considering the diagonal we have 29, so the peers for those boxes on the path diagonal increase from 20 (not considering the diagonal) to 26. 

Example: 

Number of peers of A1 (in diagonal):  26
Number of peers of B1 (not in diagonal):  20
Number of peers of D4 (in diagonal):  26

It could seem that we as our list is bigger and we have more boxes to check for peers, the performance might be slow, but it is not, as we are drammatically reducing the number of possibilities for each box, and so improving the performance of the algorithm. 


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

