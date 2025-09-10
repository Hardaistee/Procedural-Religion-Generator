from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from models import Religion, DeityType
from religion_generator import ReligionGenerator

# Environment variables yükle
load_dotenv()

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI uygulaması
app = FastAPI(
    title="Procedural Religion Generator",
    description="LLM ile din sistemleri üreten API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global değişkenler
religion_generator = ReligionGenerator()
generated_religions = {}  # Üretilen dinleri sakla

# Request modelleri
class ReligionGenerationRequest(BaseModel):
    theme: Optional[str] = None
    culture: Optional[str] = None
    complexity: str = "medium"
    deity_type: Optional[str] = None
    language: str = "Turkish"

class ComponentGenerationRequest(BaseModel):
    component_type: str
    context: str = ""
    religion_id: Optional[str] = None

class ReligionVariationRequest(BaseModel):
    base_theme: str
    count: int = 3

# Response modelleri
class ReligionResponse(BaseModel):
    id: str
    religion: Religion
    created_at: datetime
    generation_time: float

class ComponentResponse(BaseModel):
    component: dict
    component_type: str

# Ana endpoint'ler
@app.get("/")
async def root():
    """Ana sayfa"""
    return {
        "message": "Procedural Religion Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_religion": "POST /religions/generate",
            "get_religion": "GET /religions/{religion_id}",
            "list_religions": "GET /religions",
            "generate_component": "POST /components/generate",
            "generate_variations": "POST /religions/variations",
            "expand_religion": "POST /religions/{religion_id}/expand"
        }
    }

@app.post("/religions/generate", response_model=ReligionResponse)
async def generate_religion(request: ReligionGenerationRequest):
    """
    Yeni bir din üretir
    """
    try:
        start_time = datetime.now()
        
        logger.info(f"Yeni din üretim isteği: {request.dict()}")
        
        # Din üret
        religion = religion_generator.generate_religion(
            theme=request.theme,
            culture=request.culture,
            complexity=request.complexity,
            deity_type=request.deity_type,
            language=request.language
        )
        
        # ID oluştur ve sakla
        religion_id = f"religion_{len(generated_religions) + 1}_{int(start_time.timestamp())}"
        generation_time = (datetime.now() - start_time).total_seconds()
        
        generated_religions[religion_id] = {
            "religion": religion,
            "created_at": start_time,
            "generation_time": generation_time
        }
        
        logger.info(f"Din başarıyla üretildi: {religion_id}")
        
        return ReligionResponse(
            id=religion_id,
            religion=religion,
            created_at=start_time,
            generation_time=generation_time
        )
        
    except Exception as e:
        logger.error(f"Din üretim hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Din üretim hatası: {str(e)}")

@app.get("/religions/{religion_id}", response_model=ReligionResponse)
async def get_religion(religion_id: str):
    """
    Belirli bir dini getirir
    """
    if religion_id not in generated_religions:
        raise HTTPException(status_code=404, detail="Din bulunamadı")
    
    religion_data = generated_religions[religion_id]
    
    return ReligionResponse(
        id=religion_id,
        religion=religion_data["religion"],
        created_at=religion_data["created_at"],
        generation_time=religion_data["generation_time"]
    )

@app.get("/religions")
async def list_religions():
    """
    Tüm üretilen dinleri listeler
    """
    religions_list = []
    
    for religion_id, data in generated_religions.items():
        religions_list.append({
            "id": religion_id,
            "name": data["religion"].name,
            "description": data["religion"].description,
            "deity_type": data["religion"].deity_type,
            "created_at": data["created_at"],
            "generation_time": data["generation_time"]
        })
    
    return {
        "religions": religions_list,
        "total_count": len(religions_list)
    }

@app.post("/components/generate", response_model=ComponentResponse)
async def generate_component(request: ComponentGenerationRequest):
    """
    Belirli bir din bileşeni üretir
    """
    try:
        existing_religion = None
        if request.religion_id and request.religion_id in generated_religions:
            existing_religion = generated_religions[request.religion_id]["religion"]
        
        component = religion_generator.generate_specific_component(
            component_type=request.component_type,
            context=request.context,
            existing_religion=existing_religion
        )
        
        return ComponentResponse(
            component=component,
            component_type=request.component_type
        )
        
    except Exception as e:
        logger.error(f"Bileşen üretim hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bileşen üretim hatası: {str(e)}")

@app.post("/religions/variations")
async def generate_religion_variations(request: ReligionVariationRequest):
    """
    Aynı temadan farklı din varyasyonları üretir
    """
    try:
        variations = religion_generator.generate_religion_variations(
            base_theme=request.base_theme,
            count=request.count
        )
        
        variation_responses = []
        for i, religion in enumerate(variations):
            religion_id = f"variation_{request.base_theme}_{i+1}_{int(datetime.now().timestamp())}"
            generated_religions[religion_id] = {
                "religion": religion,
                "created_at": datetime.now(),
                "generation_time": 0  # Varyasyonlar için zaman hesaplanmıyor
            }
            
            variation_responses.append({
                "id": religion_id,
                "religion": religion
            })
        
        return {
            "base_theme": request.base_theme,
            "variations": variation_responses,
            "count": len(variation_responses)
        }
        
    except Exception as e:
        logger.error(f"Varyasyon üretim hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Varyasyon üretim hatası: {str(e)}")

@app.post("/religions/{religion_id}/expand")
async def expand_religion(religion_id: str, component_type: str):
    """
    Mevcut dine yeni bileşenler ekler
    """
    if religion_id not in generated_religions:
        raise HTTPException(status_code=404, detail="Din bulunamadı")
    
    try:
        religion_data = generated_religions[religion_id]
        expanded_religion = religion_generator.expand_religion(
            religion_data["religion"],
            component_type
        )
        
        # Güncellenmiş dini sakla
        generated_religions[religion_id]["religion"] = expanded_religion
        
        return {
            "message": f"Din başarıyla genişletildi",
            "religion_id": religion_id,
            "added_component": component_type,
            "religion": expanded_religion
        }
        
    except Exception as e:
        logger.error(f"Din genişletme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Din genişletme hatası: {str(e)}")

@app.get("/religions/{religion_id}/summary")
async def get_religion_summary(religion_id: str):
    """
    Din hakkında özet bilgi verir
    """
    if religion_id not in generated_religions:
        raise HTTPException(status_code=404, detail="Din bulunamadı")
    
    religion = generated_religions[religion_id]["religion"]
    
    return {
        "id": religion_id,
        "name": religion.name,
        "description": religion.description,
        "deity_type": religion.deity_type,
        "deity_count": len(religion.deities),
        "ritual_count": len(religion.rituals),
        "legend_count": len(religion.legends),
        "moral_rule_count": len(religion.moral_rules),
        "symbol_count": len(religion.symbols),
        "core_beliefs": religion.core_beliefs,
        "holy_places": religion.holy_places
    }

@app.delete("/religions/{religion_id}")
async def delete_religion(religion_id: str):
    """
    Belirli bir dini siler
    """
    if religion_id not in generated_religions:
        raise HTTPException(status_code=404, detail="Din bulunamadı")
    
    deleted_religion = generated_religions.pop(religion_id)
    
    return {
        "message": "Din başarıyla silindi",
        "deleted_religion": deleted_religion["religion"].name
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Sistem sağlık kontrolü"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "generated_religions_count": len(generated_religions)
    }

if __name__ == "__main__":
    import uvicorn
    
    # Port numarasını environment variable'dan al, yoksa varsayılan 8000 kullan
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Uygulama başlatılıyor - Port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
