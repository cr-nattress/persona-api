# Persona API - GitHub About Section Configuration

This file contains structured data to populate the GitHub repository "About" section fields.

---

## Description

**Short Description (Character Limit: 120)**

```
AI-powered REST API for generating structured persona profiles from unstructured text using LLM-based synthesis.
```

---

## Website URL

**Optional Website Link**

```
[Add website URL if/when deployed]
```

---

## Topics (Tags)

**Keywords for Repository Discovery**

Select up to 20 topics that describe the project:

### Core Technology Stack
- `python`
- `fastapi`
- `api`
- `rest-api`

### AI & Machine Learning
- `artificial-intelligence`
- `langchain`
- `openai`
- `llm`
- `generative-ai`

### Data & Persistence
- `postgresql`
- `supabase`
- `database`

### Development & Devops
- `docker`
- `backend`
- `microservices`

### Domain-Specific
- `persona-generation`
- `data-synthesis`
- `nlp`

### Recommended Selection (15 topics)
```
python
fastapi
rest-api
openai
langchain
llm
artificial-intelligence
generative-ai
postgresql
supabase
docker
backend
database
data-synthesis
persona-generation
```

---

## Full Description (Markdown)

**Extended Description (Character Limit: ~500 for About section)**

```markdown
# Persona API

Transform unstructured text into comprehensive, structured persona profiles using AI-powered synthesis.

## What It Does

Persona API is a production-ready REST API that automatically generates detailed persona objects from raw text input. Using a two-step LLM pipeline powered by OpenAI, the system normalizes user information and synthesizes it into rich, structured JSON profiles with demographics, professional history, skills, education, and more.

## Key Features

- 🤖 **AI-Powered Synthesis** - Two-step LLM pipeline for intelligent persona generation
- 🔄 **Batch Processing** - Generate multiple personas in sequence
- 🔍 **Search & Filter** - Query personas by name, role, keywords, and metadata
- 📊 **Export Capabilities** - Export personas in JSON format
- 🐳 **Containerized** - Docker-ready deployment configuration
- 🔐 **Type-Safe** - Full Pydantic validation and TypeScript-ready schemas
- ⚡ **FastAPI** - High-performance async REST API
- 🗄️ **Scalable** - PostgreSQL backend via Supabase for multi-cloud deployment

## Use Cases

- **HR & Recruitment** - Auto-generate candidate profiles from CVs and applications
- **Lead Intelligence** - Synthesize prospect information from web scraping and social data
- **Content Personalization** - Generate user personas for targeted experiences
- **Data Enrichment** - Transform raw user data into structured intelligence
- **Analytics** - Create demographic and professional profiles at scale

## Architecture

Multi-layer REST API with service-oriented design:
- **API Routes** - FastAPI endpoints with validation
- **Service Layer** - Business logic orchestration
- **LLM Chain** - Two-step synthesis pipeline (OpenAI gpt-4o-mini)
- **Repository Pattern** - Database abstraction
- **Supabase PostgreSQL** - Persistent storage

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/ML**: LangChain, OpenAI API
- **Database**: PostgreSQL (Supabase)
- **Infrastructure**: Docker, Compose
- **Validation**: Pydantic
- **Logging**: Python logging
```

---

## Visibility & Settings

**Public Repository Settings**

| Setting | Value | Notes |
|---------|-------|-------|
| **Repository Visibility** | `Public` | Open source project |
| **Discussions** | `Enabled` | For community Q&A and feature discussion |
| **Issues** | `Enabled` | Bug reports and feature requests |
| **Pull Requests** | `Enabled` | Community contributions welcome |
| **Sponsorships** | `Optional` | Set if accepting donations |
| **Template Repository** | `No` | Not a template for other projects |

---

## About Section Preview

When properly configured on GitHub, the About section should display:

```
📊 Persona API
AI-powered REST API for generating structured persona profiles from unstructured text using LLM-based synthesis.

🌐 [Website URL - Optional]

🏷️ Topics:
python • fastapi • rest-api • openai • langchain • llm • artificial-intelligence
• generative-ai • postgresql • supabase • docker • backend • database •
data-synthesis • persona-generation

👥 Discussions • 🐛 Issues • 🔀 Pull Requests
```

---

## Setup Instructions

**To populate GitHub's About section:**

1. Navigate to repository **Settings** tab
2. Scroll to **About** section (right side of repo homepage)
3. Click the gear icon to edit
4. Fill in the following fields:

   - **Description**: Copy from "Short Description" above
   - **Website**: Add URL if deployed
   - **Add topics**: Select the 15 recommended topics
   - **Visibility**: Ensure set to Public
   - **Discussions**: Enable checkbox

5. Click **Save changes**

---

## Long-Form Description (For README and Project Pages)

