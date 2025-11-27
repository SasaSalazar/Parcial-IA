import re
from collections import OrderedDict

# -------------------------
# LEXICON (mapa verbo -> tipo de acción)
# -------------------------
# Incluye español e inglés comunes. Ampliable.
ACTION_LEXICON = {
    # movimiento / transporte
    "ir": "MOVE", "go": "MOVE", "walk": "MOVE", "move": "MOVE",
    "llevar": "TRANSFER", "lleva": "TRANSFER", "carry": "TRANSFER", "take": "TRANSFER",
    "traer": "BRING", "bring": "BRING", "fetch": "BRING",

    # manipular objetos
    "recoger": "PICK", "recoge": "PICK", "toma": "PICK", "agarrar": "PICK", "pick": "PICK",
    "dejar": "PLACE", "colocar": "PLACE", "pon": "PLACE", "place": "PLACE", "put": "PLACE",

    # abrir / cerrar
    "abrir": "OPEN", "abre": "OPEN", "open": "OPEN",
    "cerrar": "CLOSE", "cierra": "CLOSE", "close": "CLOSE",

    # usar / usar llave
    "usar": "USE", "usa": "USE", "use": "USE",

    # cocinar / preparar
    "hacer": "MAKE", "preparar": "MAKE", "prepare": "MAKE", "make": "MAKE",
    "cocinar": "COOK", "cocina": "COOK", "cook": "COOK",
    "hervir": "BOIL", "hervir agua": "BOIL", "boil": "BOIL",

    # encender / apagar
    "encender": "TURN_ON", "enciende": "TURN_ON", "turn on": "TURN_ON",
    "apagar": "TURN_OFF", "apaga": "TURN_OFF", "turn off": "TURN_OFF",

    # cargar / cargar bateria
    "cargar": "CHARGE", "carga": "CHARGE", "charge": "CHARGE",

    # limpiar
    "limpiar": "CLEAN", "limpia": "CLEAN", "clean": "CLEAN",

    # entregar / enviar
    "entregar": "DELIVER", "entrega": "DELIVER", "deliver": "DELIVER",

    # neutralizar (abstracto)
    "neutralizar": "NEUTRALIZE", "neutraliza": "NEUTRALIZE", "eliminar": "NEUTRALIZE", "kill": "NEUTRALIZE",

    # observar / localizar
    "localizar": "LOCATE", "encontrar": "LOCATE", "find": "LOCATE", "buscar": "LOCATE",

    # montar / ensamblar
    "montar": "ASSEMBLE", "monta": "ASSEMBLE", "assemble": "ASSEMBLE",

    # varias acciones útiles
    "sacar": "REMOVE", "reemplazar": "REPLACE", "repara": "REPAIR", "reparar": "REPAIR"
}

# -------------------------
# Listas de objetos/lugares simples (NER por heurística)
# -------------------------
COMMON_OBJECTS = [
    "manzana","manzanas","limon","limones","pera","peras","libro","llave","llaves","taza","tazas",
    "cafe","café","pan","huevo","bateria","batería","pieza","pieza_dañada","paquete","juguete",
    "chip","archivo","generador","tienda","cocina","casa","mesa","silla","estanteria","estantería",
    "puerta","cofre","ventana","receptor","nucleo","planta","flor","gatito","gato","niño","niña"
]
COMMON_PLACES = [
    "mesa","cocina","cuarto","habitación","habitacion","estanteria","estantería","cafeteria","cafetería",
    "tienda","supermercado","puerta","laboratorio","laboratorio","base","inicio","punto_inicial","casa"
]

# -------------------------
# Conectores y patrones de orden
# -------------------------
ORDER_CONNECTORS = [
    r"\bprimero\b", r"\bdespués\b", r"\bluego\b", r"\bantes de\b", r"\bdespues de\b",
    r"\bpero solo después de\b", r"\bpero solo despues de\b", r"\bpero despues de\b",
    r"\bthen\b", r"\bafter\b", r"\bbefore\b"
]

SPLIT_SEPARATORS = [r"\by luego\b", r"\by después\b", r"\b y luego\b", r"\b, y\b", r"\b y\b", r";"]

