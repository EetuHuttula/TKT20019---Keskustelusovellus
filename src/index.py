import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)