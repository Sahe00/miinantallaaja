This is the final course project for the elementary programming course. The project is essentially a minesweeper game or perhaps I should call it a *minestomper* in this instance. :) 


**Description:**
* The gameplay is the classic minesweeper experience where your goal is to uncover all the cells on the board without detonating any mines.
  
* Once welcomed to the menu screen, interaction with the menu is done by text in the console window. You can choose to either start a new game [1], inspect statistics from past games [2], or exit out of the game [3]. The selection is done by entering the corresponding number in the console window (1-3).
  
* When a new game is begun [1], you are able to customize the difficulty of the game to your preferences. You can customize the board size by choosing your preferred width and length. Additionally, you can also choose the preferred amount of mines on the field. It is worth noting that the maximum size of the board is 25x25, and anything beyond that will get rejected. There cannot be more mines on the field as there are available cells. However, choosing an appropriate amount of mines will still be on the player.
* The minesweeper game itself is run on a seperate graphical user interface. See 'haravasto' library.
  
* You can put up flags, indicated by red "!" icons on the board, by right-clicking on the desired cell. To uncover a cell you left-click the desired cell, and the cell will turn darker and/or have a number on it indicating the amount of mines adjacent to the cell.
  
* After a game is completed, the result of the game is shown in the console. The result as well as some other statistics such as time and turns are recorded related to each game. To see these records you can access them by choosing the second option [2] once you launch the application.
  


