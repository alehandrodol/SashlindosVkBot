#!/bin/bash

cd /home/alehandrodol/SashlindosVkBot/VkBot/db
alembic upgrade head

cd python_scripts/
python3 refresh_all_seq.py

# Start your bot file
cd ../../
python3 bot.py 
