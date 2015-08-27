

ZamaticaBat
===========

A simple python twitch bot.

Lastest Release: 1.3.0

Tested on Windows

### Dependencies

You Need:
- Python 3.x.x ( https://www.python.org/downloads/ )

You May Want:
- SQLite3 Browser ( http://sqlitebrowser.org/ ) - Allows you to edit users.db and add data
- Guide to Editing JSON files ( http://imgur.com/a/Bz4N0 )
- Running your JSON file through JSONLint ( http://jsonlint.com/ ) - Checks it

Make sure the bot is a mod, it will not connect otherwise.

Features	
--------

### Variables

For connections:
- CHAN
- NICK
- PASS ( have to use a oAuth Token, go here: http://twitchapps.com/tmi/ )

Others:
- TIMEZONE
- URL ( replace "----USERNAME----" with your twitch name )
- BANNED_WORDS
- BROADCASTER
- If media is enabled:
	- TITLE
	- SOCIAL_MEDIA

- If broadcast is enabled:
	- BROADCAST

### Commands List

All:
- !help - you get the idea
- !time - displays your pc's time
- !uptime - Uptime of the stream (from when bot opened and connected)
- !stats - displays stats of the sender
- !quote - displays a quote from quotes.txt
- !coin - displays current currency (if not mod/broadcaster)
- !run - shows the runs(?)
		
Mods:
- !on - test to see if bot running
- !admin - shows you are mod
- !runtime - test bot runtime (runs equation) from chat
- !pong - shows connection lag
- !conn - test connection to database
- !quoteadd - saved in quotes.txt
- !coin - add/sub/set currency
- !update - updates viewers
- !runset - sets the display to !run
		
Broadcaster/Editor:
- !off - turns bot off
- !broad - turns on broadcast if not on or will run them


### Changelog:

1.3:
- Fixed Quote System to work better
- Reworked !coin
- Removed mods print in beginning
- Added !run/!runset command

1.2:
- Added Quote System
- Variables moved to vars.json
- Redid somethings to run better
- Added System to ensure channels aren't spammed

1.1:
- Added Currency System
- Added User List
- Add More Variables
		
1.0.1:
- Added User Variables
		
		
### To Do:
- Music Contoller

Credits
-------
Artificer Mezrus for helping with testing.
Liquid from Sevadus for the base IRC.



Licence
-------
The MIT License (MIT)

Copyright (c) 2015 Noah Sweet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.







