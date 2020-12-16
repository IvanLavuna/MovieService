from movie_app import app


@app.route("/")
@app.route("/api/v1/hello-world-16")
def hello():
    return "Hello World!" + " 16"
