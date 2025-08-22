# Claude Education Platform 🤖🎓

Una plataforma educativa impulsada por IA para enseñar programación y conceptos de inteligencia artificial a niños y adolescentes en México.

## 🌟 Características

- **Tutores Especializados**: Tres tutores de IA especializados en diferentes áreas
  - 🤖 **Tutor de Chatbots**: Enseña a crear chatbots inteligentes
  - 🧠 **Tutor de IA**: Entrena modelos de machine learning
  - 💻 **Tutor de Programación**: Python aplicado a IA

- **Metodología Socrática**: Los tutores guían el aprendizaje a través de preguntas
- **Contenido Culturalmente Relevante**: Ejemplos y referencias mexicanas
- **RAG Inteligente**: Sistema de recuperación de información con múltiples fuentes
- **Interfaces Múltiples**: Streamlit y Next.js con Vercel AI SDK
- **Base de Datos Serverless**: Integración con Neon PostgreSQL

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.9+
- Node.js 18+
- API Keys para:
  - Anthropic (Claude)
  - Firecrawl
  - Exa (opcional)
  - Tavily (opcional)
  - Neon Database

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/ScientiaCapital/claude-education-platform.git
cd claude-education-platform
```

2. **Configurar Backend (Python)**
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

3. **Configurar Frontend (Next.js)**
```bash
cd frontend
npm install
cp .env.example .env
# Configurar las mismas API keys en frontend/.env
```

4. **Probar la instalación**
```bash
cd ..
python test_sdks.py
```

### Configuración de API Keys

Crea un archivo `.env` en la raíz del proyecto:

```env
# APIs Principales
ANTHROPIC_API_KEY=tu_clave_anthropic_aqui
FIRECRAWL_API_KEY=tu_clave_firecrawl_aqui

# APIs Opcionales (para funcionalidad completa)
EXA_API_KEY=tu_clave_exa_aqui
TAVILY_API_KEY=tu_clave_tavily_aqui

# Base de Datos Neon
DATABASE_URL=postgresql://usuario:password@ep-ejemplo.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## 🎯 Uso

### Opción 1: Interfaz Streamlit (Recomendada para desarrollo)

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar aplicación Streamlit
streamlit run src/ui/app.py
```

Visita: http://localhost:8501

### Opción 2: Interfaz Next.js + API FastAPI

```bash
# Terminal 1: Ejecutar API Backend
source venv/bin/activate
python api_server.py

# Terminal 2: Ejecutar Frontend
cd frontend
npm run dev
```

Visita: http://localhost:3000

### Opción 3: Demo y Pruebas

```bash
# Ejecutar demo rápido
python examples/quick_start.py

# Ejecutar pruebas
python -m pytest tests/ -v
```

## 🏗️ Arquitectura

```
claude-education-platform/
├── src/
│   ├── agents/          # Tutores educativos especializados
│   ├── tools/           # Integraciones de APIs (Firecrawl, Exa, Tavily)
│   ├── rag/             # Sistema RAG y base de conocimientos
│   └── ui/              # Interfaz Streamlit
├── frontend/            # Aplicación Next.js con Vercel AI SDK
├── config/              # Configuración y settings
├── data/                # Datos y currículum
├── examples/            # Scripts de ejemplo
└── tests/               # Pruebas automatizadas
```

## 🔧 Tecnologías

**Backend:**
- Python 3.9+
- FastAPI
- LangChain + Anthropic
- ChromaDB (vectores)
- SQLAlchemy + Neon PostgreSQL
- Streamlit

**Frontend:**
- Next.js 14
- TypeScript
- Vercel AI SDK
- Tailwind CSS
- Framer Motion

**APIs Integradas:**
- Anthropic Claude
- Firecrawl (web scraping)
- Exa (búsqueda semántica)
- Tavily (investigación)

## 📚 Currículum Incluido

El sistema incluye lecciones predefinidas:

- **Fundamentos de Chatbots** (10-16 años, 60 min)
- **Entrenar tu Primer Modelo** (12-16 años, 90 min)
- **Python para IA** (10-16 años, 75 min)
- **Chatbots Inteligentes** (14-18 años, 120 min)
- **Ciencia de Datos para Niños** (12-16 años, 90 min)

## 🚀 Despliegue

### Vercel (Frontend)

```bash
# Conectar con Vercel
vercel login
vercel --cwd frontend

# O usar el botón de deploy:
```

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ScientiaCapital/claude-education-platform)

### Backend (Railway/Heroku/DigitalOcean)

El backend FastAPI puede desplegarse en cualquier plataforma que soporte Python.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [Anthropic](https://anthropic.com) por Claude
- [Vercel](https://vercel.com) por el AI SDK
- [Neon](https://neon.com) por la base de datos serverless
- [Firecrawl](https://firecrawl.dev) por web scraping
- Comunidad educativa de México 🇲🇽

## 📞 Soporte

- 📧 Email: support@scientiacapital.mx
- 🐙 Issues: [GitHub Issues](https://github.com/ScientiaCapital/claude-education-platform/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ScientiaCapital/claude-education-platform/discussions)

---

Hecho con ❤️ en México para la educación del futuro