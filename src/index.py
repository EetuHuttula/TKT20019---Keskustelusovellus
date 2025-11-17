import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

if __name__ == "__main__":
    # Run on port 5000 so Robot tests (and other tests) that expect
    # the app at http://127.0.0.1:5000 work without overriding test files.
    app.run(port=5000, host="0.0.0.0", debug=True)