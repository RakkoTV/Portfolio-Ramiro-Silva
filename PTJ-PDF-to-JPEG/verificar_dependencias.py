#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import importlib.util
import subprocess

def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name, package_name=None):
    if package_name is None:
        package_name = module_name
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=== Verificador de Dependencias para PTJ ===\n")
    
    dependencies = [
        {"module": "PyQt5", "package": "PyQt5", "description": "Interfaz gráfica"},
        {"module": "fitz", "package": "PyMuPDF", "description": "Procesamiento de PDF"}
    ]
    
    all_installed = True
    for dep in dependencies:
        is_installed = is_module_installed(dep["module"])
        status = "[INSTALADO]" if is_installed else "[NO INSTALADO]"
        print(f"{status} {dep['package']} - {dep['description']}")
        
        if not is_installed:
            all_installed = False
            print(f"  Intentando instalar {dep['package']}...")
            if install_module(dep["module"], dep["package"]):
                print(f"  ¡{dep['package']} instalado correctamente!")
            else:
                print(f"  Error al instalar {dep['package']}. Intente instalarlo manualmente con:")
                print(f"  pip install {dep['package']}")
    
    print("\n=== Resumen ===")
    if all_installed:
        print("Todas las dependencias están instaladas correctamente.")
        print("Puede ejecutar la aplicación PTJ.py sin problemas.")
    else:
        print("Algunas dependencias no pudieron ser instaladas automáticamente.")
        print("Por favor, instálelas manualmente siguiendo las instrucciones anteriores.")
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()