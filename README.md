# Cribbage!

## Dependencies

*Note that we need Python 3.11 for arcade to be installable.*
Use a venv maybe?

To run the game you should install:



``` pip install arcade ```

*If you are having trouble installing arcade here are some notes:
Please make sure python 3.11 is installed on your device.
Use py -3.11 -m pip install arcade if installing arcade is failing.
Make sure when you run main.py that you are running it in python 3.11*

``` pip install numpy ```

## Program Architecture

Back End: All methods that alter the game state. Broken up into each part of a player's respective turn.

Front End: Graphical aspects such as displaying the game state and also taking in user input.

How They Connect: Front End recieves user input that something was clicked, Front End then calls backend methods to alter the game state based on what was clicked, Back End updates the game state using its methods, Front End redraws board based on game state.