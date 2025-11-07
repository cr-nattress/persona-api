# Persona API

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Transform unstructured text into comprehensive, structured persona profiles using AI-powered synthesis.

**Persona API** is a production-ready REST API that automatically generates detailed persona objects from raw text input. Using a two-step LLM pipeline powered by OpenAI, the system normalizes user information and synthesizes it into rich, structured JSON profiles with demographics, professional history, skills, education, and more.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🤖 **AI-Powered Synthesis** - Two-step LLM pipeline (text cleaning + persona population) using OpenAI's gpt-4o-mini
- 📝 **Raw Text Input** - Accept unstructured text of any format or length
- 🔄 **Batch Processing** - Generate multiple personas in sequence with automatic progress tracking
- 🔍 **Search & Query** - Find personas by name, role, keywords, and structured metadata
- 📊 **Export Capabilities** - Export personas in JSON format for integration
- 🔀 **Merge Personas** - Combine information from multiple personas into one
- ⚡ **High Performance** - Async FastAPI backend for concurrent request handling
- 🐳 **Containerized** - Docker and Docker Compose ready for immediate deployment
- 🔐 **Type Safe** - Full Pydantic validation on all inputs/outputs
- 🗄️ **Scalable Database** - PostgreSQL backend via Supabase for multi-cloud deployment
- 📚 **Comprehensive Documentation** - Full API docs, architecture diagrams, data flow visualization

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- OpenAI API key
- Supabase account (or PostgreSQL database)

### Installation

```bash
# Clone repository
git clone https://github.com/cr-nattress/persona-api.git
cd persona-api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key and Supabase credentials
```

### Running the API

**Option 1: Direct Python**

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Option 2: Docker Compose**

```bash
docker-compose up
```

**Option 3: Docker**

```bash
docker build -t persona-api .
docker run -p 8080:8080 --env-file .env persona-api
```

### Verify Installation

Navigate to: http://localhost:8080/docs

You should see the interactive Swagger UI with all available endpoints.

---

## Usage

### Basic Example: Create a Persona

```bash
curl -X POST http://localhost:8080/v1/persona \
  -H "Content-Type: application/json" \
  -d '{
    "raw_text": "John Smith is a Senior Software Engineer at TechCorp with 10 years of experience. He specializes in Python and AWS. Based in San Francisco, CA. Graduated from MIT with a BS in Computer Science."
  }'
```

**Response** (HTTP 201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "John Smith is a Senior Software Engineer...",
  "persona": {
    "meta": {
      "name": "John Smith",
      "role": "Senior Software Engineer",
      "location": "San Francisco, CA"
    },
    "identity": {
      "core_description": "Experienced software engineer specializing in cloud infrastructure and system design..."
    },
    "professional": {
      "title": "Senior Software Engineer",
      "company": "TechCorp",
      "years_experience": 10,
      "expertise": ["Python", "AWS", "System Design"]
    },
    "skills": [
      {"name": "Python", "proficiency": "expert"},
      {"name": "AWS", "proficiency": "expert"},
      {"name": "System Design", "proficiency": "advanced"}
    ],
    "education": [
      {
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "institution": "MIT"
      }
    ],
    "_meta": {
      "raw_text_length": 183,
      "cleaned_text_length": 487,
      "model_used": "gpt-4o-mini"
    }
  },
  "created_at": "2024-11-07T10:30:45.123456",
  "updated_at": "2024-11-07T10:30:45.123456"
}
```

### List All Personas

```bash
curl -X GET "http://localhost:8080/v1/persona?limit=10&offset=0"
```

### Retrieve a Specific Persona

```bash
curl -X GET "http://localhost:8080/v1/persona/550e8400-e29b-41d4-a716-446655440000"
```

### Search Personas

```bash
curl -X GET "http://localhost:8080/v1/persona/search?q=engineer&limit=20"
```

### Batch Generate Personas

```bash
curl -X POST http://localhost:8080/v1/persona/batch \
  -H "Content-Type: application/json" \
  -d '["Profile text 1", "Profile text 2", "Profile text 3"]'
```

### Merge Two Personas

```bash
curl -X POST "http://localhost:8080/v1/persona/merge?persona_id_1=uuid1&persona_id_2=uuid2"
```

### Update a Persona

```bash
curl -X PATCH http://localhost:8080/v1/persona/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "raw_text": "Updated information about John..."
  }'
