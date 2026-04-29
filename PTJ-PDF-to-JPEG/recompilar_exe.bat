@echo off
echo Recompilando ejecutable PTJ con configuracion actualizada...
pyinstaller ptj.spec --clean
echo Compilacion completada. El ejecutable se encuentra en la carpeta dist.
pause