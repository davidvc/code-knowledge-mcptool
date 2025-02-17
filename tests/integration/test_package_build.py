import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path
import pytest

def test_package_builds_and_installs():
    """Test that the package can be built and installed without dependency conflicts."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Create a temporary directory for our virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "venv"
        
        # Create a virtual environment
        venv.create(venv_path, with_pip=True)
        
        # Get the path to the Python executable in the virtual environment
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
            
        # Install build package
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "build"],
            check=True,
            cwd=project_root
        )
        
        # Build the package
        subprocess.run(
            [str(python_path), "-m", "build"],
            check=True,
            cwd=project_root
        )
        
        # Install the built wheel
        wheel_dir = project_root / "dist"
        wheels = list(wheel_dir.glob("*.whl"))
        assert wheels, "No wheel file found in dist directory"
        
        subprocess.run(
            [str(python_path), "-m", "pip", "install", str(wheels[0])],
            check=True,
            cwd=project_root
        )
        
        # Verify the package can be imported
        result = subprocess.run(
            [str(python_path), "-c", "import code_knowledge_tool; print('Package successfully imported')"],
            check=True,
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        assert "Package successfully imported" in result.stdout