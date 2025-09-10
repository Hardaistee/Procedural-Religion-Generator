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
    """Din üretici ana sınıfı"""
    
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
        Tam bir din sistemi üretir
        
        Args:
            theme: Din teması (doğa, savaş, bilgelik, vb.)
            culture: Kültürel etki (antik, modern, fantastik, vb.)
            complexity: Karmaşıklık seviyesi (simple, medium, complex)
            deity_type: Tanrı türü (monotheistic, polytheistic, vb.)
            language: Din üretilecek dil (Turkish, English, Spanish, vb.)
        """
        
        logger.info(f"Yeni din üretiliyor - Tema: {theme}, Kültür: {culture}, Karmaşıklık: {complexity}")
        
        try:
            # Gemini'den ham veri al
            raw_data = self.gemini_client.generate_religion(theme, culture, complexity, deity_type, language)
            
            # Pydantic modellerine dönüştür
            religion = self._convert_to_models(raw_data)
            
            logger.info(f"Başarıyla üretildi: {religion.name}")
            return religion
            
        except Exception as e:
            logger.error(f"Din üretim hatası: {str(e)}")
            raise
    
    def generate_specific_component(
        self, 
        component_type: str, 
        context: str = "",
        existing_religion: Optional[Religion] = None
    ) -> Dict[str, Any]:
        """
        Belirli bir din bileşeni üretir
        
        Args:
            component_type: Bileşen türü (deity, ritual, legend, vb.)
            context: Bağlam bilgisi
            existing_religion: Mevcut din (tutarlılık için)
        """
        
        if existing_religion:
            context += f" Mevcut din: {existing_religion.name}. "
            context += f"Temel inançlar: {', '.join(existing_religion.core_beliefs)}"
        
        return self.gemini_client.generate_specific_component(component_type, context)
    
    def _convert_to_models(self, raw_data: Dict[str, Any]) -> Religion:
        """Ham veriyi Pydantic modellerine dönüştürür"""
        
        try:
            # Tanrıları dönüştür
            deities = []
            for deity_data in raw_data.get("deities", []):
                deities.append(Deity(**deity_data))
            
            # Kutsal metinleri dönüştür
            sacred_texts = []
            for text_data in raw_data.get("sacred_texts", []):
                sacred_texts.append(SacredText(**text_data))
            
            # Ritüelleri dönüştür
            rituals = []
            for ritual_data in raw_data.get("rituals", []):
                rituals.append(Ritual(**ritual_data))
            
            # Ahlaki kuralları dönüştür
            moral_rules = []
            for rule_data in raw_data.get("moral_rules", []):
                moral_rules.append(MoralRule(**rule_data))
            
            # Efsaneleri dönüştür
            legends = []
            for legend_data in raw_data.get("legends", []):
                legends.append(MythologicalLegend(**legend_data))
            
            # Ödül-ceza sistemini dönüştür
            reward_punishment = RewardPunishment(**raw_data.get("reward_punishment", {}))
            
            # Sembolleri dönüştür
            symbols = []
            for symbol_data in raw_data.get("symbols", []):
                symbols.append(Symbol(**symbol_data))
            
            # Ana din modelini oluştur
            religion = Religion(
                name=raw_data.get("name", "İsimsiz Din"),
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
            logger.error(f"Model dönüştürme hatası: {str(e)}")
            raise ValueError(f"Veri dönüştürme hatası: {str(e)}")
    
    def generate_religion_variations(
        self, 
        base_theme: str,
        count: int = 3
    ) -> list[Religion]:
        """
        Aynı temadan farklı din varyasyonları üretir
        
        Args:
            base_theme: Temel tema
            count: Üretilecek din sayısı
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
                logger.warning(f"Varyasyon {i+1} üretilemedi: {str(e)}")
                continue
        
        return variations
    
    def expand_religion(self, religion: Religion, component_type: str) -> Religion:
        """
        Mevcut dine yeni bileşenler ekler
        
        Args:
            religion: Mevcut din
            component_type: Eklenecek bileşen türü
        """
        
        try:
            new_component = self.generate_specific_component(
                component_type, 
                f"Bu din için uygun bir {component_type} üret",
                religion
            )
            
            # Yeni bileşeni dine ekle
            if component_type == "deity":
                new_deity = Deity(**new_component)
                religion.deities.append(new_deity)
            elif component_type == "ritual":
                new_ritual = Ritual(**new_component)
                religion.rituals.append(new_ritual)
            elif component_type == "legend":
                new_legend = MythologicalLegend(**new_component)
                religion.legends.append(new_legend)
            
            logger.info(f"{religion.name} dinine yeni {component_type} eklendi")
            return religion
            
        except Exception as e:
            logger.error(f"Din genişletme hatası: {str(e)}")
            raise
