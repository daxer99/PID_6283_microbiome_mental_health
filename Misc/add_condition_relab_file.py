import os
import csv

# === CONFIGURACIÓN ===
# Reemplaza esta ruta con la ruta a tu directorio principal (el que contiene las carpetas del 1 al 24)
directorio_principal = "/home/rodrigo/Documents/Microbiome/PID/PRJ"  # <-- CAMBIA ESTA RUTA

def leer_condiciones_desde_sample(archivo_sample):
    """
    Lee el archivo Sample - N.csv y devuelve un diccionario
    donde la clave es el ID de la muestra y el valor es la condición.
    """
    condiciones = {}
    try:
        with open(archivo_sample, 'r', encoding='utf-8') as f:
            # Leer todas las líneas para manejar mejor las cabeceras
            lineas = f.readlines()

        # La línea 0 y 1 son cabeceras que debemos ignorar.
        # La línea 2 es el comentario de QIIME2, también la ignoramos.
        # Los datos empiezan en la línea 3 (índice 3)
        for linea in lineas[3:]:
            linea = linea.strip()
            if not linea:  # Saltar líneas vacías
                continue
            # El archivo Sample está separado por comas
            partes = linea.split(',')
            if len(partes) >= 4:
                sample_id = partes[0].strip()
                condition = partes[3].strip()
                condiciones[sample_id] = condition
        print(f"  ✅ Condiciones cargadas desde: {archivo_sample}")
    except FileNotFoundError:
        print(f"  ⚠️  Archivo de sample no encontrado: {archivo_sample}. Se omitirá este directorio.")
    except Exception as e:
        print(f"  ❌ Error al leer {archivo_sample}: {e}")
    return condiciones

def agregar_fila_condicion_a_taxa(archivo_taxa_path, condiciones, archivo_sample_nombre):
    """
    Añade una fila 'condicion' al final de un archivo CSV taxonómico.
    El orden de las condiciones debe coincidir con el orden de las columnas de las muestras.
    """
    try:
        # Leer el archivo taxonómico
        with open(archivo_taxa_path, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        if not lineas:
            print(f"  ⚠️  El archivo {archivo_taxa_path} está vacío. No se modificará.")
            return

        # La primera línea contiene los encabezados (incluye los IDs de las muestras)
        encabezados = lineas[0].strip().split(',')
        # El primer elemento de los encabezados es la columna de taxonomía (ej. "d__Bacteria;p__Firmicutes;...")
        # El resto son los IDs de las muestras (SRR...)
        ids_muestras = encabezados[1:]

        # Construir la lista de condiciones en el orden correcto de las columnas
        condiciones_ordenadas = []
        for sample_id in ids_muestras:
            if sample_id in condiciones:
                condiciones_ordenadas.append(condiciones[sample_id])
            else:
                # Si por alguna razón no encontramos la condición, ponemos un valor por defecto o vacío.
                # Esto podría pasar si los IDs en el archivo de taxa no coinciden con los del archivo Sample.
                print(f"  ⚠️  Advertencia: No se encontró condición para la muestra {sample_id} en {archivo_sample_nombre}. Se usará 'Desconocido'.")
                condiciones_ordenadas.append("Desconocido")

        # Crear la nueva línea: 'condicion' + ',' + ','.join(condiciones_ordenadas)
        nueva_linea = "condicion" + "," + ",".join(condiciones_ordenadas) + "\n"

        # Añadir la nueva línea al final del contenido
        lineas.append(nueva_linea)

        # Sobrescribir el archivo original
        with open(archivo_taxa_path, 'w', encoding='utf-8') as f:
            f.writelines(lineas)

        print(f"    ➕ Fila 'condicion' añadida a: {os.path.basename(archivo_taxa_path)}")

    except Exception as e:
        print(f"  ❌ Error al procesar {archivo_taxa_path}: {e}")

def main():
    if not os.path.isdir(directorio_principal):
        print(f"❌ El directorio {directorio_principal} no existe.")
        return

    print(f"Buscando subdirectorios en: {directorio_principal}")

    # Lista de archivos taxonómicos a procesar en cada subdirectorio
    archivos_taxa = [
        "class.csv", "family.csv", "genus.csv",
        "order.csv", "phylum.csv", "species.csv"
    ]

    # Recorrer los directorios del 1 al 24
    for i in range(1, 25):
        subdir_path = os.path.join(directorio_principal, str(i))
        if not os.path.isdir(subdir_path):
            print(f"⚠️  El subdirectorio {subdir_path} no existe. Se omite.")
            continue

        print(f"\n📁 Procesando directorio: {subdir_path}")

        # Construir la ruta al archivo Sample correspondiente
        archivo_sample = os.path.join(subdir_path, f"Samples - {i}.csv")

        # Leer las condiciones del archivo Sample
        condiciones = leer_condiciones_desde_sample(archivo_sample)

        if not condiciones:
            print(f"  ⚠️  No se pudieron cargar condiciones desde {archivo_sample}. Se omite este directorio.")
            continue

        # Procesar cada archivo taxonómico en el subdirectorio actual
        for archivo_taxa in archivos_taxa:
            archivo_taxa_path = os.path.join(subdir_path, archivo_taxa)
            if os.path.exists(archivo_taxa_path):
                agregar_fila_condicion_a_taxa(archivo_taxa_path, condiciones, os.path.basename(archivo_sample))
            else:
                print(f"  ⚠️  Archivo taxonómico no encontrado: {archivo_taxa_path}")

    print("\n🎉 Proceso completado.")

if __name__ == "__main__":
    main()