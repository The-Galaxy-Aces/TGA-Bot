[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d18ec4c208743df8101d08d4ce71b82)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=Travisivart/TGA-Bot&utm_campaign=Badge_Grade)

# The Galaxy Aces Discord Bot

## Prepare your system

### Linux:

No special instructions. Skip to [Build the Bot](#build-the-bot)

### Windows:

If you are planning to use the Music feature then you will need to have ffmpeg available on your system.

If you have chocolately installed you can use it to install ffmpeg:

```powershell
 choco install ffmpeg
```

Otherwise you will need to follow the instructions on the [ffmpeg site](https://ffmpeg.org/) to add ffmpeg to your system.

## Build the Bot

Run this command from your shell. It will install any needed dependencies and setup a virtual environment.

Linux users:

**_You will need to run this as sudo to install any system dependencies._**

```sh
sudo ./build.sh
```

Windows users from powershell:

```powershell
.\build.ps1
```

### Notes for windows users

Python 3.9 for windows may give you an error such as:

> error Microsoft Visual C++ 14.0 is required

Visit [this link](https://www.scivision.dev/python-windows-visual-c-14-required/) for more details and how to resolve the issue:

## Configuration

The build script should have created a config.yaml file in the current directory.
Modify your config.yaml with your bot parameters.

At the very least you will need to include:

- name (The internal name for your bot)
- token (Your bot's discord API token)
- command_prefix (A single character which will be used to preface bot commands e.g. !music)

## Start the Bot

Run this command from your shell:

```sh
python main.py
```

## Running Multiple Bots

To run multiple bots on your server simply add additional bot configuration to your config.yaml like so.
Keep in mind that each bot needs to have a unique id and should have a unique token.
It is also recommended but not required that each bot have a unique command prefix.

```yaml
- bot_id: 1
  name: The Galaxy Aces Bot
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
      search_frequency: 10
      audio_types:
        - .flac
        - .mp3
        - .mp4
        - .ogg
        - .wav
        - .wmv
- bot_id: 2
  name: The Galaxy Aces Other Bot
  token: this_other_bots_token
  command_prefix: .
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

#### music feature

- **local_path** - A system path pointing to a local library of music. Ideally the directory structure will be **local_path/Artists/Albums/songs** But any structure should work. The music feature will search this directory for songs which match the **audio_types** every **search_frequency** seconds.
- **search_frequency** - How frequently you want the music feature to search for new music. This value is in seconds. Default is 300 seconds
- **audio_types** - The different audio formats you want the music feature to search for. These audio types must be readable by ffmpeg.
