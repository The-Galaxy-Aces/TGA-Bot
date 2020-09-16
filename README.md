[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d18ec4c208743df8101d08d4ce71b82)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Travisivart/TGA-Bot&amp;utm_campaign=Badge_Grade)

## Configuration
Copy the following json to a file named "config.json" to the base directory and substitute your Discord API Token.

```json
{
"bot_name": "Your Bot Name",
"token": "Your Discord API Key",
"enabled_features": {
"insults": {
"enabled": "True"
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
