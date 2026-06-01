# HernandezCristian_ProyectoIA

**Proyecto de Inteligencia Artificial Integrado**  
Combina **Graph RAG** (Neo4j) + **Vector RAG** (ChromaDB) + **Action Planner** + **Guardrails de Seguridad**

---

## 📁 Estructura del Proyecto

```
HernandezCristian_ProyectoIA/
│
├── data/
│   ├── archivo1_documentos.json      # Documentos en formato JSON
│   ├── archivo2_grafo.csv            # Relaciones del grafo
│   ├── archivo3_acciones.json        # Definición de acciones
│   └── Archivo4_Documentos.pdf       # Documentación adicional
│
├── src/
│   ├── security/
│   │   └── guardrail.py              # 🛡️  Prevención de inyecciones
│   │
│   ├── retrieval/
│   │   ├── vector_rag.py             # 📚 ChromaDB - Búsqueda vectorial
│   │   └── graph_rag.py              # 🕸️  Neo4j - Exploración de grafos
│   │
│   ├── planner/
│   │   └── action_planner.py         # 🎯 Orquestación de acciones
│   │
│   └── mcp_server.py                 # 🚀 Servidor MCP principal
│
├── venv/                             # Entorno virtual (Python 3.10+)
├── requirements.txt                  # Dependencias del proyecto
├── test_data.py                      # 🧪 Script de validación
├── README.md                         # Este archivo
└── informe_proyecto.pdf              # Documentación técnica final
```

## 🚀 Inicio Rápido

### 1️⃣ Requisitos Previos
- Python 3.10+
- pip (gestor de paquetes)
- Git (opcional, para control de versiones)

### 2️⃣ Instalación

```bash
# Clonar o descargar el proyecto
cd HernandezCristian_ProyectoIA

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Verificar Instalación

```bash
# Ejecutar tests de datos
python test_data.py

# Ejecutar servidor MCP
python -m src.mcp_server
```

---

## 📦 Módulos del Proyecto

### 🛡️ **Módulo de Seguridad** (`src/security/guardrail.py`)
**Propósito:** Prevenir inyecciones de prompts y validar entrada del usuario

**Funciones principales:**
- `detect_injection_attempt()` - Detecta patrones sospechosos
- `sanitize_input()` - Limpia entrada de usuario
- `validate_query()` - Valida consultas antes de procesarlas
- `apply_content_filter()` - Filtra contenido sensible en respuestas

**Ejemplo de uso:**
```python
from src.security.guardrail import validate_query

is_valid, msg = validate_query("¿Cuál es la capital de Francia?")
if is_valid:
    print("✅ Consulta aceptada")
else:
    print(f"❌ {msg}")
```

---

### 📚 **Módulo Vector RAG** (`src/retrieval/vector_rag.py`)
**Propósito:** Recuperación de información usando embebidos vectoriales con ChromaDB

**Características:**
- Almacenamiento local de vectores (sin dependencias externas)
- Búsqueda por similitud semántica
- Persistencia automática de datos
- Interfaz simple para añadir y buscar documentos

**Ejemplo de uso:**
```python
from src.retrieval.vector_rag import VectorRAG

rag = VectorRAG()
rag.load_from_json("data/archivo1_documentos.json")
results = rag.search("¿Qué es Graph RAG?", top_k=5)
```

---

### 🕸️ **Módulo Graph RAG** (`src/retrieval/graph_rag.py`)
**Propósito:** Exploración de relaciones en Neo4j Aura

**Características:**
- Conexión a Neo4j Aura (base de datos en la nube)
- Consultas Cypher personalizadas
- Creación de nodos y relaciones
- Exploración de caminos en grafos

**Configuración requerida:**
```env
NEO4J_URI=neo4j+s://xxxxx.neo4jlabs.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_contraseña
```

---

### 🎯 **Módulo Action Planner** (`src/planner/action_planner.py`)
**Propósito:** Orquestar secuencias de acciones para resolver problemas complejos

**Características:**
- Registro de acciones disponibles
- Construcción automática de planes
- Resolución de dependencias
- Optimización de secuencias

**Tipos de acciones:**
- `RETRIEVE` - Recuperar información
- `EXPLORE` - Explorar grafos
- `SYNTHESIZE` - Generar respuestas
- `SEARCH` - Buscar información
- `ANALYZE` - Analizar datos

---

### 🚀 **Servidor MCP Principal** (`src/mcp_server.py`)
**Propósito:** Unificar todos los módulos en un servidor MCP

**Workflow del servidor:**
```
1. Validación de entrada (Guardrails)
   ↓
2. Planificación de acciones
   ↓
3. Recuperación de documentos (Vector RAG)
   ↓
4. Exploración de grafos (Graph RAG - opcional)
   ↓
5. Síntesis de respuesta
   ↓
6. Filtrado de contenido
```

**Ejemplo de uso:**
```python
from src.mcp_server import MCPServer

server = MCPServer()
server.load_data_from_json("data/archivo1_documentos.json")
result = server.process_query("¿Qué es la IA?")
print(result["response"])
```

---

## 🧪 Testing

### Validar Carga de Datos
```bash
python test_data.py
```

Verifica:
✅ Existencia de archivos JSON y CSV  
✅ Correcta lectura de datos  
✅ Formato de datos válido

### Ejecutar Módulos Individuales
```bash
# Probar Guardrails
python -m src.security.guardrail

# Probar Vector RAG
python -m src.retrieval.vector_rag

# Probar Action Planner
python -m src.planner.action_planner

# Probar servidor completo
python -m src.mcp_server
```

---

## 📊 Flujo de Datos

```
Usuario
   ↓
[MCP Server]
   ├─→ [Guardrail] ✓ Validar
   ├─→ [Action Planner] → Generar Plan
   ├─→ [Vector RAG] → Buscar en ChromaDB
   ├─→ [Graph RAG] → Explorar Neo4j
   └─→ [Síntesis] → Generar Respuesta
   ↓
Respuesta Procesada
```

---

## 🔧 Configuración

### Variables de Entorno (`.env`)
```env
# ChromaDB
CHROMA_COLLECTION=documentos
CHROMA_PERSIST_DIR=./chroma_data

# Neo4j Aura (opcional)
NEO4J_URI=neo4j+s://xxxxx.neo4jlabs.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_contraseña

# MCP Server
MCP_HOST=0.0.0.0
MCP_PORT=8000
MAX_RESULTS=5
TEMPERATURE=0.7
```

---

## 📈 Próximos Pasos

- [ ] **Paso 1:** ✅ Estructura y setup completado
- [ ] **Paso 2:** Integración con Claude API
- [ ] **Paso 3:** Despliegue en servidor
- [ ] **Paso 4:** Pruebas de rendimiento
- [ ] **Paso 5:** Documentación final

---

## 📚 Referencias Técnicas

| Tecnología | Propósito | Documentación |
|-----------|----------|---------------|
| **ChromaDB** | Base de datos vectorial | [chromadb.dev](https://chromadb.dev) |
| **Neo4j Aura** | Base de datos gráfica | [neo4j.com/aura](https://neo4j.com/cloud/aura) |
| **MCP** | Protocol Model Context | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| **FastAPI** | Framework web async | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |

---

## 👨‍💻 Autor
**Cristian Hernández**

---

## 📝 Licencia
Este proyecto es de uso educativo.

**Última actualización:** Mayo 30, 2026
