[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d18ec4c208743df8101d08d4ce71b82)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=Travisivart/TGA-Bot&utm_campaign=Badge_Grade)

# The Galaxy Aces Discord Bot

## Contents

-   [Linux Install](#linux-install)
-   [Windows Install](#windows-install)
-   -   [Notes for windows users](#notes-for-windows-users)
-   [Using the Bot](#using-the-bot)
-   -   [Discord interface](#discord-interface)
-   -   [CLI interface](#cli-interface)
-   [Configuration](#configuration)
-   -   [Minimum Configuration](#minimum-configuration)
-   -   [Running Multiple Bots](#running-multiple-bots)
-   [Appendix](#appendix)
-   -   [Core bot parameters](#core-bot-parameters)
-   -   [Music Feature](#music-feature)

## Linux Install

```sh
# Clone the repo
git clone git@github.com:Travisivart/TGA-Bot.git && cd TGA-Bot

# install any required dependencies and build the virtual environment
sudo ./build.sh
```

The build script should have created a config.yaml file in the current directory.
Modify your config.yaml with your bot parameters, your bot will need a custom name,
a discord API token, and a command_prefix.
See [Configuration](#configuration) for more details

**See the [Appendix](#appendix) for more details on the config.yaml parameters.**

```sh
# Activate the virtual environment
. venv/bin/activate

# Run the bot
python main.py
```

## Windows Install

If you are planning to use the Music feature then you will need to have ffmpeg available on your system.

If you have chocolately installed you can use it to install ffmpeg:

```powershell
 choco install ffmpeg
```

Otherwise you will need to follow the instructions on the [ffmpeg site](https://ffmpeg.org/) to add ffmpeg to your system.

```powershell
# Clone the repo
git clone git@github.com:Travisivart/TGA-Bot.git; cd TGA-Bot

# Build the virtual environment
.\build.ps1

```

The build script should have created a config.yaml file in the current directory.
Modify your config.yaml with your bot parameters, your bot will need a custom name,
a discord API token, and a command_prefix.
See [Configuration](#configuration) for more details

**See the [Appendix](#appendix) for more details on the config.yaml parameters.**

```powershell
# Activate the virtual environment
.\venv\Scripts\activate

# Run the bot
python main.py
```

### Notes for windows users

Python 3.9 for windows may give you an error such as:

> error Microsoft Visual C++ 14.0 is required

Visit [this link](https://www.scivision.dev/python-windows-visual-c-14-required/) for more details and how to resolve the issue:

## Using the Bot

Once the bot is running you will be able to interact with it in multiple ways.

### Discord interface

Your bot will need to either have permissions to a text-channel in your discord server, or users will have to message the bot directly in order to interact with it. If your bot correctly has access to a text channel, you will should see it listed in the list of online users.

You can send your bot commands by typing: <command prefix> command. For example, if you wanted to play music and your bot's command prefix was !, you would type:

!music play Daft Punk

You can use !help to see the various commands and also use !help command to see the various subcommands under each command.

### CLI interface

The cli interface gives an administrator who is running the bot access to bot controls and commands without needing access to discord. WHen running the bot you will see a prompt like this:

```sh
The Galaxy Aces Bot: >>>
```

You can enter help at the prompt to list all the commands and perform various actions. Entering q or quit will shutdown the bot(s).

## Configuration

### Minimum Configuration

Your config.yaml file will at minimum need:

-   name
-   token
-   command_prefix

Before it is able to run.

### Running Multiple Bots

To run multiple bots on your server simply add additional bot configuration to your config.yaml like so.
Keep in mind that each bot needs to have a unique token.
It is also recommended but not required that each bot have a unique command prefix.

```yaml
- name: The Galaxy Aces Bot
  token: this_bots_token
  command_prefix: "!"
  logging:
    enabled: True
    logging_level: DEBUG
  enabled_features:
    insult:
      enabled: True
      permissions:
        - everyone
    music:
      enabled: True
      permissions:
        - everyone
      local_path: /music
      search_frequency: 300
      audio_types:
        - .flac
        - .mp3
        - .mp4
        - .ogg
        - .wav
        - .wmv
- name: The Galaxy Aces Other Bot
  token: this_other_bots_token
  command_prefix: "."
  logging:
    enabled: True
    logging_level: DEBUG
  enabled_features:
    insult:
      enabled: True
      permissions:
        - everyone
    music:
      enabled: True
      permissions:
        - everyone
      local_path: /music
      search_frequency: 300
      audio_types:
        - .flac
        - .mp3
        - .mp4
        - .ogg
        - .wav
        - .wmv
```

## Appendix

### config.yaml parameter descriptions

#### Core bot parameters

-   **name** - A name for the bot. It can be unique if you want, but is not required. However it will be more difficult to distingush multiple bots if you are running multiple.
-   **token** - A discord developer API token. You can get one [here](https://discord.com/developers/applications)
-   **command_prefix** - A single character which you will use to preface all commands for this bot e.g. !music
-   **logging** - Enable or disable logging for this bot by setting the enabled value to True or False.
-   -   **logging_level** - The level of logging. Possible options: NONE, INFO, WARNING, ERROR, DEBUG

#### Music Feature

-   **local_path** - A system path pointing to a local library of music. Ideally the directory structure will be **local_path/Artists/Albums/songs** But any structure should work. The music feature will search this directory for songs which match the **audio_types** every **search_frequency** seconds.
-   **search_frequency** - How frequently you want the music feature to search for new music. This value is in seconds. Default is 300 seconds (5 minutes)
-   **audio_types** - The different audio formats you want the music feature to search for. These audio types must be readable by ffmpeg.
