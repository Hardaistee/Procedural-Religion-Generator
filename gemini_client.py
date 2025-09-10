import os
import google.generativeai as genai
from typing import Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """Gemini 2.5 Flash API istemcisi"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_religion(self, theme: str = None, culture: str = None, complexity: str = "medium", deity_type: str = None, language: str = "Turkish") -> Dict[str, Any]:
        """
        Din üretir
        
        Args:
            theme: Din teması (doğa, savaş, bilgelik, vb.)
            culture: Kültürel etki (antik, modern, fantastik, vb.)
            complexity: Karmaşıklık seviyesi (simple, medium, complex)
            deity_type: Tanrı türü (monotheistic, polytheistic, pantheistic, animistic)
            language: Din üretilecek dil (Turkish, English, Spanish, French, German, Italian, Portuguese, Russian, Arabic, Japanese, Chinese)
        """
        
        prompt = self._create_religion_prompt(theme, culture, complexity, deity_type, language)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Gemini API hatası: {str(e)}")
    
    def _create_religion_prompt(self, theme: str, culture: str, complexity: str, deity_type: str, language: str) -> str:
        """Din üretimi için prompt oluşturur"""
        
        # Dil ayarları
        language_instructions = self._get_language_instructions(language)
        
        base_prompt = f"""
Sen bir yaratıcı din tasarımcısısın. Aşağıdaki kriterlere göre detaylı bir din sistemi oluştur:

Tema: {theme or "genel"}
Kültür: {culture or "evrensel"}
Karmaşıklık: {complexity}
Tanrı Türü: {deity_type or "polytheistic"}
Dil: {language}

{language_instructions}

Lütfen aşağıdaki JSON formatında bir din sistemi oluştur:

{{
    "name": "Din adı",
    "description": "Din hakkında genel açıklama",
    "deity_type": "monotheistic|polytheistic|pantheistic|animistic",
    "language": "{language}",
    "deities": [
        {{
            "name": "Tanrı adı",
            "title": "Unvanı",
            "domain": "Güç alanı",
            "description": "Açıklama",
            "attributes": ["özellik1", "özellik2"],
            "symbols": ["sembol1", "sembol2"]
        }}
    ],
    "sacred_texts": [
        {{
            "title": "Kutsal metin adı",
            "content": "İçerik özeti",
            "chapters": ["bölüm1", "bölüm2"],
            "language": "Dil",
            "origin_story": "Nasıl ortaya çıktığı"
        }}
    ],
    "rituals": [
        {{
            "name": "Ritüel adı",
            "purpose": "Amacı",
            "frequency": "Sıklığı",
            "participants": "Katılımcılar",
            "steps": ["adım1", "adım2"],
            "materials_needed": ["malzeme1", "malzeme2"],
            "significance": "Önemi"
        }}
    ],
    "moral_rules": [
        {{
            "rule": "Kural",
            "description": "Açıklama",
            "severity": "Hafif|Orta|Ağır",
            "punishment": "Cezası",
            "reward": "Ödülü"
        }}
    ],
    "legends": [
        {{
            "title": "Efsane adı",
            "story": "Hikaye",
            "characters": ["karakter1", "karakter2"],
            "moral_lesson": "Ahlaki ders",
            "cultural_impact": "Kültürel etki"
        }}
    ],
    "reward_punishment": {{
        "rewards": ["ödül1", "ödül2"],
        "punishments": ["ceza1", "ceza2"],
        "afterlife_concept": "Ölüm sonrası kavramı",
        "judgment_criteria": ["kriter1", "kriter2"]
    }},
    "symbols": [
        {{
            "name": "Sembol adı",
            "meaning": "Anlamı",
            "visual_description": "Görsel açıklama",
            "usage_context": "Kullanım bağlamı"
        }}
    ],
    "core_beliefs": ["inanç1", "inanç2"],
    "practices": ["uygulama1", "uygulama2"],
    "holy_places": ["kutsal yer1", "kutsal yer2"],
    "religious_leaders": "Dini liderlerin rolü",
    "creation_myth": "Yaratılış efsanesi"
}}

ÖNEMLİ: deity_type alanını MUTLAKA "{deity_type or "polytheistic"}" olarak ayarla. Bu parametreye uygun tanrı sistemi oluştur.

- monotheistic: Tek tanrı (örnek: Hıristiyanlık, İslam)
- polytheistic: Çok tanrılı (örnek: Antik Yunan, Norse mitolojisi)  
- pantheistic: Tanrı=Evren (örnek: Spinoza'nın felsefesi)
- animistic: Her şeyin ruhu var (örnek: Şamanizm, yerli dinler)

Lütfen yaratıcı ve detaylı bir din sistemi oluştur. Her bölümü doldur ve tutarlı bir mitoloji oluştur.
"""
        
        return base_prompt
    
    def _get_language_instructions(self, language: str) -> str:
        """Dil talimatlarını döndürür"""
        
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
        """Gemini'den gelen yanıtı parse eder"""
        try:
            # JSON kısmını bul
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Geçerli JSON formatı bulunamadı")
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parse hatası: {str(e)}")
        except Exception as e:
            raise ValueError(f"Yanıt işleme hatası: {str(e)}")
    
    def generate_specific_component(self, component_type: str, context: str = "") -> Dict[str, Any]:
        """
        Belirli bir din bileşeni üretir
        
        Args:
            component_type: Bileşen türü (deity, ritual, legend, vb.)
            context: Bağlam bilgisi
        """
        
        prompts = {
            "deity": f"""
            Yaratıcı bir tanrı/tanrıça tasarla. {context}
            
            JSON formatında:
            {{
                "name": "Tanrı adı",
                "title": "Unvanı", 
                "domain": "Güç alanı",
                "description": "Açıklama",
                "attributes": ["özellik1", "özellik2"],
                "symbols": ["sembol1", "sembol2"]
            }}
            """,
            
            "ritual": f"""
            Detaylı bir dini ritüel tasarla. {context}
            
            JSON formatında:
            {{
                "name": "Ritüel adı",
                "purpose": "Amacı",
                "frequency": "Sıklığı", 
                "participants": "Katılımcılar",
                "steps": ["adım1", "adım2"],
                "materials_needed": ["malzeme1", "malzeme2"],
                "significance": "Önemi"
            }}
            """,
            
            "legend": f"""
            Mitolojik bir efsane yaz. {context}
            
            JSON formatında:
            {{
                "title": "Efsane adı",
                "story": "Hikaye",
                "characters": ["karakter1", "karakter2"],
                "moral_lesson": "Ahlaki ders",
                "cultural_impact": "Kültürel etki"
            }}
            """
        }
        
        if component_type not in prompts:
            raise ValueError(f"Desteklenmeyen bileşen türü: {component_type}")
        
        try:
            response = self.model.generate_content(prompts[component_type])
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Bileşen üretim hatası: {str(e)}")
