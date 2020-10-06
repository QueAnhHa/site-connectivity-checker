## site-connectivity-checker
A program to check the connectivity to a specific website.

## CLI Program Version
* `site-connectivity-check.py`: A command line interface program to check a single URL connectivity.
* `site_connectivity_multi_check.py`: A command line interface program to check multiple URLs and send Desktop notifications to users when the sites can be connected. This inlcudes a sqlite3 DB to store URLs and a background process to frequently check connectivity with time intervals specified by the users.
* Run python scripts as CLI program:
    - Put shebang line `#!/usr/bin/env` at top so that the program loader knows which intepreter should execute the scripts.
    - Rename the script with the CLI program name we like. For example: `check-connect`
    - Make sure your program is on the PATH. Not recommended to copy to system directory as may cause conflicts.
      We can create a bin diretory in your user's home directory and add that to the PATH.
    

## Desktop Application Version
This is the Desktop Application version of the single URL connectivity program. User can choose to check the status of an URL and 
also can run the background process to frequently check if the URL cannot be connect at the moment. The program will run in the background and send Desttop notification to user when the site can be reached.
