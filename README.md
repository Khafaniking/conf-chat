# conf-chat
A P2P Chat

Created a very basic P2P messaging simulation using ZeroMQ and Python. Just a few ports I've set aside/set up are able to talk with each other in a Public Chat, and are able to DM each other via commands and selecting the port/address of their intended recipient.

Had planned to implement creating group chats and enabling a sort of "peeking" feature, where one player would be randomly able to view the DMs of the other members of the public chat and eavesdrop on their communications, but had issues with these and just scaled back to the public chat and DM feature. 

Requires Python (at least 3.12 as that's what it was written in) and zmq.

To run you can just simply import players.py and public_chat.py. 

Using terminal, you can then run public_chat.py typing 'python public_chat.py'

Then, use terminal to run players.py by typing 'python players.py 555X PlayerX', where X denotes a different port and Player. Ports 5551-5556 are used for Players 1 - 5. 

From the player view, they can enter the commands /dm and /public. With /public, they can then enter any message they like and this message will be logged in public_chat.py and sent to the other players. With /dm, they'll be asked to select the player port they want to talk to. For the recipient to respond, they will also have to enter /dm and initiate contact with the first messenger. 

At any point during the prompt template, you can enter '/back' to exit the DM and Public chat prompts.

