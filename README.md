# spire-class-search
Searches for a class with selenium on Spire

I didn't get CS 250 because my enrollment appointment was a little too late (the last spot closed an hour before!!!) so I made this so I get notified if a spot ever opens up. Pardon the garbage selenium, I've never used this library before, and honestly I hope I never have to use it again

This hasn't been tested for anything other than CS250 but hey it probably works, and until I gotta use it for another class it's not my problem (but actually if you wanna use this and it's not working for some class, feel free to open an issue)

This makes heavy use of the .env file. You also need a twilio account and number to get text alerts. You also need nix to deploy it (or whatever else you feel like using ig). Weirdness in nix-shell is because selenium is currently broken with nix

.env structure:
```bash
USERNAME={spire username}
PASSWORD={spire password}
MAJOR={major to search for}
NUMBER={class number}
SEMESTER={semester (ex. Spring 2023)}

TWILIO_SID={twilio account SID}
TWILIO_AUTH={twilio auth token}
TWILIO_NUM={twilio number}
YOUR_NUM={the number you wanna be notified from, probably your number}
```
