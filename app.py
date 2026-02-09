from flask import Flask, render_template, request, jsonify
from data import SCHOOL_DATA, CONTACT

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def find_answer(user_msg):
    msg = user_msg.lower()

    # 1️⃣ Check exact keyword matches
    for key, answer in SCHOOL_DATA.items():
        if key in msg:
            return answer

    # 2️⃣ Special handling for "fee" related queries
    if "fee" in msg or "fees" in msg or "charge" in msg:
        for key in SCHOOL_DATA:
            if "fee" in key:
                # Check if class name or bus route is in the message
                if any(c in msg for c in key.split()):
                    return SCHOOL_DATA[key]
        # fallback for general fee query
        return f"School fees information is not specific. Kripya in numbers par contact karein {CONTACT['numbers']}."

    # 3️⃣ Special handling for "bus" queries
    if "bus" in msg or "transport" in msg:
        for key in SCHOOL_DATA:
            if "bus" in key:
                if any(c in msg for c in key.split()):
                    return SCHOOL_DATA[key]
        return f"Bus information is not specific. Kripya in numbers par contact karein {CONTACT['numbers']}."

    # 4️⃣ Special handling for staff queries
    if "receptionist" in msg or "guard" in msg or "peon" in msg:
        for key in SCHOOL_DATA:
            if key in msg:
                return SCHOOL_DATA[key]
        return f"Staff information ke liye kripya contact karein {CONTACT['numbers']}."

    # 5️⃣ Fallback
    return f"Is question ka jawab available nahi hai. Kripya in numbers par contact karein {CONTACT['numbers']} ya school visit karein."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    answer = find_answer(user_msg)
    return jsonify({"reply": f"Sinoy:-- {answer}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
