# 🎨 Cómo Agregar el Logo de ICETEX

## 📍 Ubicación del Logo

Coloca tu archivo de logo en la siguiente carpeta:

```
/Users/axel/Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI/static/images/
```

## 📝 Instrucciones Paso a Paso

### 1. **Prepara tu logo**
   - Formato: PNG (preferiblemente con fondo transparente)
   - Nombre del archivo: `icetex.png` (exactamente así)
   - Dimensiones recomendadas: 400-800px de ancho

### 2. **Copia el archivo**
   
   **Opción A - Desde Finder:**
   - Abre Finder
   - Navega a: `Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI/static/images/`
   - Arrastra y suelta tu archivo `icetex.png` ahí
   
   **Opción B - Desde Terminal:**
   ```bash
   cp /ruta/a/tu/logo/icetex.png "/Users/axel/Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI/static/images/icetex.png"
   ```

### 3. **Verifica el archivo**
   ```bash
   ls -lh "/Users/axel/Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI/static/images/"
   ```
   
   Deberías ver `icetex.png` listado.

### 4. **Reinicia el servidor (si está corriendo)**
   - El servidor puede seguir corriendo
   - Solo actualiza tu navegador: **Ctrl+F5** (Windows) o **Cmd+Shift+R** (Mac)

### 5. **Verifica en el navegador**
   - Abre: http://localhost:8000
   - Deberías ver el logo de ICETEX en la parte superior
   - Si ves un icono roto, verifica que el archivo se llame exactamente `icetex.png`

---

## ✅ Estructura de Carpetas

```
PLATAFORMA PETICIONES AI/
├── static/
│   └── images/
│       ├── icetex.png     ← Tu logo aquí
│       └── README.md
├── templates/
├── utils/
├── main.py
└── ...
```

---

## 🔧 Solución de Problemas

### El logo no aparece:
1. ✅ Verifica que el archivo se llame exactamente `icetex.png` (minúsculas)
2. ✅ Asegúrate de que esté en la carpeta `static/images/`
3. ✅ Limpia la caché del navegador (Ctrl+Shift+Delete)
4. ✅ Verifica que el archivo no esté corrupto (ábrelo en Vista Previa)

### Error 404 en la consola:
- Abre las herramientas de desarrollador (F12)
- Si ves "404 /static/images/icetex.png", el archivo no existe o está mal ubicado
- Verifica la ruta completa del archivo

---

## 📐 Especificaciones del Logo

### Tamaño en la Plataforma:
- El logo se mostrará con un ancho máximo de **180px**
- La altura se ajustará automáticamente manteniendo la proporción

### Formato Recomendado:
- **PNG**: Fondo transparente para mejor integración
- **SVG**: También funciona (cambia la extensión en el código)
- **JPG**: Funciona, pero sin transparencia

---

## 🎯 El Logo Aparecerá En:

- ✅ Página principal de clasificación (`/`)
- ✅ Panel de administración (`/admin`)

---

**¿Necesitas ayuda?** El logo reemplazará el emoji actual (📄 y 🧠) en ambas páginas.

