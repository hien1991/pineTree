import sys
sys.path.insert(0, '.')

from flask_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
