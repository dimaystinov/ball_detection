@echo off
chcp 65001 >nul
echo Установка зависимостей...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Сборка exe...
pyinstaller --onefile --name "HSV_Filter" --clean test_opencv_hsv.py

echo.
echo Готово. exe: dist\HSV_Filter.exe
echo Положите рядом с exe файлы: img.jpg и hsv_filter.json
pause
