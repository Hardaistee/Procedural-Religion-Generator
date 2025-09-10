import os
import google.generativeai as genai
from typing import Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """Gemini 2.5 Flash API client"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_religion(self, theme: str = None, culture: str = None, complexity: str = "medium", deity_type: str = None, language: str = "Turkish") -> Dict[str, Any]:
        """
        Generates a religion
        
        Args:
            theme: Religion theme (nature, war, wisdom, etc.)
            culture: Cultural influence (ancient, modern, fantasy, etc.)
            complexity: Complexity level (simple, medium, complex)
            deity_type: Deity type (monotheistic, polytheistic, pantheistic, animistic)
            language: Language for religion generation (Turkish, English, Spanish, French, German, Italian, Portuguese, Russian, Arabic, Japanese, Chinese)
        """
        
        prompt = self._create_religion_prompt(theme, culture, complexity, deity_type, language)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _create_religion_prompt(self, theme: str, culture: str, complexity: str, deity_type: str, language: str) -> str:
        """Creates prompt for religion generation"""
        
        # Language settings
        language_instructions = self._get_language_instructions(language)
        
        base_prompt = f"""
You are a creative religion designer. Create a detailed religion system according to the following criteria:

Theme: {theme or "general"}
Culture: {culture or "universal"}
Complexity: {complexity}
Deity Type: {deity_type or "polytheistic"}
Language: {language}

{language_instructions}

Please create a religion system in the following JSON format:

{{
    "name": "Religion name",
    "description": "General description of the religion",
    "deity_type": "monotheistic|polytheistic|pantheistic|animistic",
    "language": "{language}",
    "deities": [
        {{
            "name": "Deity name",
            "title": "Title",
            "domain": "Power domain",
            "description": "Description",
            "attributes": ["attribute1", "attribute2"],
            "symbols": ["symbol1", "symbol2"]
        }}
    ],
    "sacred_texts": [
        {{
            "title": "Sacred text name",
            "content": "Content summary",
            "chapters": ["chapter1", "chapter2"],
            "language": "Language",
            "origin_story": "How it was created"
        }}
    ],
    "rituals": [
        {{
            "name": "Ritual name",
            "purpose": "Purpose",
            "frequency": "Frequency",
            "participants": "Participants",
            "steps": ["step1", "step2"],
            "materials_needed": ["material1", "material2"],
            "significance": "Significance"
        }}
    ],
    "moral_rules": [
        {{
            "rule": "Rule",
            "description": "Description",
            "severity": "Light|Medium|Heavy",
            "punishment": "Punishment",
            "reward": "Reward"
        }}
    ],
    "legends": [
        {{
            "title": "Legend name",
            "story": "Story",
            "characters": ["character1", "character2"],
            "moral_lesson": "Moral lesson",
            "cultural_impact": "Cultural impact"
        }}
    ],
    "reward_punishment": {{
        "rewards": ["reward1", "reward2"],
        "punishments": ["punishment1", "punishment2"],
        "afterlife_concept": "Afterlife concept",
        "judgment_criteria": ["criterion1", "criterion2"]
    }},
    "symbols": [
        {{
            "name": "Symbol name",
            "meaning": "Meaning",
            "visual_description": "Visual description",
            "usage_context": "Usage context"
        }}
    ],
    "core_beliefs": ["belief1", "belief2"],
    "practices": ["practice1", "practice2"],
    "holy_places": ["holy place1", "holy place2"],
    "religious_leaders": "Role of religious leaders",
    "creation_myth": "Creation myth"
}}

IMPORTANT: Set the deity_type field to "{deity_type or "polytheistic"}" exactly. Create a deity system that matches this parameter.

