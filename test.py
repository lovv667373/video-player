#!/usr/bin/env python3
"""
Simple test to verify packages are working
"""

try:
    import cv2
    print("✅ OpenCV imported successfully")
    
    from PIL import Image
    print("✅ Pillow imported successfully")
    
    import numpy as np
    print("✅ NumPy imported successfully")
    
    print("\n✅ All packages installed correctly!")
    print("Your video player should now work.")
    
except ModuleNotFoundError as e:
    print(f"❌ Missing package: {e}")
    print("\nInstall missing packages with:")
    print("pip3 install Pillow opencv-python numpy")
    
except Exception as e:
    print(f"❌ Error: {e}")