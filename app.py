import os
import json
from flask import Flask, render_template, request, jsonify
import openai
import dotenv

dotenv.load_dotenv()
app = Flask(__name__, static_folder="static", template_folder="templates")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Quiz data for Lessons
QUIZ_DATA = {
    "part1": {
        "title": "Part 1: General Knowledge on Somalia",
        "cards": [
            {"question": "What is the capital city of Somalia?", "answer": "Mogadishu"},
            {"question": "What is Somalia's official currency?", "answer": "Somali shilling"},
            {"question": "Which body of water borders Somalia to the east?", "answer": "Indian Ocean"},
            {"question": "What is the official language of Somalia?", "answer": "Somali and Arabic"},
            {"question": "What year did Somalia gain independence?", "answer": "1960"},
            {"question": "What is the largest city in Somalia?", "answer": "Mogadishu"},
            {"question": "Which continent is Somalia located in?", "answer": "Africa"}
        ]
    },
    "part2": {
        "title": "Part 2: Somali Language Basics",
        "cards": [
            {"question": "How do you say 'Hello' in Somali?", "answer": "Salaam"},
            {"question": "How do you say 'Thank you' in Somali?", "answer": "Mahadsanid"},
            {"question": "What is the Somali word for 'water'?", "answer": "Biyo"},
            {"question": "How do you say 'Good morning' in Somali?", "answer": "Subax wanaagsan"},
            {"question": "How do you say 'Yes' in Somali?", "answer": "Haa"},
            {"question": "How do you say 'No' in Somali?", "answer": "Maya"},
            {"question": "What does 'Nabad' mean in Somali?", "answer": "Peace"}
        ]
    },
    "part3": {
        "title": "Part 3: Somali History",
        "cards": [
            {"question": "In what year did Somalia gain independence?", "answer": "1960"},
            {"question": "Which ancient trading civilization was centered in present-day Somalia?", "answer": "Punt"},
            {"question": "What was the name of the 15th century state that existed in northern Somalia and eastern Ethiopia?", "answer": "Adal Sultanate"},
            {"question": "When did Somalia's civil war begin?", "answer": "1991"},
            {"question": "Who was the last president of the Somali Democratic Republic?", "answer": "Siad Barre"},
            {"question": "What year was the Transitional Federal Government of Somalia established?", "answer": "2004"},
            {"question": "What international mission was deployed to Somalia in the early 1990s?", "answer": "UNOSOM — United Nations Operation in Somalia"}
        ]
    },
    "part4": {
        "title": "Part 4: Somali Culture and Traditions",
        "cards": [
            {"question": "What is the traditional Somali nomadic dwelling called?", "answer": "Aqal — a portable dome-shaped hut made from wood and woven grass"},
            {"question": "What is the most popular sport in Somalia?", "answer": "Football (soccer)"},
            {"question": "What is 'Xeer' in Somali culture?", "answer": "A traditional system of customary law and social contracts between clans"},
            {"question": "What is the traditional Somali greeting?", "answer": "Salaam Alaykum — meaning 'Peace be upon you'"},
            {"question": "What is 'Suqaar'?", "answer": "A popular Somali dish of small pieces of meat stir-fried with vegetables and spices"},
            {"question": "What instrument is central to Somali traditional music?", "answer": "The kaban — a type of lute or guitar used in Somali folk music"},
            {"question": "What is 'Shaah' in Somalia?", "answer": "Spiced Somali tea, often made with cardamom, cinnamon and cloves — a daily staple"}
        ]
    },
    "part5": {
        "title": "Part 5: Mogadishu Landmarks and Geography",
        "cards": [
            {"question": "What was Mogadishu's historical nickname?", "answer": "The White Pearl of the Indian Ocean"},
            {"question": "What is Lido Beach?", "answer": "Mogadishu's famous sandy beach on the Indian Ocean, a popular gathering spot for locals"},
            {"question": "What is the Bakaara Market?", "answer": "One of the largest and most famous markets in Mogadishu, known for trading goods and produce"},
            {"question": "What ocean borders Mogadishu to the east?", "answer": "The Indian Ocean"},
            {"question": "What is the Mosque of Islamic Solidarity?", "answer": "One of the largest mosques in Africa, located in Mogadishu — a major landmark"},
            {"question": "What was the name of Mogadishu's famous hotel rebuilt after the war?", "answer": "The Peace Hotel — a symbol of Mogadishu's reconstruction and revival"},
            {"question": "What ancient trading civilisation was centred in present-day Somalia?", "answer": "The Land of Punt — one of the earliest known trading civilisations in history"}
        ]
    },
    "part6": {
        "title": "Part 6: Somalia's Recovery and Modern Development",
        "cards": [
            {"question": "What is EVC Plus?", "answer": "A mobile money service by Hormuud Telecom — one of the most widely used in the world, allowing Somalis to bank without a traditional bank account"},
            {"question": "What was Somalia's estimated GDP growth in 2022?", "answer": "2.8% — reported by the African Development Bank despite drought and inflation challenges"},
            {"question": "Which organisation reported Somalia as a top performer in mobile money?", "answer": "GSMA — the Global System for Mobile Communications Association"},
            {"question": "What does the term 'leapfrogging' mean in Somalia's context?", "answer": "Skipping traditional banking infrastructure and going straight to mobile money technology"},
            {"question": "When did Somali piracy peak and then decline?", "answer": "Peaked around 2007–2012, then declined dramatically — near-zero incidents by 2017"},
            {"question": "What is the Federal Government of Somalia?", "answer": "The internationally recognised central government re-established after years of civil conflict"},
            {"question": "What sector has driven much of Somalia's economic recovery?", "answer": "Telecommunications — particularly mobile money and internet services"}
        ]
    },
    "part7": {
        "title": "Part 7: Somali Language — Intermediate",
        "cards": [
            {"question": "How do you say 'Where is the beach?' in Somali?", "answer": "Xagee bay tahay xeebta?"},
            {"question": "How do you say 'How much does this cost?' in Somali?", "answer": "Imisa ayay tahay?"},
            {"question": "What does 'Waan jeclahay' mean?", "answer": "I love it / I like it"},
            {"question": "How do you say 'My name is...' in Somali?", "answer": "Magacaygu waa..."},
            {"question": "What does 'Nabad gelyo' mean?", "answer": "Goodbye — literally meaning 'Go in peace'"},
            {"question": "How do you say 'I don't understand' in Somali?", "answer": "Ma fahmin"},
            {"question": "What does 'Adduunka waa qurux' mean?", "answer": "The world is beautiful"}
        ]
    }
}

