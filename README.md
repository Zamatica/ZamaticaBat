


ZamaticaBat

Author: Zamatica

Release: 1.3.0
Releases: https://github.com/Zamatica/ZamaticaBat/releases

TESTED ON WINDOWS ONLY, SORRY OTHER USERS


You Need:
	
	- Python 3.x.x ( https://www.python.org/downloads/ )

You May Want:

	- SQLite3 Browser ( http://sqlitebrowser.org/ ) - Allows you to edit users.db and add data
	- Guide to Editing JSON files ( http://imgur.com/a/Bz4N0 )
	- Running your JSON file through JSONLint ( http://jsonlint.com/ ) - Checks it

MAKE YOUR BOT A MOD BEFORE TRYING TO CONNECT, OTHERWISE IT WILL NOT CONNECT.
	
IT WILL MOST LIKELY SAY, UNABLED TO CONNECT GIVE IT TIME.
	
	
Variables needed to be changed in the JSON file (open with any text edior)

	for connections: <---------------------------------------------- IMPORTANT
		CHAN
		NICK
		PASS ( have to use a oAuth Token, go here: http://twitchapps.com/tmi/ )

	for variables:
		TIMEZONE
		ASDF
		URL ( the ----USERNAME---- part ) <------------------------- IMPORTANT

		BANNED_WORDS
		
		BROADCASTER <----------------------------------------------- IMPORTANT
		USER_MODS   <----------------------------------------------- IMPORTANT
		
		if media is enabled
			TITLE
			SOCIAL_MEDIA

		if broadcast is enabled
			BROADCAST

Full Commands List:

	All:
		!help - you get the idea
		!asdf - prints a quote of something
		!time - displays your pc's time
			= Varible: TIMEZONE, set to your timezone
		!uptime - Uptime of the stream (from when bot opened and connected)
		!stats - displays stats of the sender
		!quote - displays a quote from quotes.txt
		!coin - displays current currency (if not mod/broadcaster)
		!run - shows the runs(?)
		
	Mods:
		!on - test to see if bot running
		!admin - shows you are mod
		!runtime - test bot runtime (runs equation) from chat
		!pong - shows connection lag
		!conn - test connection to database
		!quoteadd - saved in quotes.txt
		!coin - add/sub/set currency
		!update - updates viewers
		!runset - sets the display to !run
		
	Broadcaster/Editor:
		!off - turns bot off
		!broad - turns on broadcast if not on or will run them


Changelog:

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
			= Bot must be a mod before it will do anything

	- 1.1.4:
		- Added Currency System
		- Added User List
		- Add More Variables
		
	- 1.1.3:
		- Added User Variables

		
		
To Do:

	- Maybe Foobar2000/WinAmp/WMP/Spotify Contoller ( no zune )

