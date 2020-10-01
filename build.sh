#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    echo Creating Virtual Environment
    virtualenv venv
fi

source venv/bin/activate
pip install -r requirements.txt


# If config.yaml does not exist, generate basic config.yaml
CONFIG="config.yaml"
if [[ ! -f $CONFIG ]]; then
    cat > $CONFIG <<EOF
bots:
  - bot_id: 1
    config: 
      bot_name: 
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
EOF
else
  echo "Your config.yaml already exists, skipping generation of example config.yaml."
fi

