from flask import Flask, Blueprint
from routes.identify_parking import identify_parking_bp

app = Flask(__name__)
app.register_blueprint(identify_parking_bp)

@app.route("/")
def hello():
    return "Hello, World!"
if __name__ == '__main__':
    app.run(debug=True)
