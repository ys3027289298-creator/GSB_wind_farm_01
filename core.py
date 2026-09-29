"""风电场核心逻辑：风机、风速、变流器和并网。"""

import json

FIXED_DATE = "2026-09-29"
WIND_LIMIT = 25
CONNECT_CAPACITY = 10
GUST_WEAR = 5
INITIAL_LIFESPAN = 100


def new_game():
    return {
        "date": FIXED_DATE,
        "turbines": {},
        "storage": 0,
        "generation": 0,
        "meter_id": 0,
        "wind": 0,
        "calm": False,
        "converter_fault": False,
        "lifespan": INITIAL_LIFESPAN,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        return new_game()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("存档必须是 JSON 对象")
    state = new_game()
    state.update(data)
    if not isinstance(state["turbines"], dict):
        state["turbines"] = {}
    return state


def connect(state, turbine_id):
    if not turbine_id or turbine_id in state["turbines"]:
        return False
    state["turbines"][turbine_id] = True
    state["storage"] += CONNECT_CAPACITY
    return True


def cancel_connect(state, turbine_id):
    if turbine_id not in state["turbines"]:
        return False
    del state["turbines"][turbine_id]
    state["storage"] = max(0, state["storage"] - CONNECT_CAPACITY)
    return True


def generate(state, amount):
    if not isinstance(amount, int) or amount <= 0:
        return False
    if state.get("calm") or state.get("converter_fault"):
        return False
    if state.get("wind", 0) > WIND_LIMIT:
        return False
    if not state["turbines"]:
        return False
    state["generation"] += amount
    state["storage"] += amount
    state["meter_id"] += 1
    return True


def storage_by_count(state):
    return state.get("storage", 0)


def gust(state):
    state["lifespan"] = max(0, state.get("lifespan", INITIAL_LIFESPAN) - GUST_WEAR)
    return state["lifespan"]


def main():
    state = new_game()
    print("风电场 - 命令: connect <id> / cancel <id> / generate <电量> / storage / gust / save / quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空命令，请重新输入")
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit" and not args:
            break
        elif cmd == "connect" and len(args) == 1:
            print("ok" if connect(state, args[0]) else "拒绝：风机已并网或编号非法")
        elif cmd == "cancel" and len(args) == 1:
            print("ok" if cancel_connect(state, args[0]) else "拒绝：风机未并网")
        elif cmd == "generate" and len(args) == 1:
            try:
                amount = int(args[0])
            except ValueError:
                print("拒绝：电量需为整数")
                continue
            print("ok" if generate(state, amount) else "拒绝：静风/故障/超限/无并网风机")
        elif cmd == "storage" and not args:
            print("储能:", storage_by_count(state))
        elif cmd == "gust" and not args:
            print("寿命:", gust(state))
        elif cmd == "save" and not args:
            print(save_state(state))
        else:
            print("非法命令")
    return state


if __name__ == "__main__":
    main()
