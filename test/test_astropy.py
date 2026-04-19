import glob
import os
import pytest
from astropy.coordinates import solar_system_ephemeris, get_body
from astropy.time import Time
import astropy.units as u

def get_bsp_files():
    """Locate all minified BSP files in the dist directory."""
    return glob.glob("../dist/*.bsp")

@pytest.mark.parametrize("bsp_path", get_bsp_files())
def test_astropy_load_and_calculate(bsp_path):
    """Test that astropy can use the minified kernel as an ephemeris source."""
    assert os.path.exists(bsp_path), f"BSP file not found: {bsp_path}"
    
    # Use the kernel as the ephemeris source
    with solar_system_ephemeris.set(bsp_path):
        t = Time("2024-01-01 00:00:00")
        
        # Test Moon
        moon = get_body('moon', t)
        assert moon is not None
        print(f"Moon position from {bsp_path} (Astropy): {moon.cartesian}")
        
        # Test Earth
        earth = get_body('earth', t)
        assert earth is not None
        
        # Test Sun
        sun = get_body('sun', t)
        assert sun is not None
        
        # Simple distance check for Moon relative to Earth
        # get_body returns GCRS coordinates (Earth-centered) by default for Moon
        dist = moon.separation_3d(earth)
        # Wait, get_body('earth', t) in GCRS will be at origin.
        # Let's check distance to barycenter or just check the moon object
        assert moon.distance.to(u.km).value > 300000
