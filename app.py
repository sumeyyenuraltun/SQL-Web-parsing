from flask import Flask, render_template, request
from veri_islemleri import web_parsing, veriyi_ekle
from db import getDovizKuru, getFiltreliVeri

app = Flask(__name__)

@app.route('/')
def home():
    doviz_kuru = getDovizKuru()
    return render_template("arayuz.html", doviz_kuru=doviz_kuru)

@app.route("/filtreli", methods=["POST"])
def filtreli():
    min_alis = request.form.get("min_alis")
    max_alis = request.form.get("max_alis")
    min_dusuk = request.form.get("min_dusuk")
    max_dusuk = request.form.get("max_dusuk")
    min_degisim = request.form.get("min_degisim")
    max_degisim = request.form.get("max_degisim")

    doviz_kuru = getFiltreliVeri(min_alis, max_alis, min_dusuk, max_dusuk, min_degisim, max_degisim)
    return render_template("arayuz.html", doviz_kuru=doviz_kuru)

@app.route('/filtre_sifirla', methods=['GET'])
def filtre_sifirla():
    doviz_kuru = getDovizKuru()
    return render_template("arayuz.html", doviz_kuru=doviz_kuru)

if __name__ == '__main__':
    web_parsing()
    veriyi_ekle()
    app.run(debug=False)
