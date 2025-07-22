# Simple Chatbot con RAG - Especificaciones Técnicas

## Resumen del Proyecto

Este documento describe las especificaciones técnicas de una **extensión RAG (Retrieval-Augmented Generation)** del proyecto [Simple Chatbot](https://github.com/juanje/simple-chatbot). Esta implementación educativa demuestra cómo añadir capacidades de recuperación de conocimiento para mejorar las respuestas del chatbot con contexto relevante.

> **📚 Para especificaciones del chatbot base**, consulta la [documentación del proyecto original](https://github.com/juanje/simple-chatbot). Este documento se enfoca en **detalles técnicos específicos de RAG** e implementación.

## Características de Mejora RAG

### 1. Gestión de Base de Conocimiento
- **Formato de Almacenamiento**: Entradas de conocimiento basadas en JSON
- **Estructura**: Palabras clave, contenido, categorías y metadatos
- **Contenido**: Universo ficticio de Aethelgard para pruebas
- **Búsqueda**: Sistema de recuperación basado en palabras clave

### 2. Sistema de Recuperación
- **Procesamiento de Consultas**: Extracción de palabras clave de la entrada del usuario
- **Puntuación de Relevancia**: Cálculo de relevancia basado en ratios simples
- **Filtrado**: Configuración de umbral mínimo de relevancia
- **Limitación de Resultados**: Número máximo configurable de resultados por consulta

### 3. Aumentación de Contexto
- **Inyección de Prompts**: Añadir conocimiento recuperado al contexto del LLM
- **Control de Formato**: Formateo estructurado del contexto
- **Límites de Contexto**: Marcadores claros para contenido RAG
- **Integración**: Integración fluida con el flujo de conversación

### 4. Extensiones CLI
- **Comandos de Conocimiento**: `/knowledge`, `/search`, `/categories`, `/reload`
- **Controles RAG**: Opciones `--no-rag`, `--knowledge-file`
- **Soporte de Debug**: Logging detallado de operaciones RAG
- **Estadísticas**: Análisis e insights de la base de conocimiento

### 5. Características Educativas
- **Modo Comparación**: Pruebas con/sin RAG
- **Contenido Ficticio**: Elimina conocimiento previo del LLM
- **Atribución Clara**: Marcadores visibles de contexto RAG
- **Framework de Pruebas**: Tests específicos comprensivos de RAG

## Arquitectura Técnica RAG

### Estructura de Componentes Mejorada

```
Simple Chatbot con RAG
├── Capa de Configuración (config.py) [+ configuración RAG]
├── Capa Cliente LLM (llm_client.py) [sin cambios]
├── Gestión de Memoria (memory.py) [sin cambios]
├── Capa de Conocimiento (knowledge_base.py) [NUEVO]
├── Lógica Central (chatbot.py) [+ integración RAG]
└── Capa de Interfaz (cli.py) [+ comandos RAG]
```

### Flujo de Datos RAG

```
Consulta Usuario → Extracción Palabras Clave → Búsqueda Conocimiento → Inyección Contexto → LLM → Respuesta Mejorada
```

### Patrones de Diseño Específicos RAG

1. **Patrón Repository**: Abstracción de acceso a datos de la base de conocimiento
2. **Patrón Strategy**: Diferentes algoritmos de recuperación (extensible)
3. **Patrón Decorator**: Aumentación de contexto alrededor de respuestas base
4. **Método Template**: Ejecución estandarizada del pipeline RAG
5. **Patrón Builder**: Formateo complejo de contexto

## Modelos de Datos RAG

### Modelo de Configuración Mejorado
```python
@dataclass
class ChatbotConfig:
    # Configuración base (sin cambios)
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama2"
    temperature: float = 0.3  # Más determinista para RAG
    max_tokens: int = 2000
    system_prompt: str = "Eres un asistente útil..."
    conversation_memory_limit: int = 10
    
    # Configuración específica RAG
    rag_enabled: bool = True
    knowledge_file: str = "data/knowledge.json"
    rag_max_results: int = 3
    rag_min_relevance: float = 0.1
```

### Modelos de Base de Conocimiento
```python
@dataclass
class KnowledgeEntry:
    keywords: List[str]
    content: str
    category: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RetrievalResult:
    entry_id: str
    content: str
    relevance_score: float
    matched_keywords: List[str]
    category: Optional[str] = None
```

### Esquema JSON de Base de Conocimiento
```json
{
  "entry_id": {
    "keywords": ["palabra1", "palabra2", "..."],
    "content": "Información detallada sobre el tema...",
    "category": "nombre_categoria"
  }
}
```

## Especificaciones API RAG

### Interfaz ChatBot Mejorada

```python
class SimpleChatbot:
    # Métodos base (heredados)
    def __init__(self, config: ChatbotConfig = None)
    def chat(self, user_input: str) -> str
    def reset_conversation(self) -> None
    def is_healthy(self) -> bool
    
    # Métodos mejorados (modificados para RAG)
    def get_conversation_stats(self) -> dict  # + estadísticas RAG
    def get_conversation_history(self, format_for_display: bool = True) -> str
    
    # Nuevos métodos específicos RAG
    def search_knowledge(self, query: str) -> List[RetrievalResult]
    def get_knowledge_stats(self) -> dict
    def get_knowledge_categories(self) -> List[str]
    def reload_knowledge(self) -> bool
    
    # Métodos internos RAG
    def _get_rag_context(self, user_input: str) -> str
    def _format_prompt(self, user_input: str) -> str  # Mejorado con RAG
```

### Interfaz Base de Conocimiento

```python
class SimpleKnowledgeBase:
    def __init__(self, knowledge_file: str | Path, enabled: bool = True)
    def search(self, query: str, max_results: int = 3, min_relevance_score: float = 0.1) -> List[RetrievalResult]
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]
    def get_all_entries(self) -> Dict[str, KnowledgeEntry]
    def get_categories(self) -> List[str]
    def search_by_category(self, category: str) -> List[KnowledgeEntry]
    def format_context(self, results: List[RetrievalResult]) -> str
    def get_stats(self) -> Dict[str, Any]
    def reload(self) -> None
    
    # Métodos internos
    def _extract_keywords(self, query: str) -> Set[str]
    def _load_knowledge(self) -> None
```

## Requisitos de Implementación RAG

### Estructura de Proyecto Mejorada
```
simple-chatbot-miniRAG/
├── src/simple_chatbot/
│   ├── __init__.py
│   ├── config.py           # + configuración RAG
│   ├── llm_client.py       # sin cambios
│   ├── memory.py           # sin cambios
│   ├── chatbot.py          # + integración RAG
│   ├── knowledge_base.py   # NUEVO: Funcionalidad central RAG
│   └── cli.py              # + comandos RAG
├── data/                   # NUEVO: Almacenamiento de conocimiento
│   └── knowledge.json      # NUEVO: Datos universo ficticio
├── tests/
│   ├── test_config.py      # actualizado para RAG
│   ├── test_memory.py      # sin cambios
│   ├── test_chatbot.py     # + tests RAG
│   └── test_knowledge_base.py  # NUEVO: tests específicos RAG
├── pyproject.toml          # versión 0.2.0
└── README.md               # actualizado para RAG
```

### Pipeline de Procesamiento RAG
```python
def pipeline_rag(consulta_usuario: str) -> str:
    # 1. Procesamiento de Consulta
    palabras_clave = extraer_palabras_clave(consulta_usuario)
    
    # 2. Recuperación de Conocimiento
    resultados = base_conocimiento.search(palabras_clave)
    
    # 3. Formateo de Contexto
    contexto = formatear_contexto(resultados)
    
    # 4. Aumentación de Prompt
    prompt_mejorado = inyectar_contexto(contexto, consulta_usuario)
    
    # 5. Generación LLM
    respuesta = llm.generate(prompt_mejorado)
    
    return respuesta
```

### Esquema Universo Aethelgard
```json
{
  "character_aris_thorne": {
    "keywords": ["Aris Thorne", "aris", "thorne", "xenobotánico", "científico"],
    "content": "Dr. Aris Thorne es el xenobotánico líder...",
    "category": "personaje"
  },
  "location_aethelgard": {
    "keywords": ["aethelgard", "planeta", "mundo", "violeta", "xylos"],
    "content": "Aethelgard es un exoplaneta terrestre...",
    "category": "ubicación"
  }
}
```

## Aseguramiento de Calidad RAG

### Estrategia de Pruebas Específicas RAG
- **Tests de Base de Conocimiento**: Carga JSON, funcionalidad de búsqueda, puntuación de relevancia
- **Tests de Recuperación**: Extracción de palabras clave, filtrado de resultados, formateo de contexto
- **Tests de Integración**: Integración del pipeline RAG con chatbot
- **Tests de Comparación**: Verificación de respuestas con/sin RAG
- **Casos Extremos**: Resultados vacíos, consultas malformadas, conocimiento faltante

### Requisitos de Cobertura de Tests
- **Tests de Base de Conocimiento**: 27 casos de prueba
- **Tests de Integración RAG**: 4 casos de prueba
- **Tests de Configuración Actualizados**: Actualizados para configuración RAG
- **Cuenta Total de Tests**: 60 tests (100% pasando)
- **Objetivo de Cobertura**: 100% para componentes RAG

### Métricas de Rendimiento RAG
- **Precisión de Recuperación**: Resultados relevantes para consultas de prueba
- **Mejora de Respuesta**: Mejora medible sobre línea base
- **Cobertura de Palabras Clave**: Coincidencia comprensiva de palabras clave
- **Calidad de Contexto**: Inyección de contexto bien formateada y relevante
- **Impacto de Latencia**: Sobrecarga mínima del procesamiento RAG

### Validación Educativa
- **Contenido Ficticio**: Cero contaminación de conocimiento previo del LLM
- **Atribución Clara**: Contexto RAG claramente visible en respuestas
- **Resultados Reproducibles**: Comportamiento consistente para pruebas
- **Transparencia de Debug**: Detalles observables de operación RAG
- **Objetivos de Aprendizaje**: Comprensión demostrable de conceptos RAG

## Especificaciones de Despliegue RAG

### Gestión de Base de Conocimiento
- **Ubicación de Archivo**: `data/knowledge.json` (configurable)
- **Validación de Formato**: Validación de esquema JSON en carga
- **Actualizaciones de Contenido**: Capacidad de recarga en tiempo de ejecución (comando `/reload`)
- **Control de Versiones**: Seguimiento de cambios en base de conocimiento
- **Estrategia de Respaldo**: Respaldo y recuperación de archivo de conocimiento

### Configuración Específica RAG
```bash
# Requerido para despliegue RAG
export RAG_ENABLED="true"
export RAG_KNOWLEDGE_FILE="data/knowledge.json"

# Ajuste de rendimiento
export RAG_MAX_RESULTS="3"
export RAG_MIN_RELEVANCE="0.1"
# Nota: CHATBOT_TEMPERATURE tiene 0.3 como valor predeterminado para respuestas deterministas
```

### Despliegue Educativo
- **Contenido Ficticio**: Asegurar que la base de conocimiento no contenga información real
- **Scripts de Demo**: Consultas preparadas para demostración
- **Modo Comparación**: Cambio fácil entre modos RAG/no-RAG
- **Salida de Debug**: Operación RAG visible para aprendizaje

## Consideraciones de Seguridad RAG

### Seguridad de Base de Conocimiento
- **Validación de Contenido**: Sanitizar entradas de conocimiento
- **Control de Acceso**: Acceso de solo lectura a archivo de conocimiento
- **Prevención de Inyección**: Escapar caracteres especiales en contenido
- **Integridad de Archivo**: Validar estructura JSON y contenido

### Protección contra Inyección de Prompts
- **Aislamiento de Contexto**: Límites claros alrededor de contenido RAG
- **Filtrado de Contenido**: Remover contenido potencialmente dañino
- **Sanitización de Consultas**: Limpiar consultas de usuario antes de procesamiento
- **Validación de Respuestas**: Monitorear respuestas generadas

### Seguridad Educativa
- **Contenido Ficticio**: Sin información personal o sensible real
- **Ambiente Controlado**: Limitado a escenarios educativos
- **Operación Transparente**: Todas las operaciones RAG visibles para aprendizaje
- **Cambios Reversibles**: Fácil deshabilitar funcionalidad RAG

## Especificaciones de Interfaz de Línea de Comandos

### Nuevos Comandos RAG
```bash
# Comandos de prueba RAG
uv run chatbot --no-rag              # Deshabilitar RAG para comparación
uv run chatbot --debug               # Mostrar proceso de recuperación RAG
uv run chatbot --knowledge-file path # Base de conocimiento personalizada

# Comandos RAG interactivos (dentro del chatbot)
/knowledge                           # Mostrar estadísticas de base de conocimiento
/search <consulta>                   # Búsqueda manual de conocimiento
/categories                          # Listar categorías de conocimiento
/reload                              # Recargar base de conocimiento
```

### Ejemplo de Salida Debug RAG
```
[DEBUG] Extrayendo palabras clave de: "¿Quién es el Dr. Aris Thorne?"
[DEBUG] Palabras clave encontradas: {'quién', 'aris', 'thorne', 'dr'}
[DEBUG] Búsqueda de conocimiento encontró 1 resultados
[DEBUG] Resultado principal: character_aris_thorne (relevancia: 0.29)
[DEBUG] Inyectando contexto RAG en prompt
```

## Integración con Proyecto Original

### Componentes Sin Cambios
- **Cliente LLM**: Compatibilidad completa con implementación original
- **Gestión de Memoria**: Manejo idéntico de historial de conversación
- **Configuración Base**: Todas las configuraciones originales preservadas
- **Manejo de Errores**: Mismos mecanismos de recuperación de errores

### Componentes Mejorados
- **Configuración**: Extendida con configuraciones RAG
- **Chatbot Central**: Integración RAG en formateo de prompts
- **Interfaz CLI**: Comandos y opciones adicionales
- **Suite de Pruebas**: Expandida con tests específicos RAG

### Ruta de Migración
```python
# Uso original (sigue funcionando)
chatbot = SimpleChatbot()
response = chatbot.chat("Hola")

# Nuevo uso RAG
config = ChatbotConfig(rag_enabled=True)
chatbot = SimpleChatbot(config)
response = chatbot.chat("¿Quién es el Dr. Aris Thorne?")
```

## Consideraciones de Rendimiento

### Sobrecarga RAG
- **Extracción de Palabras Clave**: ~1ms por consulta
- **Búsqueda de Conocimiento**: ~5ms para base de conocimiento típica
- **Formateo de Contexto**: ~2ms por resultado
- **Sobrecarga Total RAG**: <10ms de latencia adicional

### Uso de Memoria
- **Base de Conocimiento**: ~50KB para universo Aethelgard
- **Índice de Búsqueda**: Huella de memoria mínima
- **Cache de Contexto**: Opcional para optimización de rendimiento

### Escalabilidad
- **Entradas de Conocimiento**: Probado hasta 100 entradas
- **Consultas Concurrentes**: Diseño de hilo único
- **Límites de Tamaño de Archivo**: Recomendado <1MB para archivo JSON

## Extensiones Futuras

### Mejoras Potenciales
- **Embeddings Vectoriales**: Búsqueda semántica avanzada
- **Múltiples Fuentes de Conocimiento**: Soporte para múltiples archivos
- **Capa de Cache**: Cache en memoria de resultados de búsqueda
- **Actualizaciones en Tiempo Real**: Monitoreo de sistema de archivos para cambios
- **Interfaz Web**: Exploración RAG basada en navegador

### Progresiones Educativas
1. **Actual**: RAG simple basado en palabras clave
2. **Intermedio**: Puntuación TF-IDF
3. **Avanzado**: Búsqueda de similitud vectorial
4. **Experto**: Integración de conocimiento multi-modal