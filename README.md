# Cribbage!

## Dependencies

*Note that we need Python 3.11 for arcade to be installable.*
Use a venv maybe?

To run the game you should install:



``` pip install arcade ```

``` pip install numpy ```

## Program Architecture

--Let me know how this looks - Carson J. King

Back End: All methods that alter the game state. Broken up into each part of a player's respective turn.

Front End: Graphical aspects such as displaying the game state and also taking in user input.

How They Connect: Front End recieves user input that something was clicked, Front End then calls backend methods to alter the game state based on what was clicked, Back End updates the game state using its methods, Front End redraws board based on game state.