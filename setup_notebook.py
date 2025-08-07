#!/usr/bin/env python3
"""
Setup script for the monocular biomechanics notebook.
Run this cell at the beginning of your notebook to fix import issues.
"""

import sys
import os

# Add the current directory to Python path so we can import monocular_demos
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"✓ Added {current_dir} to Python path")

# Test the key imports
try:
    from monocular_demos.biomechanics_mjx.visualize import render_trajectory, jupyter_embed_video
    print("✓ visualize module imported successfully")
    
    from monocular_demos.biomechanics_mjx.forward_kinematics import ForwardKinematics
    print("✓ forward_kinematics module imported successfully")
    
    from monocular_demos.utils import video_reader
    print("✓ utils module imported successfully")
    
    print("\n🎉 All modules imported successfully! Your notebook should work now.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this in the correct directory with the monocular_demos package.")
