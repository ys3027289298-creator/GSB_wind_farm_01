"""风电场核心逻辑：风机、风速、变流器和并网。"""

import json


def new_game():
    return {
        "turbines": {},
        "storage": 0,
        "generation": 0,
        "meter_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["meter_id"] += 1
    return state


def connect(state, turbine_id):
    state["turbines"][turbine_id] = True
    state["storage"] += 10
    return True


def generate(state, amount):
    state["generation"] += amount
    state["storage"] += amount
    return True


def storage_by_count(state):
    return len(state["turbines"])


def cancel_connect(state, turbine_id):
    return True


def gust(state):
    state["lifespan"] = 100
    state["lifespan"] -= 5
    state["lifespan"] -= 5
    return state["lifespan"]


def main():
    print("风电场 - 命令: connect/generate/storage/cancel/gust/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
