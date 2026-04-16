from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def charger_donnees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enregistrer', methods=['POST'])
def enregistrer():
    donnees = charger_donnees()
    nouveau_patient = request.json
    donnees.append(nouveau_patient)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=4)
    return jsonify({"status": "success"})

@app.route('/statistiques')
def statistiques():
    donnees = charger_donnees()
    if not donnees:
        return jsonify({"total": 0, "imc_moyen": 0, "regions": {}})

    total = len(donnees)
    imc_moyen = sum(float(p['imc']) for p in donnees) / total
    
    # Analyse par région
    regions = {}
    for p in donnees:
        reg = p['region']
        regions[reg] = regions.get(reg, 0) + 1

    return jsonify({
        "total": total,
        "imc_moyen": round(imc_moyen, 1),
        "regions": regions,
        "liste": donnees
    })

if __name__ == '__main__':
    app.run(debug=True)
