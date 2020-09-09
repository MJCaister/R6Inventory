@echo off
echo Installing required packages
@pip install -r requirements.txt
@C:
@cd C:\Python36\Scripts\
@pip install -r S:\16086\R6Inventory\requirements.txt
echo Finished installing any required packages
@python r6inventory.py
@cd C:\Python36\
@python S:\16086\R6Inventory\r6inventory.py
echo Program crashed/quit
pause()