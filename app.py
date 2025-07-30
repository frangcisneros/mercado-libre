from flask import Flask, render_template, request
from scraper import buscar_productos_ml

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/resultados", methods=["GET"])
def resultados():
    q = request.args.get("q", "").strip()
    productos = []
    if q:
        productos = buscar_productos_ml(q)
    return render_template("resultados.html", productos=productos, query=q)


if __name__ == "__main__":
    app.run(debug=True)
