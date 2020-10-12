[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d18ec4c208743df8101d08d4ce71b82)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=Travisivart/TGA-Bot&utm_campaign=Badge_Grade)

#The Galaxy Aces Discord Bot

## Build the Bot

Run this command from your shell. It will install any needed dependencies and setup a virtual environment.

Linux users:

```sh
./build.sh
```

Windows users from powershell:

```powershell
./build.ps1
```

#### Notes for windows users

Python 3.9 for windows may give you an error such as:

> error Microsoft Visual C++ 14.0 is required

Visit [this link](https://www.scivision.dev/python-windows-visual-c-14-required/) for more details and how to resolve the issue:

## Configuration

The build script should have created a config.yaml file in the current directory.
Modify the file with your bot parameters as such:

```yaml
- bot_id: 1
  bot_name: Your Bot Name
  token: Your Discord API Key
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
```

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
  bot_name: The Galaxy Aces Bot
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
  bot_name: The Galaxy Aces Other Bot
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
