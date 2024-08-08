# app.py
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import openai 

app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes
# Set up OpenAI client
client = OpenAI(api_key='sk-abc')


def get_color_name(hex_code):
    prompt = f"Provide only the English color name for the CSS hex code {hex_code} , without any additional text.."
    try:
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,  # Limit the response to a small number of tokens
             temperature=0  # Set temperature to 0 for deterministic results
        )
        
        color_name = response.choices[0].message.content.strip().upper()
        return color_name
    except Exception as e:
        return f"Error: {str(e)}"

def get_mood(hex_code):
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (1, 3, 5))
    if (255, 0, 0) <= rgb <= (255, 127, 127):
        return "ANGER"
    elif (255, 165, 0) <= rgb <= (255, 191, 128):
        return "JOY"
    elif (255, 255, 0) <= rgb <= (255, 255, 128):
        return "ANXIETY"
    elif (0, 255, 0) <= rgb <= (128, 255, 128):
        return "DISGUST"
    elif (0, 255, 255) <= rgb <= (128, 255, 255):
        return "SHAME"
    elif (0, 0, 255) <= rgb <= (128, 128, 255):
        return "SADNESS"
    elif (128, 0, 128) <= rgb <= (191, 128, 191):
        return "FEAR"
    elif (255, 192, 203) <= rgb <= (255, 182, 193):
        return "ENVY"
    else:
        return "MISCELLANEOUS"

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    hex_code = data.get('hex_code')
    if not hex_code:
        return jsonify({'error': 'No hex code provided'}), 400
    
    color_name = get_color_name(hex_code)
    mood = get_mood(hex_code)
    response_text = f"{color_name} is associated with the mood {mood}"
    return jsonify({'response': response_text})
   

if __name__ == '__main__':
    app.run(debug=True)
    
 #return jsonify({'color_name': color_name, 'mood': mood})