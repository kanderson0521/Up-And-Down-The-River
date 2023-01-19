# Up and Down the River

## About

Coding is something I enjoy and for the last three years I have been finding reasons to incorporate Python into my projects at work, most of which were to automate tasks by pulling data from different sources and perform some sort of analysis. All of my work and class projects were written in a procedural way and to achieve my goal of becoming a ML Engineer, I knew I would have to learn Object-oriented programming (OOP) concepts and because of that reason, this personal project of building a card game was born (typical, I know). I also took an online course to learn about unit testing while I was working on this project and decided to implement some tests using pytest to help retain what I had learned. 

Side note: The card game is called Oh Hell! and it may even have some other names, my family calls it Up and Down the River so I prefer that name but you may see it called something else depending on the person.

Second side note: I did this project to get experience with OOP and did not include exception handling. I swear I do not skip this part at work!!

## Quick Rundown About Game 

The game involves multiple rounds, where cards are dealt and players must place a bid, how many tricks they can win with their hand based on suit and values. The number of cards dealt depends on the number of players, the card count starts high on the first round, and goes down to two cards and back up, hence the name ‘Up and Down the River’. There is a trump card that is shown after dealing cards, displaying the trump suit for that round. A card of the trump suit is worth more points than any suit but can only be played if the starting card for that trick was a trump suit or the player does not have any cards matching the starting suit. After all cards are played, winners who won what they bid will have their bid + 10 points added to their score. 


Here is a video demo of the game being played:



https://user-images.githubusercontent.com/54673004/168497541-3839736a-c133-4a04-8552-0515a7c57795.mp4




## How to use

You will need game_play and game_objects to play the game, the random library is the only required library. 

If you want to check out my unit tests, you will need the conftest.py file which houses all the fixtures that pytest uses and you will need the test_game_methods.py file which runs the tests.
