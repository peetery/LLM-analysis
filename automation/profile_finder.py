"""
Helper do znajdowania domyślnego profilu Chrome
"""
import os
import platform
from pathlib import Path

def find_chrome_profile():
    """Znajdź domyślny profil Chrome na różnych systemach"""
    system = platform.system()
    
    if system == "Windows":
        # Windows paths
        paths = [
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data',
            Path(os.environ.get('USERPROFILE', '')) / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data',
        ]
    elif system == "Darwin":  # macOS
        paths = [
            Path.home() / 'Library' / 'Application Support' / 'Google' / 'Chrome',
        ]
    else:  # Linux
        paths = [
            Path.home() / '.config' / 'google-chrome',
            Path.home() / '.config' / 'chromium',
        ]
    
    for path in paths:
        if path.exists():
            print(f"Znaleziono profil Chrome: {path}")
            return str(path)
    
    return None

def list_chrome_profiles(chrome_dir):
    """Lista dostępnych profili w katalogu Chrome"""
    chrome_path = Path(chrome_dir)
    profiles = []
    
    # Default profile
    if (chrome_path / "Default").exists():
        profiles.append("Default")
    
    # Profile 1, 2, 3...
    for i in range(1, 10):
        profile_name = f"Profile {i}"
        if (chrome_path / profile_name).exists():
            profiles.append(profile_name)
    
    return profiles

def main():
    """Test znajdowania profili"""
    print("=== Chrome Profile Finder ===")
    
    chrome_dir = find_chrome_profile()
    
    if chrome_dir:
        print(f"✓ Katalog Chrome: {chrome_dir}")
        
        profiles = list_chrome_profiles(chrome_dir)
        print(f"\nDostępne profile:")
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile}")
        
        return chrome_dir, profiles
    else:
        print("✗ Nie znaleziono katalogu Chrome")
        return None, []

if __name__ == "__main__":
    main()