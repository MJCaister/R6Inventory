@echo off
echo Installing required packages
@pip install -r requirements.txt
echo Finished installing any required packages
@python r6inventory.py
echo Program crashed/quit
pause()