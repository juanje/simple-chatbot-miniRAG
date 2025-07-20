# Simple Chatbot - Especificaciones Técnicas

## 📋 Resumen del Proyecto

**Simple Chatbot** es una aplicación de línea de comandos que implementa un chatbot conversacional utilizando LangChain y Ollama. El proyecto está diseñado con fines educativos y para demostrar las mejores prácticas en el desarrollo de aplicaciones Python modernas con LLMs locales.

## 🎯 Objetivos

- **Educativo**: Demostrar la implementación de un chatbot usando tecnologías modernas
- **Modular**: Arquitectura limpia con separación de responsabilidades
- **Fácil de usar**: Interfaz CLI intuitiva con comandos especiales
- **Configurable**: Parámetros ajustables para diferentes casos de uso
- **Robusto**: Manejo de errores y validaciones completas

## 🏗️ Arquitectura

### Estructura del Proyecto

```
simple-chatbot/
├── src/simple_chatbot/
│   ├── __init__.py          # Módulo principal
│   ├── chatbot.py           # Lógica core del chatbot
│   ├── cli.py               # Interfaz de línea de comandos
│   ├── config.py            # Configuración centralizada
│   ├── llm_client.py        # Cliente para Ollama
│   └── memory.py            # Gestión de memoria conversacional
├── tests/                   # Tests unitarios
├── pyproject.toml          # Configuración del proyecto
├── README.md               # Documentación de usuario
└── SPECIFICATIONS.md       # Este archivo
```

### Componentes Principales

#### 1. **SimpleChatbot** (`chatbot.py`)
- **Responsabilidad**: Orquestación de la conversación
- **Funcionalidades**:
  - Gestión del flujo de conversación
  - Integración con memoria y cliente LLM
  - Formateo de prompts
  - Estadísticas de conversación
  - Health checks

#### 2. **CLI Interface** (`cli.py`)
- **Responsabilidad**: Interfaz de usuario
- **Funcionalidades**:
  - Interfaz Rich con paneles y colores
  - Navegación con historial de comandos (↑↓)
  - Comandos especiales con prefijo `/`
  - Atajos de teclado (Ctrl+L para limpiar)
  - Manejo de errores user-friendly

#### 3. **OllamaClient** (`llm_client.py`)
- **Responsabilidad**: Comunicación con Ollama
- **Funcionalidades**:
  - Conexión a Ollama via HTTP
  - Validación de modelos disponibles
  - Configuración de parámetros de generación
  - Manejo de errores de conexión

#### 4. **ConversationMemory** (`memory.py`)
- **Responsabilidad**: Gestión de memoria conversacional
- **Funcionalidades**:
  - Límite configurable de mensajes
  - Formateo para prompts
  - Estadísticas de conversación
  - Reset de historial

#### 5. **ChatbotConfig** (`config.py`)
- **Responsabilidad**: Configuración centralizada
- **Funcionalidades**:
  - Parámetros del modelo (temperatura, max_tokens)
  - URLs de conexión
  - Límites de memoria
  - Prompt del sistema

## 🛠️ Stack Tecnológico

### Core Dependencies
- **Python**: 3.10+ (type hints modernos)
- **LangChain**: Framework para aplicaciones LLM
- **LangChain-Ollama**: Integración específica con Ollama
- **Pydantic**: Validación de datos y configuración

### CLI & UX
- **Rich**: Interfaz de terminal avanzada
- **Click**: Framework para CLI
- **prompt-toolkit**: Input avanzado con historial

### Development Tools
- **uv**: Gestión de dependencias y entornos virtuales
- **ruff**: Linting y formateo de código
- **pytest**: Framework de testing
- **mypy**: Type checking estático

## 📋 Funcionalidades Implementadas

### Funcionalidades Core
- ✅ **Conversación básica**: Chat interactivo con LLMs locales
- ✅ **Memoria conversacional**: Mantiene contexto de la conversación
- ✅ **Configuración flexible**: Múltiples parámetros ajustables
- ✅ **Múltiples modelos**: Soporte para cualquier modelo de Ollama

### Comandos Especiales
- ✅ `/quit`, `/exit`, `/bye`: Terminar conversación
- ✅ `/reset`: Limpiar historial de conversación
- ✅ `/stats`: Mostrar estadísticas de la conversación
- ✅ `/history`: Ver historial completo
- ✅ `/help`: Mostrar ayuda

