from flask import Flask, render_template

# locate directory of folder
app = Flask(__name__,
            static_folder = "./static",
            template_folder = "./templates")

# @app.route('/')
# def index():
#     return render_template("index.html")