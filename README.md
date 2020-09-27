[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d18ec4c208743df8101d08d4ce71b82)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=Travisivart/TGA-Bot&utm_campaign=Badge_Grade)

## Configuration

Copy the following json to a file named "config.json" to the base directory and substitute your Discord API Token.

```json
{
  "bot_name": "Your Bot Name",
  "token": "Your Discord API Key",
  "logging": {
    "enabled": "True",
    "logging_level": "DEBUG"
  },
  "enabled_features": {
    "insult": {
      "enabled": "True"
    },
    "music": {
      "enabled": "True",
      "localPath": "Local path to music directory"
    }
  }
}
```

## Build the Bot

Run this command from your shell. It will install any needed dependencies and setup a virtual environment.

```sh
./build.sh
```

## Start the Bot

Run this command from your shell:

```sh
python main.py
```
