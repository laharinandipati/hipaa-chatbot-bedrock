from src.masker import mask_phi

def test_mask_basic():
    masked, mapping = mask_phi("John visited on 09/21/2025.")
    assert "[NAME]" in masked
    assert "[DATE]" in masked
    assert mapping["John"] == "[NAME]"
