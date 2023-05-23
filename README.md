# AIDiscordBot
An AI (bard in specific) directly connected to a discord bot.

## Requirements:
In order to use this project you will need 2 libraries, the google bard API and discord.py, you can install these with the following pip commands:
```commandline
pip install --upgrade discord
pip install --upgrade GoogleBard
```
You will also need access to [google's bard AI](https://bard.google.com/) as this requires it.

## How To Use:
After copying the repo locally (and installing the dependencies), you will need to create two extra files, a token.secret file and a bard.secret file.
These files will contain all the secret information for your discord bot and bard api, so keep it secret.

token.secret should have a discord bot token (get one [here](https://discord.com/developers/applications))

bard.secret will need your bard session token, in order to get this you need to go to [bard](https://bard.google.com) and open inspect element.
At the top there will be a tab called "Application" click on it. After that scroll on the left side until you find Cookies and open it up, then click on the one called "__ht<span>tps://</span>bard.google.com__", look for the cookie called "____Secure-1PSID__". You will take the info from that cookie and put it into the bard.secret file.


Once you have done the above, it should work perfectly assuming nothing goes wrong. If you do run into bugs please report them on github.

### Credits:
- [acheong08](https://github.com/acheong08/) for creating the [reverse enginnering of the Bard api](https://github.com/acheong08/Bard) and creating a python package to make this all possible
- The entire discord.py community and [Danny](https://github.com/Rapptz) for making [discord.py](https://github.com/Rapptz/discord.py)
