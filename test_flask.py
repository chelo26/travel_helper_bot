
# from flask import Flask
# test_flask = Flask(__name__)

# @test_flask.route("/")
# def hello():
#     return "<h1 style='color:blue'>Hello There!</h1>"
# if __name__ == "__main__":
#     #application.run(host='0.0.0.0', port='8080')
#     test_flask.run(host='0.0.0.0', port='5000')

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')