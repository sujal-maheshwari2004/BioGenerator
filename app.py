from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key=OPENAI_API_KEY
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_bio', methods=['POST'])
def generate_bio():
    data = request.json
    career = data.get('career', [])
    personality = data.get('personality', [])
    interests = data.get('interests', [])
    relationship_goals = data.get('relationship_goals', [])

    # Bio Samples for N-shot prompting
    bio_samples = [
        "The Adventurous Foodie: Globe-trotting architect with a passion for spicy food and sustainable design. Seeking a fellow adventurer who can appreciate a good biryani and a thought-provoking conversation.",
        "The Creative Bookworm: Introverted writer with a love for classic literature and indie coffee shops. Looking for someone who can match my wit and charm over a cup of chai and a deep discussion about our favorite novels.",
        "The Sporty Entrepreneur: Energetic entrepreneur with a passion for fitness and outdoor adventures. Seeking a partner who can keep up with my active lifestyle and shares my love for hiking, biking, and trying new things.",
        "The Compassionate Musician: Soulful musician with a heart for social justice and a love for live music. Looking for a kind and compassionate partner who enjoys jamming out at concerts and making a difference in the world.",
        "The Tech-Savvy Gamer: Software engineer by day, gamer by night. I'm equally comfortable debugging code and exploring virtual worlds. Seeking a partner who can appreciate my geeky side and isn't afraid to challenge me to a board game showdown."
    ]

    # Combine inputs into a formatted prompt
    user_input = (
        f"Create a personalized bio for someone who is a {', '.join(career)}, "
        f"with personality traits like {', '.join(personality)}, "
        f"interests in {', '.join(interests)}, and goals like {', '.join(relationship_goals)}."
    )

    # Generate the prompt with N-shot examples and the word limit instruction
    prompt = (
        "\n".join(bio_samples) + "\n" +
        "User's input: " + user_input + "\n" +
        "Please generate a bio no longer than 50 words."
    )

    # Generate bio using LLM
    try:
        response = llm.invoke([{
            "role": "system",
            "content": "You are a helpful assistant that creates engaging bios based on user input, using the following examples for reference."
        }, {
            "role": "user",
            "content": prompt
        }])
        bio = response.content.strip()
    except Exception as e:
        bio = f"Error generating bio: {str(e)}"

    return jsonify({"bio": bio})


if __name__ == "__main__":
    app.run(debug=True)
