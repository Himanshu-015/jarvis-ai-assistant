memory = []

def add_memory(role, text):
    memory.append({"role": role, "content": text})
    if len(memory) > 6:   # sirf last 6 messages
        memory.pop(0)

def get_memory():
    context = ""
    for m in memory:
        context += f"{m['role']}: {m['content']}\n"
    return context
