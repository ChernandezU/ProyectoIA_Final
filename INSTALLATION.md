# 📖 Guía de Instalación

## ⚡ Instalación Automática (Recomendado)

La forma más fácil es usar el script de instalación automática:

```bash
python install.py
```

Este script realizará automáticamente:
1. ✅ Crear el entorno virtual
2. ✅ Instalar todas las dependencias
3. ✅ Verificar archivos de datos
4. ✅ Configurar variables de entorno
5. ✅ Ejecutar pruebas

---

## 🛠️ Instalación Manual

Si prefieres hacer la instalación paso a paso:

### Paso 1: Crear Entorno Virtual

```bash
python -m venv venv
```

### Paso 2: Activar Entorno Virtual

**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos.

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará:
- `chromadb` - Base de datos vectorial
- `neo4j` - Conector para Neo4j
- `pydantic` - Validación de datos
- `pandas` - Análisis de datos
- Y más (ver `requirements.txt`)

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env  # En Mac/Linux
copy .env.example .env  # En Windows
```

Edita el archivo `.env` y añade tus credenciales (si usarás Neo4j).

### Paso 5: Validar Instalación

```bash
python test_data.py
```

Deberías ver:

```
============================================================
TEST DATA - Validación de archivos
============================================================

📁 Buscando archivos en: .../data

Archivos encontrados:
  - archivo1_documentos.json
  - archivo2_grafo.csv
  - archivo3_acciones.json

✅ Todas las pruebas pasaron correctamente
```

---

## 🚀 Ejecutar el Servidor

Una vez instalado, ejecuta:

```bash
python run.py
```

O ejecuta módulos individuales:

```bash
# Probar seguridad
python -m src.security.guardrail

# Probar Vector RAG
python -m src.retrieval.vector_rag

# Probar Action Planner
python -m src.planner.action_planner

# Ejecutar servidor completo
python -m src.mcp_server
```

---

## 🔧 Requisitos del Sistema

- **Python:** 3.10 o superior
- **Memoria:** Mínimo 2GB para ChromaDB
- **Espacio:** ~500MB para las dependencias
- **Conexión:** Opcional (solo si usas Neo4j Aura)

---

## ❌ Solución de Problemas

### Error: "No module named 'chromadb'"

```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Python 3.10+ required"

```bash
# Verificar versión de Python
python --version

# Si tienes múltiples versiones, usa:
python3.10 -m venv venv
```

### Error: "Permission denied"

En Mac/Linux, asegúrate de que el script es ejecutable:

```bash
chmod +x install.py
chmod +x run.py
```

### Los archivos de datos no se cargan

Verifica que estén en la carpeta `data/`:

```bash
# Windows
dir data/

# Mac/Linux
ls data/
```

---

## 📚 Próximos Pasos

Una vez instalado:

1. 📖 Lee el [README.md](README.md)
2. 🧪 Explora los módulos individuales
3. 🔌 Integra con Claude MCP
4. 📊 Configura Neo4j Aura (opcional)

---

## 🆘 Ayuda

Si encuentras problemas:

1. Verifica que Python 3.10+ esté instalado
2. Asegúrate de estar en el entorno virtual (`venv`)
3. Revisa los logs en `test_data.py` output
4. Consulta la documentación de cada módulo

---

**Última actualización:** Mayo 30, 2026