# --- Page Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mohammed')
def mohammed():
    return render_template('mohammed.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/itinerary')
def itinerary():
    return render_template('itinerary.html')

@app.route('/gallery-carousel')
def gallery_carousel():
    return render_template('gallery_carousel.html')

@app.route('/currency')
def currency():
    return render_template('currency.html')

@app.route('/lessons')
def lessons():
    parts = [
        {"id": "part1", "title": QUIZ_DATA["part1"]["title"]},
        {"id": "part2", "title": QUIZ_DATA["part2"]["title"]},
        {"id": "part3", "title": QUIZ_DATA["part3"]["title"]},
        {"id": "part4", "title": QUIZ_DATA["part4"]["title"]},
        {"id": "part5", "title": QUIZ_DATA["part5"]["title"]},
        {"id": "part6", "title": QUIZ_DATA["part6"]["title"]},
        {"id": "part7", "title": QUIZ_DATA["part7"]["title"]},
    ]
    return render_template('lessons.html', parts=parts)

@app.route('/lessons/<part_id>')
def quiz(part_id):
    part = QUIZ_DATA.get(part_id)
    if not part:
        return "Quiz part not found", 404
    return render_template(
        'quiz.html',
        title=part["title"],
        cards_json=json.dumps(part["cards"])
    )

# --- API Endpoints ---

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    base_prompt = (
        "You are the best Somali travel guide in the world. You also speak Somali and English. "
        "Make sure to remind users you can speak both. You can utilize the web to answer queries."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": base_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {e}"
    return jsonify({'reply': reply})

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json() or {}
    print("Received data:", data)

    personality = data.get('personality', '')
    days = data.get('days', '')
    habits = data.get('habits', '')
    pace = data.get('pace', 'moderate')

    prompt = (
        f"Create a personalized, highly detailed itinerary for a traveler visiting Mogadishu exclusively.\n"
        f"Length of stay: {days} days\n"
        f"Personality: {personality}\n"
        f"Holiday habits: {habits}\n"
        f"Preferred pace: {pace}\n\n"
        "Provide a day-by-day plan labeled Day 1, Day 2, etc. Under each day, list bullet points in the format:\n"
        "- HH:MM AM/PM - Activity description\n"
        "Use specific local landmarks and cultural experiences in Mogadishu."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a travel planning assistant for Mogadishu."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
        )
        itinerary = response.choices[0].message.content.strip()
    except Exception as e:
        itinerary = f"Error: {str(e)}"

    return jsonify({'itinerary': itinerary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)