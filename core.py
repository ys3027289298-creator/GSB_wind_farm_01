"""风电场核心逻辑：风机、风速、变流器和并网。"""

import json

CUT_OUT_WIND = 25
CONNECT_ENERGY = 10
DEFAULT_LIFESPAN = 100
GUST_WEAR = 5
DEMO_DATE = "2026-09-29"


def new_game():
    return {
        "turbines": {},
        "storage": 0,
        "generation": 0,
        "meter_id": 0,
        "lifespan": DEFAULT_LIFESPAN,
        "wind": 0,
        "calm": False,
        "converter_fault": False,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        raise ValueError("存档数据为空")
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("存档格式非法")
    for key, default in new_game().items():
        state.setdefault(key, default)
    return state


def connect(state, turbine_id):
    if not turbine_id or turbine_id in state["turbines"]:
        return False
    state["turbines"][turbine_id] = True
    state["storage"] += CONNECT_ENERGY
    state["meter_id"] += 1
    return True


def cancel_connect(state, turbine_id):
    if turbine_id not in state["turbines"]:
        return False
    del state["turbines"][turbine_id]
    state["storage"] = max(0, state["storage"] - CONNECT_ENERGY)
    return True


def generate(state, amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return False
    if state.get("converter_fault"):
        return False
    if state.get("calm"):
        return False
    if state.get("wind", 0) > CUT_OUT_WIND:
        return False
    state.setdefault("generation", 0)
    state.setdefault("storage", 0)
    state["generation"] += amount
    state["storage"] += amount
    return True


def storage_by_count(state):
    return state.get("storage", 0)


def gust(state):
    state["lifespan"] = state.get("lifespan", DEFAULT_LIFESPAN) - GUST_WEAR
    return state["lifespan"]


def main():
    state = new_game()
    print("风电场 (%s) - 命令: connect <id> / cancel <id> / generate <电量> / storage / gust / save / load / quit" % DEMO_DATE)
    archive = ""
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空命令，已忽略")
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        elif cmd == "connect" and len(args) == 1:
            print("ok" if connect(state, args[0]) else "重复并网，已忽略")
        elif cmd == "cancel" and len(args) == 1:
            print("ok" if cancel_connect(state, args[0]) else "风机未并网，已忽略")
        elif cmd == "generate" and len(args) == 1:
            try:
                amount = float(args[0])
            except ValueError:
                print("电量必须是数字")
                continue
            print("ok" if generate(state, amount) else "发电被拒绝（故障/静风/超限/非法电量）")
        elif cmd == "storage" and not args:
            print("储能:", storage_by_count(state))
        elif cmd == "gust" and not args:
            print("阵风，剩余寿命:", gust(state))
        elif cmd == "save" and not args:
            archive = save_state(state)
            print("已存档")
        elif cmd == "load" and not args:
            if not archive:
                print("无存档可读")
            else:
                state = load_state(archive)
                print("已读档")
        else:
            print("非法命令")
    print("bye")


if __name__ == "__main__":
    main()
