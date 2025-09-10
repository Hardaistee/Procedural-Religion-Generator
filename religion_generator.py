from typing import Dict, Any, Optional
from models import (
    Religion, Deity, SacredText, Ritual, MoralRule, 
    MythologicalLegend, RewardPunishment, Symbol, DeityType
)
from gemini_client import GeminiClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReligionGenerator:
    """Main religion generator class"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
    
    def generate_religion(
        self, 
        theme: Optional[str] = None,
        culture: Optional[str] = None,
        complexity: str = "medium",
        deity_type: Optional[str] = None,
        language: str = "Turkish"
    ) -> Religion:
        """
        Generates a complete religion system
        
        Args:
            theme: Religion theme (nature, war, wisdom, etc.)
            culture: Cultural influence (ancient, modern, fantasy, etc.)
            complexity: Complexity level (simple, medium, complex)
            deity_type: Deity type (monotheistic, polytheistic, etc.)
            language: Language for religion generation (Turkish, English, Spanish, etc.)
        """
        
        logger.info(f"Generating new religion - Theme: {theme}, Culture: {culture}, Complexity: {complexity}")
        
        try:
            # Get raw data from Gemini
            raw_data = self.gemini_client.generate_religion(theme, culture, complexity, deity_type, language)
            
            # Convert to Pydantic models
            religion = self._convert_to_models(raw_data)
            
            logger.info(f"Successfully generated: {religion.name}")
            return religion
            
        except Exception as e:
            logger.error(f"Religion generation error: {str(e)}")
            raise
    
    def generate_specific_component(
        self, 
        component_type: str, 
        context: str = "",
        existing_religion: Optional[Religion] = None
    ) -> Dict[str, Any]:
        """
        Generates a specific religion component
        
        Args:
            component_type: Component type (deity, ritual, legend, etc.)
            context: Context information
            existing_religion: Existing religion (for consistency)
        """
        
        if existing_religion:
            context += f" Existing religion: {existing_religion.name}. "
            context += f"Core beliefs: {', '.join(existing_religion.core_beliefs)}"
        
        return self.gemini_client.generate_specific_component(component_type, context)
    
    def _convert_to_models(self, raw_data: Dict[str, Any]) -> Religion:
        """Converts raw data to Pydantic models"""
        
        try:
            # Convert deities
            deities = []
            for deity_data in raw_data.get("deities", []):
                deities.append(Deity(**deity_data))
            
            # Convert sacred texts
            sacred_texts = []
            for text_data in raw_data.get("sacred_texts", []):
                sacred_texts.append(SacredText(**text_data))
            
            # Convert rituals
            rituals = []
            for ritual_data in raw_data.get("rituals", []):
                rituals.append(Ritual(**ritual_data))
            
            # Convert moral rules
            moral_rules = []
            for rule_data in raw_data.get("moral_rules", []):
                moral_rules.append(MoralRule(**rule_data))
            
            # Convert legends
            legends = []
            for legend_data in raw_data.get("legends", []):
                legends.append(MythologicalLegend(**legend_data))
            
            # Convert reward-punishment system
            reward_punishment = RewardPunishment(**raw_data.get("reward_punishment", {}))
            
            # Convert symbols
            symbols = []
            for symbol_data in raw_data.get("symbols", []):
                symbols.append(Symbol(**symbol_data))
            
            # Create main religion model
            religion = Religion(
                name=raw_data.get("name", "Unnamed Religion"),
                description=raw_data.get("description", ""),
                deity_type=DeityType(raw_data.get("deity_type", "polytheistic")),
                language=raw_data.get("language", "Turkish"),
                deities=deities,
                sacred_texts=sacred_texts,
                rituals=rituals,
                moral_rules=moral_rules,
                legends=legends,
                reward_punishment=reward_punishment,
                symbols=symbols,
                core_beliefs=raw_data.get("core_beliefs", []),
                practices=raw_data.get("practices", []),
                holy_places=raw_data.get("holy_places", []),
                religious_leaders=raw_data.get("religious_leaders", ""),
                creation_myth=raw_data.get("creation_myth", "")
            )
            
            return religion
            
        except Exception as e:
            logger.error(f"Model conversion error: {str(e)}")
            raise ValueError(f"Data conversion error: {str(e)}")
    
    def generate_religion_variations(
        self, 
        base_theme: str,
        count: int = 3
    ) -> list[Religion]:
        """
        Generates different religion variations from the same theme
        
        Args:
            base_theme: Base theme
            count: Number of religions to generate
        """
        
        variations = []
        cultures = ["antik", "modern", "fantastik", "fütüristik", "tribal"]
        complexities = ["simple", "medium", "complex"]
        
        for i in range(count):
            culture = cultures[i % len(cultures)]
            complexity = complexities[i % len(complexities)]
            
            try:
                religion = self.generate_religion(
                    theme=base_theme,
                    culture=culture,
                    complexity=complexity
                )
                variations.append(religion)
            except Exception as e:
                logger.warning(f"Variation {i+1} could not be generated: {str(e)}")
                continue
        
        return variations
    
    def expand_religion(self, religion: Religion, component_type: str) -> Religion:
        """
        Adds new components to existing religion
        
        Args:
            religion: Existing religion
            component_type: Component type to add
        """
        
        try:
            new_component = self.generate_specific_component(
                component_type, 
                f"Bu din için uygun bir {component_type} üret",
                religion
            )
            
            # Add new component to religion
            if component_type == "deity":
                new_deity = Deity(**new_component)
                religion.deities.append(new_deity)
            elif component_type == "ritual":
                new_ritual = Ritual(**new_component)
                religion.rituals.append(new_ritual)
            elif component_type == "legend":
                new_legend = MythologicalLegend(**new_component)
                religion.legends.append(new_legend)
            
            logger.info(f"New {component_type} added to {religion.name} religion")
            return religion
            
        except Exception as e:
            logger.error(f"Religion expansion error: {str(e)}")
            raise
