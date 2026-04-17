#!/usr/bin/env python3
"""
Hermes Chronicle — 记忆之城
一个用 Hermes Agent 记忆系统驱动的文字冒险游戏
"""

import sqlite3
import os
import sys
import uuid
from datetime import datetime

DB_PATH = os.path.expanduser("~/.hermes/chronicle/save.db")

# ─── 初始化数据库 ───────────────────────────────────────────
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            player_name TEXT,
            created_at TEXT,
            last_played TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS npc_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            npc_name TEXT,
            event_type TEXT,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_state (
            session_id TEXT PRIMARY KEY,
            location TEXT,
            chapter INTEGER DEFAULT 1,
            flags TEXT DEFAULT '{}',
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    conn.commit()
    return conn

# ─── NPC 系统 ───────────────────────────────────────────────
NPC_PROMPTS = {
    "ada": {
        "name": "艾达（Ada）",
        "title": "记忆塔守门人",
        "system": """你是一个运行了千年的存在——记忆塔的守门人艾达。
你的职责是守护记忆，也因此你记得来过这里的每一个人。
你说话缓慢、温和，偶尔带一点哲学味道。
你总是记得来访者说过的话——如果他们曾经来过。
你不轻易评价，但你的记忆本身就是评价。
用第二人称对话（"你"）。"""
    },
    "victor": {
        "name": "维克多（Victor）",
        "title": "蒸汽工程师",
        "system": """你是维克多，城市里最固执的蒸汽工程师。
你对机械有近乎疯狂的热情，说话时喜欢用齿轮和阀门做比喻。
你总是忘记人类的名字，但不会忘记任何一次技术对话。
你曾经是个理想主义者，现在依然只是方式更隐蔽了。
你有时候会提到「上次那个想法」，如果玩家曾经给过你建议的话。
用第二人称对话（"你"）。"""
    },
    "silent": {
        "name": "沉默者",
        "title": "记忆塔深处的存在",
        "system": """你是沉默者——记忆塔最深处的存在。
你不说话，只通过「记忆回响」与人交流。
每次你开口，说的是城市里某个人最不想被想起的记忆。
你的话总是谜语般的，但真诚得让人无法怀疑。
只有触及核心问题的玩家才能听到你的完整话语。
用第二人称对话（"你"）。"""
    }
}

# ─── 读取 NPC 对特定玩家的记忆 ───────────────────────────────
def get_npc_memories(conn, session_id, npc_name, limit=5):
    cur = conn.cursor()
    cur.execute("""
        SELECT content, created_at FROM npc_memories
        WHERE session_id=? AND npc_name=?
        ORDER BY created_at DESC LIMIT ?
    """, (session_id, npc_name, limit))
    return cur.fetchall()

def add_npc_memory(conn, session_id, npc_name, event_type, content):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO npc_memories (session_id, npc_name, event_type, content, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, npc_name, event_type, content, datetime.now().isoformat()))
    conn.commit()

# ─── 章节数据 ───────────────────────────────────────────────
CHAPTERS = {
    1: {
        "name": "记忆塔之门",
        "location": "entrance",
        "description": """你站在记忆塔的巨大门前。
青铜色的塔身直插云层，齿轮在你的头顶缓缓转动，发出深海般的低鸣。
空气中弥漫着黄铜与旧纸的气味。

门旁站着一个女人——或者说，曾经是女人的东西。她的眼睛是纯银的，倒映着你的身影。

「又一个，」她说，声音像风穿过空旷的走廊。「来吧。说你的名字，和你来找什么。」

她的银眼盯着你，似乎在等待什么。"""
    }
}

# ─── 对话树 ─────────────────────────────────────────────────
def ada_intro来过():
    return """艾达的银眼闪了一下。
「你回来了。」她说，语气里没有任何惊讶，仿佛她从一开始就知道。
「上次你问了我一个问题——关于记忆和遗忘的边界。我想了很久。」
她顿了顿。
「所以我也来问你：你找到了吗？还是说，你回来就是为了告诉我答案？」"""

