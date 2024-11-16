from flask import Flask, render_template, request, jsonify
from langchain_ollama import ChatOllama

app = Flask(__name__)

# Initialize Ollama LLM
llm = ChatOllama(
    model="llama3.2",  
    temperature=0.7,
)

@app.route('/')
def home():
    """
    Renders the home page.
    This route serves the main webpage where users can input data for bio generation.
    """
    return render_template('index.html')

@app.route('/generate_bio', methods=['POST'])
def generate_bio():
    """
    Generates a personalized bio based on the input data from the user.
    
    Steps:
    1. Receives JSON input from the user.
    2. Validates the input to ensure all required fields are provided and non-empty.
    3. Prepares a structured prompt using predefined bio samples and the user's input.
    4. Passes the prompt to the Ollama LLM to generate a personalized bio.
    5. Returns the generated bio as a JSON response.
    """
    # Capture incoming JSON data
    data = request.json
    
    # Check if the necessary fields are present in the input
    required_fields = ['career', 'personality', 'interests', 'relationship_goals']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields in the input data"}), 400
    
    # Extract values from the incoming data
    career = data.get('career', [])
    personality = data.get('personality', [])
    interests = data.get('interests', [])
    relationship_goals = data.get('relationship_goals', [])
    
    # Validate if the input lists are non-empty
    if not any([career, personality, interests, relationship_goals]):
        return jsonify({"error": "At least one of the input fields is empty"}), 400

    # Bio Samples for N-shot prompting
    bio_samples = [
        "The Adventurous Foodie: Globe-trotting architect with a passion for spicy food and sustainable design. Seeking a fellow adventurer who can appreciate a good biryani and a thought-provoking conversation.",
        "The Creative Bookworm: Introverted writer with a love for classic literature and indie coffee shops. Looking for someone who can match my wit and charm over a cup of chai and a deep discussion about our favorite novels.",
        "The Sporty Entrepreneur: Energetic entrepreneur with a passion for fitness and outdoor adventures. Seeking a partner who can keep up with my active lifestyle and shares my love for hiking, biking, and trying new things.",
        "The Compassionate Musician: Soulful musician with a heart for social justice and a love for live music. Looking for a kind and compassionate partner who enjoys jamming out at concerts and making a difference in the world.",
        "The Tech-Savvy Gamer: Software engineer by day, gamer by night. I'm equally comfortable debugging code and exploring virtual worlds. Seeking a partner who can appreciate my geeky side and isn't afraid to challenge me to a board game showdown."
    ]
    
    # Combine inputs into a well-structured prompt
    user_input = (
        f"Create a personalized bio for a person who is a {', '.join(career)}, "
        f"with the following personality traits: {', '.join(personality)}, "
        f"interests in {', '.join(interests)}, and relationship goals of {', '.join(relationship_goals)}."
    )
    
    # Format the final prompt with N-shot examples and the user's input
    prompt = (
        "\n".join(bio_samples) + "\n\n" +  # Ensure there's a newline for clarity
        f"User's input: {user_input}\n" + 
        "Please generate a bio no longer than 50 words."
    )
    
    # Generate the bio using Ollama
    try:
        response = llm.invoke([ 
            ("system", "You are a helpful assistant that creates engaging bios based on user input, using the following examples for reference."),
            ("human", prompt)
        ])
        
        # Check if the response content is valid
        if not response.content.strip():
            raise ValueError("Generated bio is empty.")
        
        bio = response.content.strip()
        
        # Return the generated bio as a JSON response
        return jsonify({"bio": bio})
    
    except Exception as e:
        # Log error message for debugging purposes
        print(f"Error generating bio: {str(e)}")
        
        # Return a user-friendly error message
        return jsonify({"error": f"Error generating bio: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