```

### Delete a Persona

```bash
curl -X DELETE "http://localhost:8080/v1/persona/550e8400-e29b-41d4-a716-446655440000"
```

---

## Architecture

### High-Level Flow

```
HTTP POST Request
    ↓
API Route Handler (Validation)
    ↓
PersonaService (Business Logic)
    ↓
PersonaSynthesizer (Orchestration)
    ↓
LLM Chain (Two-Step Pipeline)
    ├─ Step 1: Clean/Normalize Text (OpenAI)
    └─ Step 2: Generate Persona JSON (OpenAI)
    ↓
PersonaRepository (Data Access)
    ↓
Supabase PostgreSQL (Storage)
    ↓
HTTP 201 Response (Persona Object)
```

### System Components

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **API Routes** | REST endpoint definitions | FastAPI |
| **Service Layer** | Business logic orchestration | Python async |
| **Synthesizer** | LLM generation + persistence coordination | LangChain |
| **LLM Chain** | Two-step AI pipeline | OpenAI API (gpt-4o-mini) |
| **Repository** | Database abstraction layer | Supabase client |
| **Database** | Persistent storage | PostgreSQL |
| **Models** | Request/response validation | Pydantic |

### Project Structure

```
persona-api/
├── app/
│   ├── api/                    # REST endpoints
│   │   └── routes.py          # All /v1/persona endpoints
│   ├── models/                 # Pydantic data models
│   │   └── persona.py         # PersonaCreate, PersonaInDB, PersonaResponse
│   ├── services/               # Business logic layer
│   │   ├── persona_service.py        # High-level orchestration
│   │   ├── persona_synthesizer.py    # LLM + DB coordination
│   │   └── llm_chain.py              # Two-step LLM pipeline
│   ├── repositories/           # Data access layer
│   │   └── persona_repo.py    # Database CRUD operations
│   ├── db/                     # Database configuration
│   │   └── supabase_client.py # Supabase connection
│   ├── core/                   # Core utilities
│   │   ├── config.py          # Settings and environment
│   │   └── logging.py         # Structured logging
│   └── main.py                # FastAPI app initialization
├── prompts/                    # LLM prompt templates
│   ├── step1_clean_system.txt
│   ├── step1_clean_user.txt
│   ├── step2_persona_system.txt
│   └── step2_persona_user.txt
├── sample-data/                # Example personas and test data
├── diagrams/                   # Architecture documentation
│   └── POST_persona_dataflow.md # Complete data flow diagram
├── tests/                      # Comprehensive test suite
├── .github/                    # GitHub configuration
│   └── ABOUT.md               # Repository metadata
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/v1/persona` | Create new persona |
| **GET** | `/v1/persona` | List all personas (paginated) |
| **GET** | `/v1/persona/{id}` | Retrieve persona by ID |
| **PATCH** | `/v1/persona/{id}` | Update persona |
| **DELETE** | `/v1/persona/{id}` | Delete persona |

### Advanced Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/v1/persona/batch` | Batch generate multiple personas |
| **POST** | `/v1/persona/merge` | Merge two personas |
| **GET** | `/v1/persona/search` | Search personas by query |
| **GET** | `/v1/persona/stats` | Get system statistics |
| **GET** | `/v1/persona/export` | Export all personas |

### Documentation

- **Interactive API Docs**: http://localhost:8080/docs (Swagger UI)
- **ReDoc Documentation**: http://localhost:8080/redoc
- **Data Flow Diagram**: [diagrams/POST_persona_dataflow.md](diagrams/POST_persona_dataflow.md)

---

## Use Cases

### 1. HR & Recruitment

Automatically generate candidate profiles from CVs, LinkedIn profiles, and application forms.

```bash
# Convert CV text to structured persona
curl -X POST http://localhost:8080/v1/persona \
  -d '{"raw_text": "[CV content from PDF/text extraction]"}'
```

### 2. Lead Intelligence

Synthesize prospect information from web scraping, social media, and business data.

```bash
# Convert web-scraped prospect data
curl -X POST http://localhost:8080/v1/persona \
  -d '{"raw_text": "[Prospect info from LinkedIn/web]"}'
```

### 3. Content Personalization

Generate user personas for targeted marketing and content experiences.

