@echo off

echo  Here we go.
echo  Starting processing
start "C:\Program Files (x86)\Python37-32\python.exe" C:\Users\student\Documents\StudentBeamProfile\ImageExample.py
rem echo  Starting viewer
rem start C:\Program Files (x86)\Python37-32\python.exe C:\Users\student\Documents\StudentBeamProfile\ImageViewer.py
echo  Starting acquisition application
start C:\Users\student\Documents\StudentBeamProfile\basler-cls-linac.exe
