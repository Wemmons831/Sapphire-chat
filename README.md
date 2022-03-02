
# Sapphie Chat

A all in one chat-bot for Windows.



## Install

To start you MUST have python 3.6  <br>  <br> 
First clone the github repo

```bash
  git clone https://github.com/Wemmons831/Sapphire-chat.git
```
Then Install the required dependencies

```bash
    pip install -r requirements.txt
```

## Usage
To use simply press control and f1 and speak.  <br> <br>

If you wish to change this hotkey, you can edit line 244 of saphire.py
<br> Sapphire can do the following:
google things, define words, tell weather, do basic math (+ - * /), open videos on youtube, set timers, and open programs
## Known Issues

1. Chipset errors:
    to solve this you must find a version of tensorflow that doesn't use the issued chipset.
2. Not Opening Programs:
    To solve this the program you wish to open must be in the C:/ProgramData/Microsoft/Windows/Start Menu/Programs/ directory
