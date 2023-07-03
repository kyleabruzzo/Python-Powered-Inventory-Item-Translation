QS-Inventory Items Translation Tutorial
=====================================

Welcome to the QS-Inventory Items Translation tutorial! This tutorial will guide you through the process of using the script to translate your items to multiple languages using google translate api.


Note
-------------
The translation time may change depending on your internet speed.
Please keep in mind that this isn't perfect, so there are chances that you will have to manually translate some stuff, there will be a things_to_manually_do.txt file inside the output folder with the lines that failled to translate.
Also you will have to do a search for " \' " to complete the translation because it will suck, tried my best to add a check for this, guess what, i failled.

Prerequisites
-------------

Before you get started, make sure you have the following dependencies installed on your computer:

1. Python 3.x: If you don't have python installed, you can download it from the official python website (https://www.python.org).

2. `googletrans`, you can install it using `pip`:
pip install googletrans==4.0.0-rc1

Script Usage
------------

1. Open the lang.txt file and choose ur language

2. Open main.py and go to line `79` and edit the language to yours, for example for me will be:
 target_languages = `['it']`

3. Paste you items.lua file where the main.py is located.

4. Open run.bat.

5. The script will display a file selection, use it to select the file that you want to translate, and then click "Open".

6. The script will automatically translate the "label" and "description" fields.

7. Once the translation is complete, you can find the translated file in the translations folder.

8. Congratulations! You have successfully translated your items to your language.

