from flask import Flask, request,render_template
app = Flask(__name__)

#home para desplegar nombres de los sujetos evaluados
@app.route("/", methods=["POST","GET"])
def home_www():
    return render_template("inicio.html")

app.run("localhost",8080)
