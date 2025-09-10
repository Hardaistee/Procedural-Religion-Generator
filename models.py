from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class DeityType(str, Enum):
    """Deity types"""
    MONOTHEISTIC = "monotheistic"  # Single deity
    POLYTHEISTIC = "polytheistic"  # Multiple deities
    PANTHEISTIC = "pantheistic"    # Pantheistic
    ANIMISTIC = "animistic"        # Animistic

class Deity(BaseModel):
    """Deity/Goddess model"""
    name: str
    title: str
    domain: str  # Power domain (war, wisdom, nature, etc.)
    description: str
    attributes: List[str]  # Attributes
    symbols: List[str]     # Symbols

class SacredText(BaseModel):
    """Sacred text model"""
    title: str
    content: str
    chapters: List[str]
    language: str
    origin_story: str  # How it was created

class Ritual(BaseModel):
    """Ritual model"""
    name: str
    purpose: str
    frequency: str  # How often it's performed
    participants: str  # Who participates
    steps: List[str]
    materials_needed: List[str]
    significance: str

class MoralRule(BaseModel):
    """Moral rule model"""
    rule: str
    description: str
    severity: str  # Light, medium, heavy
    punishment: str  # Punishment
    reward: str      # Reward

class MythologicalLegend(BaseModel):
    """Mythological legend model"""
    title: str
    story: str
    characters: List[str]
    moral_lesson: str
    cultural_impact: str

class RewardPunishment(BaseModel):
    """Reward and punishment system"""
    rewards: List[str]
    punishments: List[str]
    afterlife_concept: str
    judgment_criteria: List[str]

class Symbol(BaseModel):
    """Symbol model"""
    name: str
    meaning: str
    visual_description: str
    usage_context: str  # When it's used

class Religion(BaseModel):
    """Main religion model"""
    name: str
    description: str
    deity_type: DeityType
    language: str  # Language the religion was generated in
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
