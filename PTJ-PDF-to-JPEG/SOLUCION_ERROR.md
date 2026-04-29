# Solución al Error "PC archive entry not found in the TOC"

## Problema
Al ejecutar el archivo PTJ.exe en otro equipo, aparece el error "PC archive entry not found in the TOC". Este error ocurre cuando PyInstaller no puede encontrar correctamente los recursos empaquetados en el ejecutable.

## Causa del problema
El archivo de icono en formato SVG (`icon.svg`) estaba referenciado en el archivo de especificación (`ptj.spec`), pero PyInstaller no puede procesar archivos SVG como iconos para el ejecutable. Esto causaba el error "cannot identify image file" durante la compilación y posteriormente el error "PC archive entry not found in the TOC" al ejecutar en otro equipo.

## Solución implementada
Se ha modificado el archivo `ptj.spec` para resolver el problema con el icono en formato SVG. PyInstaller no puede procesar archivos SVG como iconos para el ejecutable, por lo que se ha comentado la línea del icono en el archivo de especificación.

Cambio realizado:
```python
# Antes
datas=[('icon.svg', '.')],
icon='icon.svg',

# Después
datas=[('icon.svg', '.')],
# icon='icon.svg',  # Comentado porque PyInstaller no puede procesar SVG como iconos
```

Esta solución permite que el ejecutable se compile correctamente sin intentar usar el archivo SVG como icono, lo que evita el error "cannot identify image file".

## Cómo recompilar el ejecutable

1. Se ha creado un archivo batch `recompilar_exe.bat` que puedes ejecutar para recompilar el ejecutable con la configuración actualizada.

2. Simplemente haz doble clic en el archivo `recompilar_exe.bat` y espera a que termine el proceso de compilación.

3. El nuevo ejecutable se generará en la carpeta `dist` y debería funcionar correctamente en otros equipos.

## Notas adicionales

- Si sigues experimentando problemas, asegúrate de que todos los recursos necesarios (como archivos de datos, imágenes, etc.) estén incluidos correctamente en la sección `datas` del archivo `ptj.spec`.

- Para incluir más recursos, puedes agregar más entradas a la lista `datas` siguiendo el formato: `('ruta_al_archivo', 'directorio_destino_relativo')`.

- Si el problema persiste, considera revisar los logs de PyInstaller para obtener más información sobre el error específico.