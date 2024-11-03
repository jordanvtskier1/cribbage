# Development Plan

Refer to [this file](Flowchart.mmd) for all state representations.
The idea is that our GameState keep track of different states of the game.
The different states are:
- StartMenu
- Deal
- Add To Cribbage
- Play
- Wait for other player to make move
- Calculate Score
- End Game

If we can keep track of all states of the game that we are in we can succesfully 
constraint what we must represent on the screen and what we do not.

At all times FrontEnd **CAN ONLY** access the state of the game as a read variable.
This ensures that it remains separated from the logic of the backend.

## On  Draw

### Start Menu
Must show only a button to start the game.

(Optional) Change player names.
(In the future). Make a connection to Other Player.

### Deal 

State Deal needs:
- Which player is the dealer
- Which player has the crib

Deal will show:
- An empty cribbage
- An empty score board
- A deck of cards (Non clickable)
- A Sprite Button **DEAL**
#### On click:
Only the Deal button can be clicked in this state
- Update the Game State to Add to Crib
- Shuffle a deck of cards
- Give players 6 cards
- Determine a card on top of the deck

### Add to Crib
#### State Add to Crib needs:
- Which player has crib
- Which player is dealer
- Cards on hand
- Card on top of deck

#### Add to crib will show:
- A player's cards on their hands
- Card on top of the deck
- Crib on either ours or opposite side
- Empty cribbage, empty score board

#### On click:
On this state we wait for two on hand cards to be clicked
- Update backend to add 2 cards to cribbage
- Simulate P2 adding 2 cards for now
- Update stay to Play 

### Play
(It is our turn)
#### State Play Needs:
- cards on hand
- cards on crib
- who has crib
- Scoreboard
- Card on top of deck
- Cards on center (Starts at 0)
- Running sum on center

#### Will show:
All the listed above needs

#### On click:
Only one card on our hand must be clicked
Backend adds a card to the center
If cards left on our hand
- If other player can play: Transition to Wait State
- If other player cannot play: Transition to Play State
If no cards left on our hand:
- If other player can play: Transition to Wait
- No one can play: Transition to calculate score

### Wait 
(Not our turn or cannot play)

This state is the same as play except we cannot click any sprites

Should call a function periodically so the backend can check for state updates

### Calculate Score
#### Needs
Same as Play

#### Shows
- Same as play
- Calculate score button

#### On click
Only can click score button.

Calls the backend which returns a calculated score.

Adds to the cribbage current score

Updates the state to deal
