import pandas as pd
import os
from openpyxl import Workbook

# Directorio base donde están las carpetas 1-22
directorio_base = "/home/rodrigo/Documents/Microbiome/PID/PRJ"  # Cambia esto por la ruta donde están tus carpetas

# Lista de los archivos que queremos procesar
archivos_a_procesar = ['phylum', 'genus', 'species']


def crear_excel_multiple(tipo_archivo):
    """
    Crea un archivo Excel con múltiples hojas, una por cada carpeta (1-22)
    tipo_archivo: string con el nombre del archivo (ej: 'phylum', 'genus', 'species')
    """

    # Nombre del archivo de salida
    nombre_salida = f"{tipo_archivo}_all.xlsx"

    # Crear un nuevo workbook
    wb = Workbook()

    # Eliminar la hoja por defecto que se crea automáticamente
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # Iterar sobre las carpetas del 1 al 22
    for i in range(1, 23):
        try:
            # Construir la ruta del archivo
            ruta_archivo = os.path.join(directorio_base, str(i), f"{tipo_archivo}.csv")

            # Verificar si el archivo existe
            if os.path.exists(ruta_archivo):
                # Leer el archivo CSV
                df = pd.read_csv(ruta_archivo)

                # Crear una nueva hoja con el nombre de la carpeta
                with pd.ExcelWriter(nombre_salida, engine='openpyxl', mode='a' if i > 1 else 'w') as writer:
                    # Si es la primera hoja, creamos el archivo, si no, agregamos al existente
                    if i == 1:
                        df.to_excel(writer, sheet_name=str(i), index=False)
                    else:
                        df.to_excel(writer, sheet_name=str(i), index=False)

                print(f"✓ Procesado: Carpeta {i} - {tipo_archivo}.csv")
            else:
                print(f"✗ No encontrado: Carpeta {i} - {tipo_archivo}.csv")

        except Exception as e:
            print(f"✗ Error en carpeta {i}: {str(e)}")

    print(f"\n✅ Archivo '{nombre_salida}' creado exitosamente!\n")


# Procesar cada tipo de archivo
for tipo in archivos_a_procesar:
    print(f"Procesando archivos {tipo}.csv...")
    crear_excel_multiple(tipo)