# Procedural Religion Generator

Python REST API that generates automatic religion systems using LLM (Gemini 2.5 Flash).

## Features

- **Complete Religion System Generation**: Deities, sacred texts, rituals, moral rules, legends and more
- **Flexible Parameters**: Customizable with theme, culture, complexity level
- **Component-Based Generation**: Generate specific religion components separately
- **Religion Variations**: Create different versions of religions from the same theme
- **Religion Expansion**: Add new components to existing religions
- **REST API**: Modern and fast API with FastAPI

## Installation

### 1. Requirements

```bash
pip install -r requirements.txt
```

### 2. Gemini API Key

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.env` file:
```bash
cp env_example.txt .env
```
3. Add your API key and port number to `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
PORT=8000
```

### 3. Starting the Application

```bash
python main.py
```

The API will run on `http://localhost:8000` by default. You can change the port number using the `PORT` variable in the `.env` file.

## API Usage

### Main Endpoints

#### 1. Generate Religion

**Turkish Polytheistic Religion Example:**
```http
POST /religions/generate
Content-Type: application/json

{
    "theme": "war",
    "culture": "ancient",
    "complexity": "medium",
    "deity_type": "polytheistic",
    "language": "Turkish"
}
```

**English Monotheistic Religion Example:**
```http
POST /religions/generate
Content-Type: application/json

{
    "theme": "wisdom",
    "culture": "modern",
    "complexity": "complex",
    "deity_type": "monotheistic",
    "language": "English"
}
```

**Spanish Animistic Religion Example:**
```http
POST /religions/generate
Content-Type: application/json

{
    "theme": "nature",
    "culture": "tribal",
    "complexity": "simple",
    "deity_type": "animistic",
    "language": "Spanish"
}
```

#### 2. List Religions
```http
GET /religions
```

#### 3. Get Specific Religion
```http
GET /religions/{religion_id}
```

#### 4. Generate Religion Component
```http
POST /components/generate
Content-Type: application/json

{
    "component_type": "deity",
    "context": "war god",
    "religion_id": "religion_1_1234567890"
}
```

#### 5. Religion Variations
```http
POST /religions/variations
Content-Type: application/json

{
    "base_theme": "wisdom",
    "count": 3
}
```

#### 6. Expand Religion
```http
POST /religions/{religion_id}/expand?component_type=ritual
```

### Parameters

#### Religion Generation Parameters
- `theme`: Religion theme (nature, war, wisdom, etc.)
- `culture`: Cultural influence (ancient, modern, fantasy, etc.)
- `complexity`: Complexity level (simple, medium, complex)
- `deity_type`: Deity type (one of the options below)
- `language`: Language for religion generation (one of the supported languages below)

#### Deity Type Options

| Deity Type | Description | Example Religions | Features |
|------------|-------------|-------------------|----------|
| **monotheistic** | Single deity | Christianity, Islam, Judaism | One supreme god, strong hierarchy |
| **polytheistic** | Multiple deities | Ancient Greek, Norse, Hinduism | Multiple gods, different power domains |
| **pantheistic** | Pantheistic | Spinoza philosophy, Taoism | God = Universe, nature-focused |
| **animistic** | Animistic | Shamanism, indigenous religions | Everything has a spirit, nature spirits |

#### Supported Languages

| Language | Code | Description |
|----------|------|-------------|
| **Turkish** | Turkish | Turkish (default) |
| **English** | English | English |
| **Spanish** | Spanish | Spanish |
| **French** | French | French |
| **German** | German | German |
| **Italian** | Italian | Italian |
| **Portuguese** | Portuguese | Portuguese |
| **Russian** | Russian | Russian |
| **Arabic** | Arabic | Arabic |
| **Japanese** | Japanese | Japanese |
| **Chinese** | Chinese | Chinese |

#### Component Types
- `deity`: God/Goddess
- `ritual`: Religious ritual
- `legend`: Mythological legend

## Religion Components

Each generated religion contains the following components:

### Deities
- Name, title, power domain
- Attributes and symbols
- Detailed descriptions

### Sacred Texts
- Title and content
- Chapters and language
- Origin story

### Rituals
- Name and purpose
- Frequency and participants
- Steps and required materials

### Moral Rules
- Rule and description
- Severity level
- Reward and punishment system

### Mythological Legends
- Title and story
- Characters
- Moral lesson and cultural impact

### Reward-Punishment System
- Rewards and punishments
- Afterlife concept
- Judgment criteria

### Symbols
- Name and meaning
- Visual description
- Usage context

## Usage Examples

### Python API Usage

```python
import requests

# Generate Turkish polytheistic war religion
response = requests.post("http://localhost:8000/religions/generate", json={
    "theme": "war",
    "culture": "ancient",
    "complexity": "complex",
    "deity_type": "polytheistic",
    "language": "Turkish"
})

religion_data = response.json()
religion_id = religion_data["id"]
print(f"Generated religion: {religion_data['religion']['name']}")
print(f"Deity type: {religion_data['religion']['deity_type']}")

# Get religion summary
summary = requests.get(f"http://localhost:8000/religions/{religion_id}/summary")
print(summary.json())

# Add new ritual to religion
requests.post(f"http://localhost:8000/religions/{religion_id}/expand?component_type=ritual")
```

**Different Language and Deity Type Examples:**

```python
# English monotheistic wisdom religion
monotheistic_religion = requests.post("http://localhost:8000/religions/generate", json={
    "theme": "wisdom",
    "deity_type": "monotheistic",
    "language": "English"
})

# French animistic nature religion
animistic_religion = requests.post("http://localhost:8000/religions/generate", json={
    "theme": "nature",
    "deity_type": "animistic",
    "language": "French"
})

# Japanese pantheistic universe religion
pantheistic_religion = requests.post("http://localhost:8000/religions/generate", json={
    "theme": "universe",
    "deity_type": "pantheistic",
    "language": "Japanese"
})

# Arabic polytheistic war religion
polytheistic_religion = requests.post("http://localhost:8000/religions/generate", json={
    "theme": "war",
    "deity_type": "polytheistic",
    "language": "Arabic"
})
```

### cURL API Usage

```bash
# Generate Turkish polytheistic religion
curl -X POST "http://localhost:8000/religions/generate" \
     -H "Content-Type: application/json" \
     -d '{"theme": "war", "culture": "modern", "complexity": "medium", "deity_type": "polytheistic", "language": "Turkish"}'

# Generate English monotheistic religion
curl -X POST "http://localhost:8000/religions/generate" \
     -H "Content-Type: application/json" \
     -d '{"theme": "wisdom", "deity_type": "monotheistic", "language": "English"}'

# Generate Spanish animistic religion
curl -X POST "http://localhost:8000/religions/generate" \
     -H "Content-Type: application/json" \
     -d '{"theme": "nature", "deity_type": "animistic", "language": "Spanish"}'

# List religions
curl -X GET "http://localhost:8000/religions"

# Health check
curl -X GET "http://localhost:8000/health"
```

## API Documentation

When the application is running, you can access Swagger UI at:
- http://localhost:8000/docs

## Development

### Project Structure
```
PRG/
├── main.py                 # FastAPI application
├── models.py              # Pydantic models
├── gemini_client.py       # Gemini API client
├── religion_generator.py  # Religion generator service
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variable example
└── README.md             # This file
```

### Adding New Features

1. Add new model to `models.py`
2. Add new prompt to `gemini_client.py`
3. Add new method to `religion_generator.py`
4. Add new endpoint to `main.py`

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## Issue Reporting

You can report issues through GitHub Issues.
