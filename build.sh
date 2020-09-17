#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    echo Creating Virtual Environment
    virtualenv venv
fi

source venv/bin/activate
pip install -r requirements.txt
