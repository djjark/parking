import os
from flask import Flask, Blueprint
from routes.identify_parking import identify_parking_bp
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)
app = Flask(__name__)
app.register_blueprint(identify_parking_bp)

@app.route("/")
def hello():
    return "Hello, World!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
