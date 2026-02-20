import pandas as pd
import os
import glob

# =============================================
# SOLO TIENES QUE CAMBIAR ESTA RUTA
# =============================================
DIRECTORIO = "/home/rodrigo/Documents/Microbiome/PID/All_relab/species/"  # <--- CAMBIA ESTO POR TU RUTA
PATRON = "*.csv"  # Puedes cambiarlo si quieres solo algunos archivos (ej: "phylum*.csv")
ARCHIVO_SALIDA = "/home/rodrigo/Documents/Microbiome/PID/All_relab/species/fusionado.csv"  # Nombre del archivo de salida
# =============================================

print(f"Buscando archivos {PATRON} en: {DIRECTORIO}")

# Buscar archivos
archivos = glob.glob(os.path.join(DIRECTORIO, PATRON))

if not archivos:
    print(f"❌ No se encontraron archivos en {DIRECTORIO}")
    exit()

print(f"✅ Encontrados {len(archivos)} archivos:")
for a in archivos:
    print(f"  - {os.path.basename(a)}")

# Procesar archivos
datos_abundancia = []
condiciones = {}

print("\n📊 Procesando archivos...")
for i, archivo in enumerate(archivos, 1):
    try:
        print(f"  [{i}/{len(archivos)}] {os.path.basename(archivo)}")

        # Leer CSV
        df = pd.read_csv(archivo, index_col=0)

        # Guardar condiciones (última fila)
        for muestra, cond in zip(df.columns, df.iloc[-1].values):
            condiciones[muestra] = cond

        # Agregar datos de abundancia (sin la última fila)
        datos_abundancia.append(df.iloc[:-1])

    except Exception as e:
        print(f"  ⚠ Error: {e}")

# Fusionar todo
print("\n🔄 Fusionando tablas...")
fusionado = pd.concat(datos_abundancia, axis=1, join='outer').fillna(0)

# Ordenar columnas
fusionado = fusionado.reindex(sorted(fusionado.columns), axis=1)

# Agregar condiciones
fusionado.loc['condicion'] = [condiciones.get(m, 'Desconocida') for m in fusionado.columns]

# Guardar
fusionado.to_csv(ARCHIVO_SALIDA)
print(f"\n✅ Archivo guardado: {ARCHIVO_SALIDA}")
print(f"📊 {len(fusionado) - 1} microorganismos, {len(fusionado.columns)} muestras")