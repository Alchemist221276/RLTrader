..\venv\scripts\pyside6-uic ../ui/MainForm.ui -o ../ui/MainFormUI.py
..\venv\scripts\pyside6-rcc ../ui/resources.qrc > ../ui/resources.py
..\venv\scripts\python update_uires_file.py ..\ui\MainFormUI.py ..\ui\resources.py
pause