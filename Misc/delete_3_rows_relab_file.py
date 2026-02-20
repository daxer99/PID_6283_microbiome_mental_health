import os

# === CONFIGURACIÓN ===
# Reemplaza esta ruta con la ruta a tu directorio principal
directorio_principal = "/home/rodrigo/Documents/Microbiome/PID/PRJ"  # <-- CAMBIA ESTO

def eliminar_ultimas_tres_lineas(archivo_path):
    """
    Lee un archivo y lo reescribe sin las últimas 3 líneas.
    """
    try:
        with open(archivo_path, 'r', encoding='utf-8') as file:
            lineas = file.readlines()

        # Verificar que el archivo tiene al menos 3 líneas
        if len(lineas) <= 3:
            print(f"  ⚠️  El archivo {archivo_path} tiene 3 líneas o menos. No se modificará.")
            return

        # Conservar todas las líneas excepto las últimas 3
        lineas_a_guardar = lineas[:-3]

        # Sobrescribir el archivo original
        with open(archivo_path, 'w', encoding='utf-8') as file:
            file.writelines(lineas_a_guardar)

        print(f"  ✅ Modificado: {archivo_path}")

    except Exception as e:
        print(f"  ❌ Error al procesar {archivo_path}: {e}")

def main():
    if not os.path.isdir(directorio_principal):
        print(f"El directorio {directorio_principal} no existe.")
        return

    print(f"Buscando archivos CSV en: {directorio_principal}")
    archivos_modificados = 0

    # Recorrer todos los subdirectorios y archivos (os.walk es recursivo)
    for raiz, dirs, archivos in os.walk(directorio_principal):
        for archivo in archivos:
            if archivo.endswith(".csv"):
                archivo_path = os.path.join(raiz, archivo)
                print(f"Procesando: {archivo_path}")
                eliminar_ultimas_tres_lineas(archivo_path)
                archivos_modificados += 1

    print(f"\nProceso completado. Se modificaron {archivos_modificados} archivos CSV.")

if __name__ == "__main__":
    main()