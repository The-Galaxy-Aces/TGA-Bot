#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    echo Creating Virtual Environment
    virtualenv -p python3 venv
fi

source venv/bin/activate
pip install -r requirements.txt


# If config.yaml does not exist, generate basic config.yaml
CONFIG="config.yaml"
if [[ ! -f $CONFIG ]]; then
    cat > $CONFIG <<EOF
- bot_id: 1
  name: 
  token: 
  command_prefix: "!"
  logging:
    enabled: "True"
    logging_level: DEBUG
  enabled_features:
    insult:
      enabled: "True"
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
EOF
else
  echo "Your config.yaml already exists, skipping generation of example config.yaml."
fi

