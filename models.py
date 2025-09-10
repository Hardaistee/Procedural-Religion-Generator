from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class DeityType(str, Enum):
    """Tanrı türleri"""
    MONOTHEISTIC = "monotheistic"  # Tek tanrılı
    POLYTHEISTIC = "polytheistic"  # Çok tanrılı
    PANTHEISTIC = "pantheistic"    # Panteistik
    ANIMISTIC = "animistic"        # Animistik

class Deity(BaseModel):
    """Tanrı/Tanrıça modeli"""
    name: str
    title: str
    domain: str  # Güç alanı (savaş, bilgelik, doğa, vb.)
    description: str
    attributes: List[str]  # Özellikler
    symbols: List[str]     # Simgeler

class SacredText(BaseModel):
    """Kutsal metin modeli"""
    title: str
    content: str
    chapters: List[str]
    language: str
    origin_story: str  # Nasıl ortaya çıktığı

class Ritual(BaseModel):
    """Ritüel modeli"""
    name: str
    purpose: str
    frequency: str  # Ne sıklıkla yapılır
    participants: str  # Kimler katılır
    steps: List[str]
    materials_needed: List[str]
    significance: str

class MoralRule(BaseModel):
    """Ahlaki kural modeli"""
    rule: str
    description: str
    severity: str  # Hafif, orta, ağır
    punishment: str  # Cezası
    reward: str      # Ödülü

class MythologicalLegend(BaseModel):
    """Mitolojik efsane modeli"""
    title: str
    story: str
    characters: List[str]
    moral_lesson: str
    cultural_impact: str

class RewardPunishment(BaseModel):
    """Ödül ve ceza sistemi"""
    rewards: List[str]
    punishments: List[str]
    afterlife_concept: str
    judgment_criteria: List[str]

class Symbol(BaseModel):
    """Sembol modeli"""
    name: str
    meaning: str
    visual_description: str
    usage_context: str  # Ne zaman kullanılır

class Religion(BaseModel):
    """Ana din modeli"""
    name: str
    description: str
    deity_type: DeityType
    language: str  # Din üretildiği dil
    deities: List[Deity]
    sacred_texts: List[SacredText]
    rituals: List[Ritual]
    moral_rules: List[MoralRule]
    legends: List[MythologicalLegend]
    reward_punishment: RewardPunishment
    symbols: List[Symbol]
    core_beliefs: List[str]
    practices: List[str]
    holy_places: List[str]
    religious_leaders: str
    creation_myth: str