# -------------------------
# Utilidades de parsing
# -------------------------
def normalize(text):
    t = text.lower()
    t = t.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    # unify punctuation spacing
    t = re.sub(r"[-/]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def find_objects(tokens):
    found = []
    for o in COMMON_OBJECTS:
        if o in tokens:
            found.append(o.replace(" ", "_"))
    return found

def find_places(tokens):
    found = []
    for p in COMMON_PLACES:
        if p in tokens:
            found.append(p.replace(" ", "_"))
    return found

def find_actions(tokens):
    acts = []
    for i, tok in enumerate(tokens):
        # check two-word verbs first
        if i+1 < len(tokens):
            two = f"{tok} {tokens[i+1]}"
            if two in ACTION_LEXICON:
                acts.append((two, ACTION_LEXICON[two]))
                continue
        if tok in ACTION_LEXICON:
            acts.append((tok, ACTION_LEXICON[tok]))
    return acts

# -------------------------
# Extraer pasos (secuencia) simple
# -------------------------
def split_into_steps(text):
    """
    Divide la instrucción en pasos usando comas, 'y', 'luego', 'después', 'antes de', 'primero'...
    Mantiene un orden aproximado.
    """
    txt = normalize(text)
    # split by explicit separators conservatively
    parts = re.split(r",|;| y luego | y | luego | despues | después | then | and then | and ", txt)
    steps = [p.strip() for p in parts if p.strip()]
    # handle "pero solo despues de X" by merging if necessary - we will process conditions later
    return steps

# -------------------------
# Construcción de plan intermedio (lista de pasos con action/object/place/cond)
# -------------------------
def build_plan_steps(text):
    steps_raw = split_into_steps(text)
    plan_steps = []
    for step in steps_raw:
        tokens = [t.strip() for t in re.split(r"\s+", normalize(step))]
        actions = find_actions(tokens)
        objects = find_objects(step)
        places = find_places(step)
        # simple heuristics: pick first action found, first object/place
        if actions:
            verb_text, verb_type = actions[0]
        else:
            # fallback: try to derive from infinitives
            verb_type = None
            for tok in tokens:
                # Spanish infinitive heuristic
                if tok.endswith(("ar","er","ir")):
                    # map common endings to MAKE or PICK heuristically
                    if tok in ("hacer","preparar","cocinar"):
                        verb_type = "MAKE"
                    else:
                        verb_type = "DEFAULT"
                    break
            if verb_type is None:
                verb_type = "DEFAULT"
            verb_text = tokens[0] if tokens else "do"
        # detect conditional pre/post phrases (e.g., "pero solo después de hervir el agua")
        condition = None
        m = re.search(r"pero solo despu[eé]s de (.+)$", step)
        if not m:
            m = re.search(r"pero solo despues de (.+)$", step)
        if m:
            condition = m.group(1).strip()
        # detect "antes de X" => this step should be before X
        before_match = re.search(r"(.+) antes de (.+)$", step)
        if before_match:
            # treat as two-step: do before_match.group(1) then group(2)
            # We'll let split_into_steps have probably separated them; if not, leave condition
            pass

        plan_steps.append({
            "raw": step,
            "verb_text": verb_text,
            "action": verb_type,
            "object": objects[0] if objects else None,
            "place": places[0] if places else None,
            "condition": condition
        })
    return plan_steps

# -------------------------
# Generador de dominio dinámico (basado en las acciones presentes)
# -------------------------
def build_domain_for_actions(actions_present):
    """
    Construye un dominio que contiene definiciones para acciones comunes.
    Agrega step predicates (step-done-1, ... ) para forzar secuencia si es necesario.
    """
    # common predicates
    preds = [
        "  (:predicates",
        "    (at ?a - agent ?l - location)",
        "    (in ?o - object ?l - location)",
        "    (has ?a - agent ?o - object)",
        "    (prepared ?o - object)",
        "    (heated ?o - object)",
        "    (open ?p - object)",
        "    (closed ?p - object)",
        "    (charged ?o - object)",
        "    (clean ?o - object)",
        "    (neutralized ?t - target)",
    ]
    # add step predicates in case we want to enforce ordering; created dynamically later when used
    domain_actions = []

    # helper to add action templates for common action types
    def add_move():
        domain_actions.append("""
  (:action move
    :parameters (?a - agent ?from - location ?to - location)
    :precondition (at ?a ?from)
    :effect (and (not (at ?a ?from)) (at ?a ?to))
  )""")
    def add_pick():
        domain_actions.append("""
  (:action pick
    :parameters (?a - agent ?o - object ?l - location)
    :precondition (and (at ?a ?l) (in ?o ?l))
    :effect (and (not (in ?o ?l)) (has ?a ?o))
  )""")
    def add_place():
        domain_actions.append("""
  (:action place
    :parameters (?a - agent ?o - object ?l - location)
    :precondition (has ?a ?o)
    :effect (and (not (has ?a ?o)) (in ?o ?l))
  )""")
    def add_open():
        domain_actions.append("""
  (:action open
    :parameters (?a - agent ?p - object)
    :precondition ()
    :effect (open ?p)
  )""")
    def add_close():
        domain_actions.append("""
  (:action close
    :parameters (?a - agent ?p - object)
    :precondition ()
    :effect (closed ?p)
  )""")
    def add_use():
        domain_actions.append("""
  (:action use
    :parameters (?a - agent ?o - object ?t - object)
    :precondition (has ?a ?o)
    :effect ()
  )""")
    def add_prepare():
        domain_actions.append("""
  (:action prepare
    :parameters (?a - agent ?o - object ?ap - object)
    :precondition (has ?a ?o)
    :effect (prepared ?o)
  )""")
    def add_boil():
        domain_actions.append("""
  (:action boil
    :parameters (?a - agent ?o - object ?k - object)
    :precondition ()
    :effect (heated ?o)
  )""")
    def add_turn_on():
        domain_actions.append("""
  (:action turn_on
    :parameters (?a - agent ?d - object)
    :precondition ()
    :effect ()
  )""")
    def add_clean():
        domain_actions.append("""
  (:action clean
    :parameters (?a - agent ?o - object)
    :precondition ()
    :effect (clean ?o)
  )""")
    def add_charge():
        domain_actions.append("""
  (:action charge
    :parameters (?a - agent ?b - object)
    :precondition ()
    :effect (charged ?b)
  )""")
    def add_neutralize():
        domain_actions.append("""
  (:action neutralize
    :parameters (?a - agent ?t - target)
    :precondition ()
    :effect (neutralized ?t)
  )""")
    def add_locate():
        domain_actions.append("""
  (:action locate
    :parameters (?a - agent ?o - object ?l - location)
    :precondition ()
    :effect (in ?o ?l)
  )""")
    def add_deliver():
        domain_actions.append("""
  (:action deliver
    :parameters (?a - agent ?o - object ?from - location ?to - location)
    :precondition (and (in ?o ?from) (at ?a ?from))
    :effect (and (not (in ?o ?from)) (in ?o ?to))
  )""")
    def add_assemble():
        domain_actions.append("""
  (:action assemble
    :parameters (?a - agent ?part - object ?product - object)
    :precondition ()
    :effect ()
  )""")

    # Map action type to templates
    mapping = {
        "MOVE": add_move,
        "PICK": add_pick,
        "PLACE": add_place,
        "OPEN": add_open,
        "CLOSE": add_close,
        "USE": add_use,
        "MAKE": add_prepare,
        "COOK": add_prepare,
        "BOIL": add_boil,
        "TURN_ON": add_turn_on,
        "TURN_OFF": add_turn_on,
        "CLEAN": add_clean,
        "CHARGE": add_charge,
        "NEUTRALIZE": add_neutralize,
        "LOCATE": add_locate,
        "DELIVER": add_deliver,
        "TRANSFER": add_deliver,
        "BRING": add_deliver,
        "ASSEMBLE": add_assemble,
        "REPAIR": add_assemble,
        "REMOVE": add_assemble,
        "REPLACE": add_assemble
    }

    for a in sorted(set(actions_present)):
        fn = mapping.get(a)
        if fn:
            fn()
        else:
            # add a generic action for unknown ones
            domain_actions.append(f"""
  (:action {a.lower()}
    :parameters (?a - agent ?x - object)
    :precondition ()
    :effect ()
  )""")

    # close predicates list
    preds.append("  )")
    domain = "(define (domain generated_domain)\n  (:requirements :strips :typing)\n  (:types agent object location target)\n"
    domain += "\n".join(preds) + "\n"
    domain += "\n".join(domain_actions) + "\n)\n"
    return domain

# -------------------------
# Construcción de problem específico
# -------------------------
def build_problem_from_steps(steps, metadata=None):
    """
    steps: lista ordenada de dicts {action, object, place, condition, raw}
    Crea objetos, init facts y goal(s) adaptados.
    """
    objs = set()
    locs = set()
    init = []
    goals = []
    # default agent and home
    objs.add("robot")
    locs.add("home")

    # track steps to create ordered sub-goals if necessary
    step_index = 0
    for s in steps:
        step_index += 1
        action = s.get("action", "DEFAULT")
        obj = s.get("object")
        place = s.get("place")
        raw = s.get("raw", "")
        # normalize names
        if obj:
            objname = obj.replace(" ", "_")
            objs.add(objname)
        else:
            objname = None
        if place:
            place_name = place.replace(" ", "_")
            locs.add(place_name)
        else:
            place_name = None

        # Decide init facts and goals per action type
        if action in ("PICK","PICK_UP","PICKUP"):
            # object must be at a location -> goal: has robot object
            if not place_name:
                # if no place, assume object is at home
                init.append(f"(in {objname} home)")
            else:
                init.append(f"(in {objname} {place_name})")
            goals.append(f"(has robot {objname})")
        elif action in ("PLACE","PUT","TRANSFER","BRING","DELIVER"):
            # goal: object at place_name
            if place_name:
                goals.append(f"(in {objname} {place_name})")
            else:
                # if no destination, place at home
                goals.append(f"(in {objname} home)")
        elif action in ("OPEN",):
            goals.append(f"(open {objname or 'door'})")
        elif action in ("CLOSE",):
            goals.append(f"(closed {objname or 'door'})")
        elif action in ("MAKE","COOK","PREPARE","BOIL"):
            # goal: prepared <object>
            target = objname or ("dish" + str(step_index))
            goals.append(f"(prepared {target})")
        elif action in ("TURN_ON",):
            goals.append(f"(on {objname or 'device'})")
        elif action in ("CHARGE",):
            goals.append(f"(charged {objname or 'battery'})")
        elif action in ("CLEAN",):
            goals.append(f"(clean {objname or 'object'})")
        elif action in ("NEUTRALIZE",):
            # neutralize target: use target type predicate
            target = objname or ("target" + str(step_index))
            goals.append(f"(neutralized {target})")
        elif action in ("LOCATE", "FIND"):
            # goal: object at some known place
            goals.append(f"(in {objname or 'object'} {place_name or 'home'})")
        elif action in ("DELIVER",):
            goals.append(f"(in {objname} {place_name or 'home'})")
        else:
            # generic
            goals.append(f"(done robot)")

    # Build objects and init strings
    objects_decl = []
    if objs:
        objects_decl.append(" ".join(sorted(objs)) + " - object") if len(objs)>0 else None
    if locs:
        # list locations separately
        objects_decl.append(" ".join(sorted(locs)) + " - location")

    # ensure there's at least some objects
    if not objects_decl:
        objects_decl = ["robot - agent", "home - location"]

    # Compose init
    init_lines = ""
    if init:
        for f in init:
            init_lines += f"    {f}\n"
    else:
        init_lines = "    (at robot home)\n"

    # Compose goal: if multiple goals, set as conjunction
    goal_lines = ""
    if len(goals) == 1:
        goal_block = f"{goals[0]}"
    else:
        # prefer to require last goal if it's a sequence; but also allow conjunction — here we use conjunction
        goal_block = "(and\n"
        for g in goals:
            goal_block += f"    {g}\n"
        goal_block += ")"

    # final problem text
    objects_text = "\n  (:objects " + "\n    " + "\n    ".join(objects_decl) + ")\n"
    problem = f"""(define (problem generated-problem)
  (:domain generated_domain)
  {objects_text}
  (:init
{init_lines}  )
  (:goal {goal_block})
)
"""
    return problem

# -------------------------
# API method: main generator
# -------------------------
def generate_pddl_from_instruction(nl_text):
    """
    Entrada: cadena en ES/EN
    Salida: dict {domain, problem, meta}
    """
    raw = nl_text or ""
    text = normalize(raw)

    steps = build_plan_steps(text)
    # create domain based on actions present
    actions_present = [s.get("action","DEFAULT") for s in steps]
    domain_text = build_domain_for_actions(actions_present)
    problem_text = build_problem_from_steps(steps)

    meta = {
        "raw": raw,
        "normalized": text,
        "steps": steps,
        "actions_present": actions_present
    }
    return {"domain": domain_text, "problem": problem_text, "meta": meta}

# -------------
# Ejemplos rápidos (si ejecutas este archivo directamente para pruebas)
# -------------
if __name__ == "__main__":
    examples = [
        "El robot debe recoger una manzana de la mesa.",
        "El agente debe ir al cuarto y encender la luz.",
        "El robot debe llevar un libro desde la mesa hasta la estantería.",
        "El robot debe preparar te, pero solo despues de hervir el agua en la tetera.",
        "El robot debe cocinar pasta: llenar la olla, hervir el agua y luego anadir la pasta."
    ]
    for ex in examples:
        out = generate_pddl_from_instruction(ex)
        print("IN:", ex)
        print("--- DOMAIN ---")
        print(out["domain"])
        print("--- PROBLEM ---")
        print(out["problem"])
        print("--- META ---")
        print(out["meta"])
        print("\n" + "="*60 + "\n")
