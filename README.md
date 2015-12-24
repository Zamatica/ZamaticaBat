

ZamaticaBat
-
ZamaticaBat is a simple python bot for twitch. The connection is base on a IRC connection from Sevadus. It is capable of multiple things, with more to come soon. 

To run the bot, simply install **Python3** and double click on **setup.py**, follow the prompts and then click on **run.py**. 

### Table of Contents
 - [Dependencies](#dependencies)
 - [Optional](#optional)
 - [Streaming](#streaming)
 - [Variables](#variables)
 - [Full Commands List](#full-commands-list)
 - [Changelog](#changelog)
 - [To Do](#to-do)

##### Author: Zamatica
Release: 1.4.5<br>
Releases: https://github.com/Zamatica/ZamaticaBat/releases

##### Tested on Windows


### Dependencies:
	
- [Python 3.x.x](https://www.python.org/downloads/)

### Optional:
- [SQLite3 Browser](http://sqlitebrowser.org/) - Allows you to edit users.db and add data
- Guide to Editing JSON files [here](http://imgur.com/a/Bz4N0)
- Running your JSON file through [JSONLint](http://jsonlint.com/) - Checks it
	
### Streaming:
- [Snip](https://github.com/dlrudie/Snip/releases/tag/v5.0.5) - outputs a text that shows Artist and Songs
 -  Refer here for NowPlaying Guide: https://obsproject.com/forum/threads/now-playing-music-for-spotify-itunes-winamp-on-stream.925/

- If you have subscribers and want your bot to see them you need to connect your twitch account with the bot
 - if you can do that, great! If not watch this: https://www.youtube.com/watch?v=aQ66m7S2L0c
	
	
### Variables:


- Connections
 - CHAN
 - NICK
 - PASS, You have to use [oAuth](http://www.twitchapps.com/tmi/)

- Options:
 - TIMEZONE
 - BANNED_WORDS
 - Music
 - Media -- Title, Social Media, and Shown
 - Broadcast -- Broadcast and Shown
 - Currency -- Minus, Update, and Value

### Full Commands List:

- All:
 - !help - you get the idea
 - !asdf - prints a quote of something
 - !time - displays your pc's time
 - !uptime - Uptime of the stream (from when bot opened and connected)
 - !stats - displays stats of the sender
 - !quote - displays a quote from quotes.txt
 - !coin - displays current currency (if not mod/broadcaster)
  - !run - shows the runs(?)
		
- Mods:
 - !on - test to see if bot running
 - !admin - shows you are mod
 - !runtime - test bot runtime (runs equation) from chat
 - !pong - shows connection lag
 - !conn - test connection to database
 - !quoteadd - saved in quotes.txt
 - !coin - add/sub/set currency
 - !update - updates viewers
 - !runset - sets the display to !run
 - !check <user> - checks for user in database
 - !add <user> - adds user to database
		
- Broadcaster/Editor:
 - !off - turns bot off
 - !broad - turns on broadcast if not on or will run them

### Changelog:

- 1.4.5:
 - Added setup.py and run.py
 - Bot now runs off run.py not init.py
 - Changed the JSON file

- 1.4:
 - Reworked the Code to be more organized
 - Added Follower/Subscriber Data to Database

- 1.3:
  - Fixed Quote System to work better
  - Reworked !coin
  - Removed mods print in beginning
  - Added !run/!runset command

- 1.2:
 - Added Quote System
 - Variables moved to vars.json
 - Redid somethings to run better
 - Added System to ensure channels
	-- Bot must be a mod before it will do anything

- 1.1.4:
 - Added Currency System
 - Added User List
 - Add More Variables
		
- 1.1.3:
 - Added User Variables

		
		
### To Do:

 - Maybe Foobar2000/WinAmp/WMP/Spotify Contoller ( no zune )