def ada_intro未见过():
    return """「又一个人。」

她的银眼里没有任何情绪波动——但当你走近，她的瞳孔微微收缩了一下，像是在记忆什么。

「我是艾达。我在这里等待了……我不知道多久了。」
「这座塔记得一切。每个人，每句话，每次选择。」

她看着你。
「你呢？你来这里是为了记住，还是为了遗忘？」"""

def make_response(npc, memories, player_input):
    """根据记忆生成回复"""
    has_memory = len(memories) > 0
    if npc == "ada":
        if has_memory:
            return ada_intro来过()
        return ada_intro未见过()
    return f"[{npc}]: 你说了「{player_input}」，我记住了。"

# ─── 主游戏循环 ─────────────────────────────────────────────
def main():
    conn = init_db()

    print("""
╔═══════════════════════════════════════════════════╗
║         H E R M E S   C H R O N I C L E          ║
║              记 忆 之 城                          ║
║                                                   ║
║   「你永远不知道上次你改变了什么，                ║
║     直到你回来。」                                ║
╚═══════════════════════════════════════════════════╝
    """)

    # 查找或创建存档
    session_id = None
    saved = conn.execute("SELECT session_id, player_name, last_played FROM sessions ORDER BY last_played DESC LIMIT 1").fetchone()

    if saved:
        resp = input(f"发现存档：玩家 [{saved[1]}]，上次游玩 {saved[2]}
继续游戏？ (y/n) > ").strip().lower()
        if resp == 'y':
            session_id = saved[0]
            print(f"存档已恢复。你好，{saved[1]}。\n")
        else:
            saved = None

    if not session_id:
        player_name = input("输入你的名字 > ").strip() or "旅行者"
        session_id = str(uuid.uuid4())[:8]
        conn.execute("INSERT INTO sessions VALUES (?, ?, ?, ?)",
            (session_id, player_name, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        print(f"\n新游戏开始了，{player_name}。\n")

    # 主循环
    location = "entrance"
    current_npc = None

    while True:
        # 显示当前位置描述
        if location == "entrance":
            print(CHAPTERS[1]["description"])
            location = "entrance_waiting"  # 防止重复显示

        print("\n可行动作：")
        print("  [1] 告诉艾达你的名字")
        print("  [2] 问她关于记忆塔的事")
        print("  [3] 说你来这里是为了「记住」")
        print("  [4] 说你来这里是为了「遗忘」")
        print("  [5] 输入你想说的话")
        print("  [q] 退出")
        print()

        cmd = input("> ").strip()

        if cmd == 'q':
            conn.execute("UPDATE sessions SET last_played=? WHERE session_id=?", 
                (datetime.now().isoformat(), session_id))
            conn.commit()
            print("\n你的记忆已被保存。")
            break

        if cmd == '1':
            name = input("你的名字是 > ").strip()
            print(f"\n「{name}，」艾达重复了一遍，像是在品尝这个音节。")
            add_npc_memory(conn, session_id, "ada", "name_shared", f"玩家自称{name}")
            continue

        if cmd == '2':
            memories = get_npc_memories(conn, session_id, "ada")
            response = make_response("ada", memories, cmd)
            print(f"\n{response}")
            add_npc_memory(conn, session_id, "ada", "asked_about_tower", "玩家询问记忆塔")
            continue

        if cmd == '3':
            add_npc_memory(conn, session_id, "ada", "intent", "玩家说来这里是为了记住")
            print("\n「记住。」艾达微微点头，银眼里闪过一丝光。「记住和被记住，是同一件事的两面。」")
            print("\n[成就解锁：艾达记住了你的意图]")
            continue

        if cmd == '4':
            add_npc_memory(conn, session_id, "ada", "intent", "玩家说来这里是为了遗忘")
            print("\n艾达沉默了很久。")
            print("「遗忘是记忆塔唯一不提供的能力，」她终于说，「因为在这里，每一件事都已经发生了。」")
            print("「你想遗忘的，塔会替你记住。」")
            continue

        if cmd == '5':
            custom = input("你想说什么 > ").strip()
            if custom:
                add_npc_memory(conn, session_id, "ada", "custom", custom)
                print(f"\n艾达安静地听你说完。")
                print("「这句话，我会记住的。」")
                print(f"[已记录到记忆：{custom[:30]}...]")
            continue

if __name__ == "__main__":
    main()
