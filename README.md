# Hermes Chronicle — 记忆之城

<p align="center">
  <img src="https://img.shields.io/badge/stars-95K-FFD700?style=for-the-badge" alt="95K GitHub Stars">
  <img src="https://img.shields.io/badge/Memory%20System-SQLite+GPT-blue?style=for-the-badge" alt="Memory System">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge" alt="Platform">
</p>

**"The AI that never forgets you." — Now you can see why.**

Hermes Chronicle is a text adventure game that demonstrates what makes Hermes Agent unique: **a persistent memory system that actually works across sessions**.

When you talk to an NPC, it remembers. Not just for one conversation — **forever**. Come back a week later, and the NPC will ask about "that thing you told me last time."

---

## ✦ The Problem Every AI User Knows

You spend 3 days refining a complex prompt. You get it perfect. Tomorrow you open a new session:

```
AI: "Hello! How can I help you today?"
You: [have to re-explain everything from scratch]
```

Every AI assistant has this problem. Hermes Agent was built to solve it.

**Hermes Chronicle is a playable demonstration of that solution.**

---

## ✦ What Makes Chronicle Different

| Feature | Regular Text Adventure | Hermes Chronicle |
|---------|----------------------|------------------|
| NPC Memory | Resets every session | Persists **forever** |
| Player History | Gone after game restart | Stored in SQLite |
| Context | One conversation at a time | Full session graph |
| World State | Hard-coded | Learns from your choices |

---

## ✦ Screenshots

```
═══════════════════════════════════════════════════
        记 忆 之 城 — H E R M E S  C H R O N I C L E
═══════════════════════════════════════════════════

  [艾达] 记忆塔守门人

  "啊……你回来了。"
  "我记得你。上一次你来的时候，问了我关于这座塔的来历。"
  "你说你要找到真相。"
  "你带来了新的线索吗？"

  ────────────────────────────────────────────────
  1. 询问记忆塔的历史
  2. 告诉她你最近的发现
  3. 询问沉默者的事情
  4. [自由对话]
```

---

## ✦ Quick Start

```bash
# Clone
git clone https://github.com/NousResearch/hermes-agent
cd hermes-agent/projects/chronicle

# Install dependencies
pip install openai

# Set your API key
export OPENAI_API_KEY=sk-your-key-here

# Run
python chronicle.py
```

**Requirements:** Python 3.8+ | OpenAI API key (or any compatible endpoint)

---

## ✦ How the Memory System Works

Every conversation with an NPC is stored in a SQLite database:

```python
# When you talk to an NPC, it writes to this table:
CREATE TABLE npc_memories (
    npc_name TEXT,        # Which NPC remembers
    event_type TEXT,       # 'conversation', 'choice', 'discovery'
    content TEXT,          # What was said/done
    created_at TEXT        # Timestamp
);
```

Next time you talk to that NPC, it loads your history and generates responses that reference your shared past.

**This is the same memory system powering Hermes Agent — now you can see it in action.**

---

## ✦ The Three Characters

**艾达 (Ada)** — The Gatekeeper of Memory
> "I remember everyone who has ever walked through these doors. Including you."

**维克多 (Victor)** — The Steam Engineer
> "I may forget names, but I never forget a good idea. Or a bad one."

**沉默者 (The Silent One)** — The Deep Presence
> Speaks only in echoes of memories. Knows things about you that you have forgotten.

---

## ✦ For Developers

Hermes Chronicle is a reference implementation of the Hermes memory architecture:

- **SessionDB** — SQLite with FTS5 for full-text search across your conversation history
- **NPC Memory** — Per-NPC persistent memory that survives session boundaries  
- **State Machine** — Game state persisted to disk, resumable at any time

The code is designed to be read and extended. After playing, read `chronicle.py` — it's ~250 lines and documents the entire memory architecture.

---

## ✦ Star the Parent Project

Hermes Chronicle is a demonstration of **Hermes Agent** — the AI that never forgets you.

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/★%20Hermes%20Agent-95K%20Stars-FFD700?style=for-the-badge&logo=github" alt="Star Hermes Agent">
  </a>
</p>

**95,000+ developers** use Hermes Agent for its memory, skills, and cross-platform deployment.

---

## ✦ License

MIT — built by [Nous Research](https://nousresearch.com)
