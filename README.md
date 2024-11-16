# BioGenerator

This is a simple Flask web application that allows users to generate personalized bios based on their inputs, such as career, personality traits, interests, and relationship goals. The app uses Ollama's LLM to generate the bio based on the user-provided information.

## Features
- **User-friendly interface**: The app provides an interactive front-end with options for users to select their career, personality traits, interests, and relationship goals.
- **Bio generation**: After selecting options, the user can generate a personalized bio that reflects their chosen attributes.
- **Ollama LLM integration**: The backend uses the Ollama LLM model to generate the bio based on predefined bio samples and user input.

## Requirements
- Python 3.x
- Flask
- `langchain_ollama` Python package

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sujal-maheshwari2004/BioGenerator.git
    cd BioGenerator
    ```

2. Install the necessary Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    **Note:** Make sure to install the `langchain_ollama` package for Ollama LLM integration.

3. Start the Flask app:

    ```bash
    python app.py
    ```

4. Open your browser and go to `http://127.0.0.1:5000` to access the application.

## How It Works

1. **Frontend (index.html)**: 
   - The user selects their career, personality traits, interests, and relationship goals using clickable options.
   - After making the selections, the user clicks the "Generate Bio" button to trigger the bio generation process.

2. **Backend (app.py)**:
   - The Flask app receives the user's selections as a POST request on the `/generate_bio` route.
   - The server then creates a structured prompt combining the user's selections with predefined bio samples.
   - The prompt is passed to Ollama LLM, which generates a personalized bio based on the input.
   - The generated bio is returned to the frontend and displayed to the user.

3. **Bio Generation**:
   - The generated bio is returned in a JSON response and displayed on the webpage. If there is any error in bio generation, a user-friendly error message is shown instead.

## Example Usage

1. Open the app in your browser.
2. Select a career, personality traits, interests, and relationship goals from the provided options.
3. Click the "Generate Bio" button to see the generated bio.

### Sample Bio

- **Career**: Engineer
- **Personality Traits**: Creative, Ambitious
- **Interests**: Traveling, Cooking
- **Relationship Goals**: Long-term Commitment

The app might generate something like:

> "Creative engineer with a passion for exploring new destinations and cooking delicious meals. Ambitious, seeking a long-term partner who shares my zest for life and adventure."

## Error Handling

- If the user misses any required fields (career, personality, interests, relationship goals), the app will return an error message prompting them to provide all necessary data.
- If there is an issue with generating the bio, a generic error message will be returned.

## Technologies Used
- **Flask**: Web framework for building the backend.
- **Ollama LLM**: Used to generate the personalized bios.
- **HTML/CSS**: Frontend design and user interface.
