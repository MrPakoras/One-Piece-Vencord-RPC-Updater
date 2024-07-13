# One Piece Vencord RPC Updater
- This program sets your Discord Rich Presence (RPC) to information regarding the next scheduled One Piece chapter.
- It requires Vencord to set a custom RPC.
- Data is scraped from [claystage.com](https://claystage.com/one-piece-chapter-release-schedule-for-2024), thanks!

![Vencord RPC](https://i.imgur.com/X5Vf36t.png?raw=true "Vencord RPC")

# How to use:
## Set up a Discord Application:
- Visit [https://discord.com/developers/applications](https://discord.com/developers/applications)
- Create a new application
- Copy your `Application ID`

## Set up the Custom RPC plugin
- Install [Vencord](https://vencord.dev/download/)
- Once installed, open Discord and go to `User Settings`
- Under the Vencord section go to `Plugins`
- Search for `CustomRPC` and enable it
- Click the settings icon and paste your Discord Application ID
- Enter an Application Name
- Save and Close

## Set up the Python program
- Under the Vencord section in Discord settings, click `Open Settings Folder`
- Copy the address of the `settings.json` file in the `settings` folder
- Enter the path as the `vencordrpcfile` variable in the Python program
- Run it!
