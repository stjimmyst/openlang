from flask import Flask
import time, os

app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)