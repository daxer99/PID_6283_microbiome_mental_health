import os

# 1. Solicitar la ruta al usuario
# Puedes pegar la ruta completa entre comillas si tiene espacios, el script la limpiará.
ruta_raiz = "/home/rodrigo/Documents/Microbiome/PID/PRJ"

# Eliminar comillas dobles o simples accidentales al copiar/pegar en Windows/Mac
ruta_raiz = ruta_raiz.strip('"').strip("'")

# 2. Validar que la ruta exista
if not os.path.isdir(ruta_raiz):
    print(f"\nError: La ruta '{ruta_raiz}' no existe o no es un directorio válido.")
    print("Por favor verifica la ruta e intenta de nuevo.")
    exit()

print(f"\nIniciando proceso en: {ruta_raiz}\n")

# 3. Iterar sobre los directorios del 1 al 22
for i in range(1, 23):
    dir_name = str(i)
    ruta_directorio = os.path.join(ruta_raiz, dir_name)

    # Verificar si el subdirectorio específico existe (ej: carpeta "1", "2", etc.)
    if os.path.isdir(ruta_directorio):
        print(f"Procesando directorio: {dir_name}...")

        for filename in os.listdir(ruta_directorio):
            if filename.endswith(".csv"):
                # Separar nombre y extensión
                name, ext = os.path.splitext(filename)

                # Construir nuevo nombre: nombre_original_numero.csv
                new_filename = f"{name}_{i}{ext}"

                # Rutas completas para origen y destino
                old_path = os.path.join(ruta_directorio, filename)
                new_path = os.path.join(ruta_directorio, new_filename)

                try:
                    # Renombrar
                    os.rename(old_path, new_path)
                    print(f"  -> {filename} renombado a {new_filename}")
                except Exception as e:
                    print(f"  -> Error al renombrar {filename}: {e}")
    else:
        print(f"El directorio '{dir_name}' no se encontró en la ruta indicada, se salta...")

print("\n¡Proceso finalizado!")