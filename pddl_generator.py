# pddl_generator.py (Versión 2 NER heurístico por que que fastidio)

# NOTA: esta es la version 2.1 del generador PDDL, este utiliza un NER heurístico

import re
import json

# -----------------------------
# STOPWORDS para evitar falsos objetos
# -----------------------------
STOPWORDS = {
    "el", "la", "lo", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "a", "en", "pero", "primero", "que", "tiene",
    "para", "con", "su", "sus", "y", "o", "u", "se", "debe", "deben",
    "debo", "debes", "solo", "despues", "después", "antes", "luego"
}

# -----------------------------
# Raíces verbales → acciones
# -----------------------------
VERB_ACTION_MAP = {
    "recog": "pick",
    "tom": "pick",
    "agarr": "pick",
    "entreg": "deliver",
    "llev": "deliver",
    "abr": "open",
    "cerr": "close",
    "encend": "activate",
    "prend": "activate",
    "prepar": "prepare",
    "herv": "heat",
    "carg": "charge",
    "activ": "activate",
    "busc": "locate",
    "encontr": "locate",
    "localiz": "locate",
    "repar": "repair",
    "arregl": "repair",
    "mont": "assemble",
    "llen": "fill",
    "neutraliz": "neutralize",
    "mat": "neutralize",
    "asesin": "neutralize",
    "destr": "neutralize",
    "acab": "neutralize"
}

# -----------------------------
# Detectar objetos, lugares y targets
# -----------------------------

def extract_nouns(text):
    words = re.findall(r"[a-záéíóúñ]+", text.lower())
    return [w for w in words if w not in STOPWORDS]

# heurística básica: si suena a lugar
LOCATION_HINTS = {"cocina", "cuarto", "habitacion", "habitación", "sala", "mesa", "estanteria", "estantería", "laboratorio", "dormitorio", "home"}

TARGET_HINTS = {"enemigo", "mosquito", "amenaza", "intruso", "objetivo", "target"}

# -----------------------------
# Parsear secuencias: "pero primero", "antes de", "solo después de"
# -----------------------------

def detect_order(text):
    text = text.lower()
    if "pero primero" in text or "antes de" in text:
        return "reverse"  # indica que la primera acción mencionada va después
    return "normal"

# -----------------------------
# Detectar verbos → acción
# -----------------------------

def detect_actions(text):
    actions = []
    words = extract_nouns(text)
    for w in words:
        for root, act in VERB_ACTION_MAP.items():
            if w.startswith(root):
                actions.append(act)
    return actions

# -----------------------------
# Ensamblar acciones con pasos
# -----------------------------

def build_domain(actions):
    step_predicates = "".join([f"    (step-done-{i})\n" for i in range(len(actions)+1)])

    action_blocks = []
    for i, act in enumerate(actions):
        s1 = i
        s2 = i + 1

        if act == "locate":
            template = f"""
  (:action locate-{i}
    :parameters (?a - agent ?o - object ?l - location ?s1 - step ?s2 - step)
    :precondition (step-done-?s1)
    :effect (and (in ?o ?l) (step-done-?s2))
  )
"""
        elif act == "deliver":
            template = f"""
  (:action deliver-{i}
    :parameters (?a - agent ?o - object ?from - location ?to - location ?s1 - step ?s2 - step)
    :precondition (and (step-done-?s1) (at ?a ?from) (in ?o ?from))
    :effect (and (not (in ?o ?from)) (in ?o ?to) (step-done-?s2))
  )
"""
        elif act == "neutralize":
            template = f"""
  (:action neutralize-{i}
    :parameters (?a - agent ?t - target ?l - location ?s1 - step ?s2 - step)
    :precondition (and (step-done-?s1) (at ?a ?l))
    :effect (and (neutralized ?t) (step-done-?s2))
  )
"""
        else:
            # genérico
            template = f"""
  (:action {act}-{i}
    :parameters (?a - agent ?o - object ?l - location ?s1 - step ?s2 - step)
    :precondition (step-done-?s1)
    :effect (step-done-?s2)
  )
"""

        # sustituir pasos
        template = template.replace("?s1", str(s1)).replace("?s2", str(s2))
        action_blocks.append(template)

    domain = f"""
(define (domain generated_domain)
  (:requirements :strips :typing)
  (:types agent object location target step)
  (:predicates
    (at ?a - agent ?l - location)
    (in ?o - object ?l - location)
    (has ?a - agent ?o - object)
    (neutralized ?t - target)
{step_predicates}  )
{''.join(action_blocks)}
)
"""
    return domain

# -----------------------------
# Construir el problema
# -----------------------------

def build_problem(objs, locs):
    obj_str = " ".join(objs)
    loc_str = " ".join(locs)

    problem = f"""
(define (problem generated-problem)
  (:domain generated_domain)
  (:objects
    {obj_str} - object
    {loc_str} - location
  )
  (:init
    (at robot home)
  )
  (:goal (step-done-{len(objs)}))
)
"""
    return problem

# -----------------------------
# Fun principal — llamada desde app.py
# -----------------------------

def generate_pddl_from_instruction(instruction):
    text = instruction.lower()
    order_type = detect_order(text)

    # acciones
    acts = detect_actions(text)
    if order_type == "reverse":
        acts = acts[::-1]

    # objetos / lugares
    nouns = extract_nouns(text)

    objs = [w for w in nouns if w not in LOCATION_HINTS and w not in TARGET_HINTS and w not in VERB_ACTION_MAP]
    if "robot" not in objs:
        objs.append("robot")

    locs = ["home"] + [w for w in nouns if w in LOCATION_HINTS]

    # construir dominio y problema
    domain = build_domain(acts)
    problem = build_problem(objs, locs)

    return {
        "domain": domain,
        "problem": problem,
        "meta": {
            "actions": acts,
            "objects": objs,
            "locations": locs,
            "order": order_type
        }
    }
