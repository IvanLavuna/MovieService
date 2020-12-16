from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!' + '16'


if __name__ == "__main__":
    app.run(debug=True, port=4200)