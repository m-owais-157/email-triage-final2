from fastapi import FastAPI

app = FastAPI()

emails = [
    {"id": 1, "text": "Urgent: Your bank account needs verification", "label": "important"},
    {"id": 2, "text": "You won a lottery! Claim now", "label": "spam"},
    {"id": 3, "text": "Meeting scheduled for tomorrow", "label": "normal"}
]

state = {"step": 0}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metadata")
def metadata():
    return {
        "name": "Email Triage Environment",
        "description": "Classify emails into spam, important, or normal"
    }


@app.get("/schema")
def schema():
    return {
        "action": {"email_id": "int", "label": "string"},
        "state": {"step": "int"},
        "observation": {"emails": "list"}
    }


@app.post("/reset")
def reset():
    state["step"] = 0
    return {"state": {"emails": emails, "step": 0}}


@app.post("/step")
def step(action: dict):
    email_id = action.get("email_id")
    label = action.get("label")

    email = next((e for e in emails if e["id"] == email_id), None)

    if not email:
        return {"state": state, "reward": -1, "done": False, "info": {"error": "Invalid email_id"}}

    correct = email["label"]

    if label == correct:
        reward = 2
    elif correct == "spam":
        reward = -3
    else:
        reward = -1

    state["step"] += 1

    return {
        "state": state,
        "reward": reward,
        "done": state["step"] >= len(emails),
        "info": {"correct_label": correct}
    }


@app.get("/state")
def get_state():
    return {"state": state}