- monotheistic: Single deity (example: Christianity, Islam)
- polytheistic: Multiple deities (example: Ancient Greek, Norse mythology)  
- pantheistic: God=Universe (example: Spinoza's philosophy)
- animistic: Everything has a spirit (example: Shamanism, indigenous religions)

Please create a creative and detailed religion system. Fill every section and create a consistent mythology.
"""
        
        return base_prompt
    
    def _get_language_instructions(self, language: str) -> str:
        """Returns language instructions"""
        
        language_map = {
            "Turkish": "TÜM İÇERİĞİ TÜRKÇE OLARAK ÜRET. Din adı, açıklamalar, tanrı isimleri, ritüeller, efsaneler - her şey Türkçe olsun.",
            "English": "GENERATE ALL CONTENT IN ENGLISH. Religion name, descriptions, deity names, rituals, legends - everything should be in English.",
            "Spanish": "GENERA TODO EL CONTENIDO EN ESPAÑOL. Nombre de la religión, descripciones, nombres de deidades, rituales, leyendas - todo debe estar en español.",
            "French": "GÉNÉREZ TOUT LE CONTENU EN FRANÇAIS. Nom de la religion, descriptions, noms des divinités, rituels, légendes - tout doit être en français.",
            "German": "GENERIEREN SIE ALLE INHALTE AUF DEUTSCH. Religionsname, Beschreibungen, Gottheitsnamen, Rituale, Legenden - alles sollte auf Deutsch sein.",
            "Italian": "GENERA TUTTO IL CONTENUTO IN ITALIANO. Nome della religione, descrizioni, nomi delle divinità, rituali, leggende - tutto dovrebbe essere in italiano.",
            "Portuguese": "GERE TODO O CONTEÚDO EM PORTUGUÊS. Nome da religião, descrições, nomes das divindades, rituais, lendas - tudo deve estar em português.",
            "Russian": "СОЗДАЙТЕ ВЕСЬ КОНТЕНТ НА РУССКОМ ЯЗЫКЕ. Название религии, описания, имена божеств, ритуалы, легенды - все должно быть на русском языке.",
            "Arabic": "أنشئ كل المحتوى باللغة العربية. اسم الدين، الأوصاف، أسماء الآلهة، الطقوس، الأساطير - كل شيء يجب أن يكون باللغة العربية.",
            "Japanese": "すべてのコンテンツを日本語で生成してください。宗教名、説明、神々の名前、儀式、伝説 - すべて日本語である必要があります。",
            "Chinese": "用中文生成所有内容。宗教名称、描述、神祇名称、仪式、传说 - 一切都应该是中文。"
        }
        
        return language_map.get(language, language_map["Turkish"])
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parses response from Gemini"""
        try:
            # Find JSON part
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Valid JSON format not found")
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parse error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Response processing error: {str(e)}")
    
    def generate_specific_component(self, component_type: str, context: str = "") -> Dict[str, Any]:
        """
        Generates a specific religion component
        
        Args:
            component_type: Component type (deity, ritual, legend, etc.)
            context: Context information
        """
        
        prompts = {
            "deity": f"""
            Design a creative deity/goddess. {context}
            
            In JSON format:
            {{
                "name": "Deity name",
                "title": "Title", 
                "domain": "Power domain",
                "description": "Description",
                "attributes": ["attribute1", "attribute2"],
                "symbols": ["symbol1", "symbol2"]
            }}
            """,
            
            "ritual": f"""
            Design a detailed religious ritual. {context}
            
            In JSON format:
            {{
                "name": "Ritual name",
                "purpose": "Purpose",
                "frequency": "Frequency", 
                "participants": "Participants",
                "steps": ["step1", "step2"],
                "materials_needed": ["material1", "material2"],
                "significance": "Significance"
            }}
            """,
            
            "legend": f"""
            Write a mythological legend. {context}
            
            In JSON format:
            {{
                "title": "Legend name",
                "story": "Story",
                "characters": ["character1", "character2"],
                "moral_lesson": "Moral lesson",
                "cultural_impact": "Cultural impact"
            }}
            """
        }
        
        if component_type not in prompts:
            raise ValueError(f"Unsupported component type: {component_type}")
        
        try:
            response = self.model.generate_content(prompts[component_type])
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Component generation error: {str(e)}")