```bash
# Create personas for audience segmentation
curl -X POST http://localhost:8080/v1/persona/batch \
  -d '["User profile 1", "User profile 2", ...]'
```

### 4. Data Enrichment

Transform raw user data into structured intelligence for analytics.

```bash
# Enrich customer database with structured personas
curl -X POST http://localhost:8080/v1/persona \
  -d '{"raw_text": "[Customer data]"}'
```

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python | 3.11+ |
| **Web Framework** | FastAPI | 0.104+ |
| **ASGI Server** | Uvicorn | Latest |
| **AI/ML** | LangChain | Latest |
| **LLM Provider** | OpenAI API | gpt-4o-mini |
| **Database** | PostgreSQL | 14+ |
| **Database Client** | Supabase | Latest |
| **Validation** | Pydantic | v2 |
| **Containerization** | Docker | Latest |
| **Orchestration** | Docker Compose | Latest |

---

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Supabase Configuration
SUPABASE_URL=https://[project].supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Application Configuration
APP_ENV=development
LOG_LEVEL=INFO
```

### Database Setup

The API requires a PostgreSQL database with a `personas` table:

```sql
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_text TEXT NOT NULL,
    persona JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for search
CREATE INDEX idx_personas_created_at ON personas(created_at DESC);
```

Supabase handles table creation automatically when using the provided schema.

---

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/cr-nattress/persona-api.git
cd persona-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing and development

# Copy environment file
cp .env.example .env
# Edit .env with your credentials
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_persona_service.py

# Run tests in watch mode
pytest-watch
```

### Code Style

```bash
# Format code with Black
black app/ tests/

# Lint with Ruff
ruff check app/ tests/

# Type checking with mypy
mypy app/
```

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit with clear messages
   ```bash
   git commit -m "Add feature description"
   ```

4. **Add tests** for new functionality

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** with a detailed description

### Code Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions and classes
- Write tests for new features
- Update documentation as needed
- Use type hints throughout

---

## Roadmap

Planned improvements for future releases:

- [ ] GraphQL endpoint support
- [ ] Batch import from CSV/JSON files
- [ ] Advanced search with vector embeddings
- [ ] Persona versioning and history tracking
- [ ] Webhook notifications for persona updates
- [ ] Rate limiting and API key authentication
- [ ] Web dashboard for persona management
- [ ] Export to additional formats (CSV, XML)
- [ ] Advanced caching strategies
- [ ] Performance optimization for large batches

---

## Performance

### Benchmarks

- **Single Persona Generation**: 5-15 seconds (dominated by OpenAI API latency)
- **Batch Processing**: ~10 seconds per persona (sequential)
- **Database Query**: <500ms typical
- **Request Validation**: <10ms

### Optimization Tips

- Use batch endpoints for multiple personas to reduce per-request overhead
- Configure appropriate OpenAI rate limits in `.env`
- Monitor database connection pool size in Supabase settings
- Cache frequently accessed personas if needed

---

## Troubleshooting

### Common Issues

**Issue**: `422 Unprocessable Entity` on POST request

**Solution**: Ensure `raw_text` field is present and is a non-empty string.

```bash
# Correct
{"raw_text": "Person description..."}

# Incorrect (missing raw_text)
{"description": "..."}
```

**Issue**: `OpenAI API key invalid` error

**Solution**: Verify your `OPENAI_API_KEY` in `.env` is correct and has sufficient credits.

**Issue**: `Supabase connection refused` error

**Solution**: Check `SUPABASE_URL` and `SUPABASE_KEY` are correct and the database is accessible.

**Issue**: Slow persona generation (>30 seconds)

**Solution**:
- Check OpenAI API status
- Review LLM prompt complexity
- Ensure input text isn't excessively long (>10,000 chars recommended max)

---

## Support

- 💬 **GitHub Discussions**: [Ask questions and share ideas](https://github.com/cr-nattress/persona-api/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/cr-nattress/persona-api/issues)
- 📖 **Documentation**: [Full API Reference](diagrams/POST_persona_dataflow.md)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright © 2024 Chris Nattress

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [OpenAI](https://openai.com/) - Language models
- [Supabase](https://supabase.com/) - PostgreSQL database
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Built with ❤️ using FastAPI, LangChain, and OpenAI**
