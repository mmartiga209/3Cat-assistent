"""
Cadenes LangChain per a l'estudi de notícies
"""

from .video_analysis_chain import VideoAnalysisChain
from .tag_identification_chain import TagIdentificationChain
from .activity_generation_chain import ActivityGenerationChain
from .verification_chain import VerificationChain
from .critique_chain import CritiqueChain

__all__ = [
    'VideoAnalysisChain',
    'TagIdentificationChain',
    'ActivityGenerationChain',
    'VerificationChain',
    'CritiqueChain'
]