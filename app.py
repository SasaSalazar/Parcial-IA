# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import requests
import logging
from pddl_generator import generate_pddl_from_instruction

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(level=logging.INFO)

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

SOLVER_URL = "https://solver.planning.domains/solve"  # public solver

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    instr = data.get("instruction", "")
    if not instr:
        return jsonify({"error": "No instruction provided"}), 400

    result = generate_pddl_from_instruction(instr)
    domain = result["domain"]
    problem = result["problem"]
    meta = result["meta"]

    # Save files for download
    dpath = OUTPUT / "domain.pddl"
    ppath = OUTPUT / "problem.pddl"
    dpath.write_text(domain, encoding="utf-8")
    ppath.write_text(problem, encoding="utf-8")

    return jsonify({"domain": domain, "problem": problem, "meta": meta}), 200

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json(force=True)
    domain = data.get("domain")
    problem = data.get("problem")
    if not domain or not problem:
        return jsonify({"error": "domain and problem required"}), 400

    payload = {"domain": domain, "problem": problem}
    try:
        r = requests.post(SOLVER_URL, json=payload, timeout=30)
        r.raise_for_status()
        return jsonify(r.json()), 200
    except Exception as e:
        logging.exception("Solver error")
        return jsonify({"error": "solver request failed", "detail": str(e)}), 502

@app.route("/download/<path:filename>")
def download(filename):
    # safe serve from output folder
    return send_from_directory(str(OUTPUT.resolve()), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