```markdown
# Persona API

Transform unstructured text into comprehensive, structured persona profiles using advanced AI synthesis.

## Overview

Persona API is a production-ready REST API service designed to automatically generate detailed, structured persona objects from unstructured text input. Leveraging a two-step LLM pipeline powered by OpenAI's gpt-4o-mini model, the system intelligently normalizes, cleans, and synthesizes raw user information into rich, actionable persona profiles.

## Problem Solved

**Challenge**: Converting unstructured data (CVs, profiles, notes, web content) into uniform, structured profiles is tedious, error-prone, and time-consuming when done manually.

**Solution**: Persona API automates this process using intelligent text processing and generative AI, transforming dozens of unstructured text sources into consistent, queryable persona objects in seconds.

## Core Capabilities

### Generation
- Accept raw text input of any structure or length
- Two-step LLM processing for optimal quality
- Generate comprehensive persona JSON with demographics, professional history, skills, education
- Automatic UUID generation and timestamping

### Management
- Retrieve personas by ID with full metadata
- List personas with pagination
- Update personas with new information
- Delete personas
- Search by name, role, keywords

### Batch Operations
- Generate multiple personas in sequence
- Merge personas with combined information
- Export all personas to JSON

### Advanced Features
- Request validation and error handling
- Comprehensive logging and monitoring
- Docker containerization
- Multi-cloud deployment (AWS, Azure, GCP via Supabase)

## Architecture Highlights

- **Async-First Design** - Built on FastAPI for high concurrency
- **Service Layer Pattern** - Clean separation of concerns
- **LLM Integration** - LangChain + OpenAI for intelligent synthesis
- **Database Abstraction** - Repository pattern for flexibility
- **Type Safety** - Pydantic models for all inputs/outputs
- **Comprehensive Logging** - Structured logging throughout

## Use Cases

1. **Recruitment & HR**
   - Auto-generate candidate profiles from applications
   - Standardize CV data for comparison
   - Build searchable talent database

2. **Sales & Marketing**
   - Synthesize prospect intelligence from web data
   - Create lead profiles automatically
   - Personalize outreach based on generated insights

3. **Content & Analytics**
   - Build user personas for product development
   - Generate audience segments
   - Create demographic profiles at scale

4. **Data Integration**
   - Transform legacy data into modern formats
   - Normalize data from multiple sources
   - Enrich existing databases

## Quick Start

```bash
# Clone repository
git clone https://github.com/cr-nattress/persona-api.git
cd persona-api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key and Supabase credentials

# Run with Docker
docker-compose up

# Or run directly
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Visit: http://localhost:8080/docs for interactive API documentation

## Example Usage

```bash
curl -X POST http://localhost:8080/v1/persona \
  -H "Content-Type: application/json" \
  -d '{
    "raw_text": "John is a senior engineer at TechCorp with 10 years experience in Python and AWS..."
  }'
```

**Response**: 201 Created with full persona object including generated ID and timestamps

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI + Uvicorn |
| **AI/ML** | LangChain + OpenAI |
| **Database** | PostgreSQL (Supabase) |
| **Validation** | Pydantic |
| **Infrastructure** | Docker + Docker Compose |
| **Logging** | Python logging |

## Project Structure

```
persona-api/
├── app/
│   ├── api/                 # REST endpoint definitions
│   ├── models/              # Pydantic data models
│   ├── services/            # Business logic layer
│   ├── repositories/        # Data access layer
│   ├── db/                  # Database configuration
│   └── core/                # Core utilities (logging, config)
├── prompts/                 # LLM prompt templates
├── sample-data/             # Example personas and test data
├── diagrams/                # Architecture documentation
├── tests/                   # Comprehensive test suite
├── docker-compose.yml       # Container orchestration
└── requirements.txt         # Python dependencies
```

## Documentation

- 📖 [API Documentation](./diagrams/POST_persona_dataflow.md) - Complete data flow
- 🏗️ [Architecture Guide](./diagrams/) - System design and components
- 🚀 [Deployment Guide](./docs/deployment.md) - Production deployment
- 🧪 [Testing Guide](./docs/testing.md) - Test suite and coverage

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/cr-nattress/persona-api.git
cd persona-api
pip install -r requirements.txt
python -m pytest  # Run tests
```

## Roadmap

- [ ] GraphQL endpoint support
- [ ] Batch import from CSV/JSON
- [ ] Advanced search with vector embeddings
- [ ] Persona versioning and history
- [ ] Webhook notifications
- [ ] Rate limiting and API keys
- [ ] Web dashboard for persona management

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

- 💬 [GitHub Discussions](https://github.com/cr-nattress/persona-api/discussions)
- 🐛 [GitHub Issues](https://github.com/cr-nattress/persona-api/issues)
- 📧 [Email Support](mailto:support@example.com)

---

**Built with ❤️ using FastAPI, LangChain, and OpenAI**
```

---

## Additional Metadata

**Keywords for SEO/Discovery**:
```
persona generation, AI, REST API, FastAPI, OpenAI, LangChain, LLM,
data synthesis, structured data, Python, PostgreSQL, Supabase, Docker
```

**Social Links** (if applicable):
```
GitHub: https://github.com/cr-nattress/persona-api
Email: [contact email]
Website: [project website]
```

**Code of Conduct**: Reference [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md) if available

**Security Policy**: Reference [SECURITY.md](.github/SECURITY.md) if available
