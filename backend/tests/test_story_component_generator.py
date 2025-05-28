import pytest
import asyncio
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.services.story_component_generator import story_components

@pytest.mark.asyncio
async def test_story_components_basic():
    # Test için örnek bir hikaye promptu
    test_prompt = """
    Bir zamanlar küçük bir köyde yaşayan Ali adında bir çocuk vardı. 
    Ali'nin en büyük hayali, köyün dışındaki büyük şehri görmekti. 
    Bir gün, ailesinden gizli olarak şehre gitmeye karar verdi. 
    Yolculuğu sırasında birçok zorlukla karşılaştı ama sonunda 
    amacına ulaştı ve eve döndüğünde ailesine değerli bir ders verdi.
    """
    
    result = await story_components(test_prompt)
    
    # Sonucun bir sözlük olduğunu kontrol et
    assert isinstance(result, dict)
    
    # Gerekli anahtarların varlığını kontrol et
    required_keys = [
        "Main_character",
        "Environment",
        "Main_conflict",
        "Moral",
        "Plot",
        "character_goal",
        "Genre",
        "Final_type"
    ]
    
    for key in required_keys:
        assert key in result
        assert isinstance(result[key], str)
        assert len(result[key]) > 0  # Boş olmadığından emin ol
    
    # Türkçe karakterlerin varlığını kontrol et
    turkish_chars = "çğıöşüÇĞİÖŞÜ"
    for value in result.values():
        assert any(char in value for char in turkish_chars), "Çıktı Türkçe karakterler içermiyor"

@pytest.mark.asyncio
async def test_story_components_empty_prompt():
    # Boş prompt ile test
    with pytest.raises(Exception):
        await story_components("")

@pytest.mark.asyncio
async def test_story_components_short_prompt():
    # Çok kısa bir prompt ile test
    test_prompt = "Ali okula gitti."
    result = await story_components(test_prompt)
    
    assert isinstance(result, dict)
    # Kısa prompt için bile tüm alanların doldurulduğunu kontrol et
    assert all(len(value) > 0 for value in result.values()) 