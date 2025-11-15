# 📁 Directorio de Datos

Este directorio contiene los archivos Excel que se utilizan para la búsqueda de información.

## 📋 Archivo Excel Requerido

**Coloca tu archivo Excel aquí:**

- **Nombre del archivo**: `contratos_icetex.xlsx`
- **Formato**: `.xlsx` (Excel formato abierto)
- **Ubicación**: Este mismo directorio (`data/`)

## 📍 Ubicación del archivo:

```
PLATAFORMA PETICIONES AI/
├── main.py
├── data/
│   ├── contratos_icetex.xlsx  ← Coloca tu archivo Excel aquí
│   └── README.md
└── ...
```

## 🔧 Configuración

### Opción 1: Archivo por defecto (Recomendado)
1. Coloca tu archivo Excel en este directorio
2. Nómbralo exactamente: `contratos_icetex.xlsx`
3. El sistema lo cargará automáticamente

### Opción 2: Ruta personalizada
Si tu archivo está en otra ubicación, puedes configurarlo en el archivo `.env`:

**Windows:**
```env
EXCEL_FILE_PATH=C:\Users\TuNombre\Documents\mi_archivo.xlsx
```

**Mac/Linux:**
```env
EXCEL_FILE_PATH=/home/usuario/documentos/mi_archivo.xlsx
```

**Nota:** El sistema funciona en Windows, Mac y Linux. Las rutas se manejan automáticamente según el sistema operativo.

## 📊 Estructura del Excel

El archivo Excel debe tener:
- **Primera fila**: Encabezados de columnas
- **Columnas de búsqueda**: El sistema detectará automáticamente las columnas que contienen:
  - **Nombres**: Columnas con palabras como "nombre", "razón social", "representante legal"
  - **IDs**: Columnas con palabras como "id", "cédula", "documento", "nit"

## ✅ Una vez agregado el archivo:

1. Reinicia el servidor para que cargue el archivo
2. Accede a la página de búsqueda: `http://localhost:8000/search`
3. Busca por nombre o número de identificación

## ⚠️ Notas:

- El archivo se carga en memoria al iniciar el servidor
- Si actualizas el Excel, necesitarás reiniciar el servidor para ver los cambios
- El sistema soporta archivos grandes (miles de filas)
- Asegúrate de que el archivo no esté abierto en Excel cuando el servidor intente leerlo

## 🌐 Para Despliegue (Deployment):

**IMPORTANTE:** Para que el archivo Excel funcione en producción (desde cualquier lugar):

1. **El archivo DEBE estar en el repositorio Git** - No debe estar en `.gitignore`
2. **Comitéa el archivo:**
   ```bash
   git add data/contratos_icetex.xlsx
   git commit -m "Add Excel data file"
   git push
   ```
3. **Al desplegar**, el archivo se incluirá automáticamente en el despliegue
4. **Cualquier usuario** podrá acceder a la búsqueda desde: `https://tu-app.com/search`

El archivo Excel viajará con tu aplicación y funcionará desde cualquier lugar del mundo! 🌍

