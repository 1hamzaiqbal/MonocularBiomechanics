# Notebook Setup Instructions

## Problem
You're getting a `ModuleNotFoundError: No module named 'body_models'` error in your notebook.

## Solution
The issue is that the notebook is trying to import from `body_models` but the correct module name is `monocular_demos`. I've already fixed the import statement in your notebook.

## To fix the import issues:

### Option 1: Run the setup script (Recommended)
Add this cell at the beginning of your notebook and run it:

```python
# Run this cell to fix import issues
exec(open('setup_notebook.py').read())
```

### Option 2: Manual fix
Add this code at the beginning of your notebook:

```python
import sys
import os
# Add the current directory to Python path so we can import monocular_demos
sys.path.insert(0, os.getcwd())
```

### Option 3: Use the virtual environment
Make sure you're using the correct virtual environment:

```bash
source venv_py311/bin/activate
jupyter notebook
```

## What was fixed:
1. Changed `from body_models.biomechanics_mjx.visualize import render_trajectory, jupyter_embed_video` 
   to `from monocular_demos.biomechanics_mjx.visualize import render_trajectory, jupyter_embed_video`

2. All other imports in your notebook are already correct (using `monocular_demos` instead of `body_models`)

## Testing
You can test that everything works by running:
```bash
python test_imports.py
```

This should show "All imports successful!" if everything is set up correctly.
