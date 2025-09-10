# Frontend API Documentation

## Religion Generation Endpoint

### POST /religions/generate

Generates a complete religion system with all components.

#### Request

**URL:** `http://localhost:8000/religions/generate`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body

```json
{
    "theme": "string (optional)",
    "culture": "string (optional)", 
    "complexity": "string (optional)",
    "deity_type": "string (optional)",
    "language": "string (optional)"
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `theme` | string | No | - | Religion theme (e.g., "war", "nature", "wisdom") |
| `culture` | string | No | - | Cultural influence (e.g., "ancient", "modern", "fantasy") |
| `complexity` | string | No | "medium" | Complexity level: "simple", "medium", "complex" |
| `deity_type` | string | No | - | Deity type: "monotheistic", "polytheistic", "pantheistic", "animistic" |
| `language` | string | No | "Turkish" | Language: "Turkish", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Arabic", "Japanese", "Chinese" |

#### Example Requests

**Simple English Religion:**
```json
{
    "theme": "nature",
    "deity_type": "animistic",
    "language": "English"
}
```

**Complex Turkish War Religion:**
```json
{
    "theme": "war",
    "culture": "ancient",
    "complexity": "complex",
    "deity_type": "polytheistic",
    "language": "Turkish"
}
```

#### Response

**Status Code:** `200 OK`

```json
{
    "id": "religion_1_1757526854",
    "religion": {
        "name": "Religion Name",
        "description": "Religion description...",
        "deity_type": "polytheistic",
        "language": "English",
        "deities": [
            {
                "name": "Deity Name",
                "title": "Deity Title",
                "domain": "Power Domain",
                "description": "Deity description...",
                "attributes": ["attribute1", "attribute2"],
                "symbols": ["symbol1", "symbol2"]
            }
        ],
        "sacred_texts": [
            {
                "title": "Sacred Text Title",
                "content": "Text content...",
                "chapters": ["chapter1", "chapter2"],
                "language": "Ancient Language",
                "origin_story": "How it was created..."
            }
        ],
        "rituals": [
            {
                "name": "Ritual Name",
                "purpose": "Ritual purpose...",
                "frequency": "How often performed",
                "participants": "Who participates",
                "steps": ["step1", "step2"],
                "materials_needed": ["material1", "material2"],
                "significance": "Why it's important"
            }
        ],
        "moral_rules": [
            {
                "rule": "Rule text",
                "description": "Rule description...",
                "severity": "Light|Medium|Heavy",
                "punishment": "Punishment for breaking",
                "reward": "Reward for following"
            }
        ],
        "legends": [
            {
                "title": "Legend Title",
                "story": "Legend story...",
                "characters": ["character1", "character2"],
                "moral_lesson": "What it teaches",
                "cultural_impact": "Cultural significance"
            }
        ],
        "reward_punishment": {
            "rewards": ["reward1", "reward2"],
            "punishments": ["punishment1", "punishment2"],
            "afterlife_concept": "What happens after death",
            "judgment_criteria": ["criterion1", "criterion2"]
        },
        "symbols": [
            {
                "name": "Symbol Name",
                "meaning": "What it represents",
                "visual_description": "How it looks",
                "usage_context": "When it's used"
            }
        ],
        "core_beliefs": ["belief1", "belief2"],
        "practices": ["practice1", "practice2"],
        "holy_places": ["place1", "place2"],
        "religious_leaders": "Role of religious leaders",
        "creation_myth": "How the world was created"
    },
    "created_at": "2025-01-10T20:54:14.862231",
    "generation_time": 23.204891
}
```

#### Error Response

**Status Code:** `500 Internal Server Error`

```json
{
    "detail": "Error message describing what went wrong"
}
```

## Frontend Implementation Examples

### JavaScript/Fetch

```javascript
async function generateReligion(parameters) {
    try {
        const response = await fetch('http://localhost:8000/religions/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parameters)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error generating religion:', error);
        throw error;
    }
}

// Usage
const religion = await generateReligion({
    theme: "nature",
    deity_type: "animistic",
    language: "English"
});

console.log(religion.religion.name);
```

### React Hook

```javascript
import { useState } from 'react';

function useReligionGenerator() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const generateReligion = async (parameters) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('http://localhost:8000/religions/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(parameters)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            setLoading(false);
            return data;
        } catch (err) {
            setError(err.message);
            setLoading(false);
            throw err;
        }
    };
    
    return { generateReligion, loading, error };
}
```

### Vue.js Composition API

```javascript
import { ref } from 'vue';

export function useReligionGenerator() {
    const loading = ref(false);
    const error = ref(null);
    
    const generateReligion = async (parameters) => {
        loading.value = true;
        error.value = null;
        
        try {
            const response = await fetch('http://localhost:8000/religions/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(parameters)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            loading.value = false;
            return data;
        } catch (err) {
            error.value = err.message;
            loading.value = false;
            throw err;
        }
    };
    
    return { generateReligion, loading, error };
}
```

## Notes

- **Generation Time**: Usually takes 15-30 seconds depending on complexity
- **Rate Limiting**: No rate limiting implemented (be reasonable)
- **CORS**: Enabled for all origins (`*`)
- **Error Handling**: Always check response status and handle errors gracefully
- **Loading States**: Show loading indicators during generation
- **Data Structure**: The `religion` object contains all generated content
- **ID**: Each generated religion gets a unique ID for future reference
