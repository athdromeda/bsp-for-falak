import glob
import os
import pytest
from skyfield.api import load

def get_bsp_files():
    """Locate all minified BSP files in the dist directory."""
    bsp_files = glob.glob("../dist/*.bsp")
    return bsp_files

@pytest.mark.parametrize("bsp_path", get_bsp_files())
def test_skyfield_load_and_calculate(bsp_path):
    """Test that skyfield can load the kernel and perform basic calculations."""
    assert os.path.exists(bsp_path), f"BSP file not found: {bsp_path}"
    
    # Load the kernel
    planets = load(bsp_path)
    print(f"Loaded {bsp_path}")
    
    # Check for expected bodies (Sun: 10, Moon: 301, Earth: 399, EMB: 3)
    # Skyfield provides access via ID
    assert 3 in planets, f"Earth-Moon Barycenter (3) missing in {bsp_path}"
    assert 10 in planets, f"Sun (10) missing in {bsp_path}"
    assert 301 in planets, f"Moon (301) missing in {bsp_path}"
    assert 399 in planets, f"Earth (399) missing in {bsp_path}"
    
    # Perform a simple calculation: Moon relative to Earth
    ts = load.timescale()
    t = ts.utc(2024, 1, 1)
    
    earth = planets[399]
    moon = planets[301]
    
    # Position of Moon relative to Earth
    astrometric = earth.at(t).observe(moon)
    ra, dec, distance = astrometric.radec()
    
    assert distance.km > 300000, "Moon distance should be reasonable"
    print(f"Moon position at {t.utc_iso()}: RA={ra}, DEC={dec}, DIST={distance.km:.2f} km")
