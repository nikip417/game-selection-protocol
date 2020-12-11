Nikita Patel
CS 544 - Computer Networks


The Game Selection Protocol - README


The primary purpose of GSP is to allow users to play games so thus the implementation of this protocol will be tested and proved through the playing of a simple tic-tac-toe game. In order to play, consider the following notes and follow the steps below or watch the video where the same steps are explained.


Notes::
The GSP protocol is written entirely in python3 and was developed and tested on a Unix machine and all the commands provided are the ones used by myself to run on said Unix system.


Steps to run:
Once you have ensured that you are in the project directory


Step 1: Start the GSP server
Run the command below and once the server has started, you will see a single log indicating such that say “The GSP server is listening”
python3 GSP_server_start.p


Step 2: Start GSP clients
python3 GSP_client_start.py


Step 3: Log in
When each client is started the user will have to go through a series of prompts in the command-line interface. The user will initially be asked for a username and password, this can be anything, the application will simply create your account for you if it does not already exist and then it will automatically log you in.


Step 4: Choose your opponents
If there are only two servers running at a single time, respond ‘yes’ in one and ‘no’ in the other. Something to note is that you may run into problems, due to the way the ui is setup, if there is only one client and not users are found so it is best to log into two clients and then say yes in one and no in the other.
The player that said yes will have a random opponent chosen for them from the users that are logged in and are registered to play the same game that the initiating user is wanting to play (in this case ‘tic-tac-toe). Once an opponent is found, the application will automatically send a request to that user. Looking in the client that is waiting for game requests (the other client), a prompt like the following will appear
        Would you like to play a game of tic_tac_toe with opponent nrp62 (yes/no)
By answering ‘yes’ you are accepting the request and the requesting user is notified. Going back to the requesting client, you will see the following prompt
        Would you like to start the game? (yes/no)
Type ‘yes’ and the tic-tac-toe will begin!


Step 5: Play
Instructions on how to play will appear on the screen and the game can begin. Only thing to note here is when typing the location where you want to place your mark, it should be separated by a single comma and have no spaces. For example 0,0




Analysis:
It is the intent of the Game Selection Protocol to be robust in nature, protecting the security of its users as well as the integrity of the games played on it. However, the current implementation is fairly basic in nature. It proves out the concepts of what GSP is trying to do but does not quite go above and beyond in every single one of those aspects. There are areas where the protocol implementation can grow and become more robust and for such growth. However, it was implemented with the possibility of such improvements in mind and thus, improvements can be done more easily and the basic architecture can remain the same. 


For example, one area where improvements can be made is through message validation. The messages on send and on receive should be checked for their components and that they have been formatted correctly as to not break the system and protect it further. Validation could include checking message component values for correct types, making sure the correct number of parameters are included in each message and always checking for a delimiter. At a basic level, however, this does exist. In reading messages, GSP only extracts the components that it needs, not reading the entire message buffer if it doesn’t have to. This mitigated risk of additional, unexpected data from ruining game play to an extent.


Additional levels of validation are provided through state checking that is enabled by the DFA. There is a very explicit mapping of what commands can be executed in which states as well as what ACKs and NAKs do to the client state. The explicit nature of the state checking helps to protect the protocol from some fuzzing. The state validation has been tested thoroughly to guarantee this to protect against bad users trying to send information in attempts to corrupt the system.


In the future it would also be beneficial to secure the game play process further. Currently, when a player makes a move and that move is sent to the other player, there is no checking to make sure that they user did not manipulate the board dishonestly in their favor. While it is somewhat incumbent on the application running on GSP to do this checking and implement this level of safety there are definitely steps that can be taken by GSP as well. The GSP server can hold on to all in progress game information such as last known game state to help in cases where a user did not receive a message or in other events where users try to corrupt the game.


GSP currently does a good job at user validation. Every time a user logs in, there is a password check as well as hostname update. On every message there is also hostname validation to ensure another client is not trying to send information under the name of another. These are all checks that occur is a user is registered in the system. Additional checks keeping Unregisted users from causing harm to the system are put in place through the state validation discussed earlier.