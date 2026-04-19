import glob
import os
import pytest
import spiceypy as spice

def get_bsp_files():
    """Locate all minified BSP files in the dist directory."""
    return glob.glob("../dist/*.bsp")

@pytest.fixture(scope="module", autouse=True)
def load_lsk():
    """Load the leapseconds kernel (LSK) for all tests."""
    lsk_path = "../raw/naif0012.tls"
    assert os.path.exists(lsk_path), f"LSK file not found: {lsk_path}"
    spice.furnsh(lsk_path)
    yield
    spice.unload(lsk_path)

@pytest.mark.parametrize("bsp_path", get_bsp_files())
def test_spiceypy_bodies_presence(bsp_path):
    """Test that spiceypy can load the kernel and bodies are accessible."""
    assert os.path.exists(bsp_path), f"BSP file not found: {bsp_path}"
    
    # Load (furnish) the BSP kernel
    spice.furnsh(bsp_path)
    
    try:
        # Check presence using spkobj
        bodies = spice.spkobj(bsp_path)
        
        # Bodies IDs: 3 (EMB), 10 (Sun), 301 (Moon), 399 (Earth)
        expected_ids = {3, 10, 301, 399}
        actual_ids = set(bodies)
        
        for body_id in expected_ids:
            assert body_id in actual_ids, f"Body ID {body_id} missing in {bsp_path}"
            
        # Test calculation: Moon (301) relative to Earth (399)
        et = spice.str2et('2024-01-01 00:00:00')
        state, lt = spice.spkezr('301', et, 'J2000', 'NONE', '399')
        
        assert len(state) == 6
        distance_km = (state[0]**2 + state[1]**2 + state[2]**2)**0.5
        assert distance_km > 300000, "Moon distance should be reasonable"
        print(f"Distance to Moon from {bsp_path}: {distance_km:.2f} km")
        
    finally:
        # Always unload the BSP kernel
        spice.unload(bsp_path)