### Características UX
- ✅ **Interfaz Rica**: Paneles coloreados y formato mejorado
- ✅ **Historial de comandos**: Navegación con ↑↓
- ✅ **Shortcuts**: Ctrl+L para limpiar pantalla
- ✅ **Loading indicators**: Spinners durante procesamiento
- ✅ **Manejo de errores**: Mensajes informativos

### Opciones de CLI
- ✅ `--model`: Selección de modelo Ollama
- ✅ `--temperature`: Control de creatividad (0.0-1.0)
- ✅ `--max-tokens`: Límite de tokens de respuesta
- ✅ `--long-responses`: Modo respuestas largas (4000 tokens)
- ✅ `--ollama-url`: URL personalizada de Ollama
- ✅ `--memory-limit`: Límite de mensajes en memoria
- ✅ `--debug`: Logging detallado

## 🔧 Configuración

### Variables de Entorno
```bash
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama2
TEMPERATURE=0.7
MAX_TOKENS=2000
CONVERSATION_MEMORY_LIMIT=10
```

### Configuración Programática
```python
config = ChatbotConfig(
    ollama_base_url="http://localhost:11434",
    model_name="mistral",
    temperature=0.5,
    max_tokens=3000,
    conversation_memory_limit=15
)
```

## 🚀 Instalación y Uso

### Instalación Local
```bash
# Clonar y entrar al directorio
git clone <repo-url>
cd simple-chatbot

# Instalar dependencias
uv sync

# Verificar instalación
uv run chatbot --help
```

### Instalación Global
```bash
# Opción 1: pipx (recomendado)
pipx install .

# Opción 2: uv tool
uv tool install .
```

### Uso Básico
```bash
# Ejecutar con configuración por defecto
uv run chatbot

# Usar modelo específico
uv run chatbot --model mistral --temperature 0.5

# Modo debug para desarrollo
uv run chatbot --debug
```

## 🧪 Testing

### Estructura de Tests
```
tests/
├── test_chatbot.py     # Tests del componente principal
├── test_config.py      # Tests de configuración
└── test_memory.py      # Tests de memoria conversacional
```

### Ejecutar Tests
```bash
# Tests completos
uv run pytest

# Con coverage
uv run pytest --cov=src/simple_chatbot
```

## 📊 Métricas y Estadísticas

El chatbot proporciona las siguientes métricas:
- **Total messages**: Número total de mensajes intercambiados
- **User messages**: Mensajes del usuario
- **Bot messages**: Respuestas del bot
- **Average message length**: Longitud promedio de mensajes
- **Conversation duration**: Duración de la sesión

## 🔐 Seguridad y Consideraciones

### Seguridad
- **Datos locales**: Todos los datos permanecen en el sistema local
- **Sin telemetría**: No se envían datos a servicios externos
- **Validación de entrada**: Sanitización básica de inputs

### Limitaciones
- **Dependencia de Ollama**: Requiere Ollama ejecutándose localmente
- **Memoria volátil**: El historial se pierde al cerrar la aplicación
- **Sin persistencia**: No hay almacenamiento permanente de conversaciones

## 📈 Posibles Mejoras Futuras

### Funcionalidades
- [ ] **Persistencia**: Guardar conversaciones en base de datos
- [ ] **Múltiples sesiones**: Gestionar varias conversaciones
- [ ] **Export/Import**: Exportar conversaciones a archivos
- [ ] **Configuración por archivo**: Archivos de configuración TOML/YAML
- [ ] **Plugins**: Sistema de extensiones

### Técnicas
- [ ] **Async/await**: Mejorar concurrencia
- [ ] **Streaming**: Respuestas en tiempo real
- [ ] **Rate limiting**: Límites de uso
- [ ] **Metrics**: Métricas avanzadas con Prometheus
- [ ] **Web UI**: Interfaz web opcional

## 🤝 Contribuciones

### Estándares de Código
- **Type hints**: Obligatorios en todas las funciones
- **Docstrings**: Google style para todas las funciones públicas
- **Ruff**: Linting y formateo automático
- **Tests**: Coverage mínimo del 90%

### Process de Desarrollo
1. **Fork** del repositorio
2. **Branch** para nueva funcionalidad
3. **Tests** para cualquier cambio
4. **PR** con descripción detallada

## 📝 Versionado

El proyecto sigue [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nuevas funcionalidades compatible
- **PATCH**: Bug fixes compatibles

**Versión actual**: 0.1.0

---

## 📄 Licencia

Este proyecto está diseñado con fines educativos y de demostración.

**Autor**: Juanje Ojeda (juanje@redhat.com)
**Fecha**: Julio 2025