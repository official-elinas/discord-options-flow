Step 1. Install python3 on your system to run the bot.
        You may use google to search for instructions or use this 
        article (macOS: https://medium.com/@rajputankit22/install-python3-in-macos-high-sierra-675d58913e6b) to install python3.


Step 2. Create new bot on discord developers website.
        This step is defined well here --> ( https://discordpy.readthedocs.io/en/latest/discord.html#creating-a-bot-account )
        Just follow the instructions to get a bot account .


Step 3. Get bot token.
        This article explains how to get bot token --> (https://www.writebots.com/discord-bot-token/)


Step 4. Add Bot token and channel names to conf.ini file.
        Now add the bot token to conf.ini file.
        Enter the names for channels in the relevent fields.


Step 5. Install required libraries for bot to rrun.
        open command prompt and change directory to folder where you have the 
        files of the bot. Now, make sure there is a file requirements.txt in that 
        directory. Type 'pip3 install -r requirements.txt' without single quotes to install.

Step 6. Download and add selenium to your path.
        This article explains this step very well. --> https://www.kenst.com/2015/03/including-the-chromedriver-location-in-macos-system-path/


Final Step. Run the bot.
        If all the above step went well then you are good to run the bot.
        open command prompt and change the directory to the folder where you have the bot files.
        Type 'python3 discordbot.py' without quotes to run the bot.
        The bot may take 
