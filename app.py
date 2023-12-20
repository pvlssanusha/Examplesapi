from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# Initialize the Cohere Client with an API Key
api = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['POST'])
def get_response():
    try:
        course = request.get_json().get('course')
        submodule=request.get_json().get('submodule')
        target = request.get_json().get('target')
        # module = request.get_json().get('module')
        # submodules = request.get_json().get('submodules')
        
        # submodules = " , ".join(submodules)
            # Define the request payload
        print("started")
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": 
                            f'''
            I want to create  3 examples  for submodule {submodule}  for target audience{target}
            Create only descriptive examples.
            Give the output in json format as code block.Strictly in json format only:
            {{
                    "examplelist":   [
                                        "Example 1: Description of the first example for {submodule}.",
                                        "Example 2: Description of the second example for {submodule}.",
                                        "Example 3: Description of the third example for {submodule}."
                    ]  
            }}
        '''
                        }
                    ]
                }
            ]
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)
        print(response)
        if response.status_code == 200:
            # Parse and print the response JSON
            response_json = response.json()
            print(response_json)
            if (response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="{"):
            #print(response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
                return (response_json["candidates"][0]["content"]["parts"][0]["text"])
            elif response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="J" or response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="j":
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][0][7:-3])
            # elif response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="\"":
                
            else:
                return (response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3])

            # print(json.dumps(response_json, indent=2))
            # print(response_json)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return json.dump(
            {
                "msg":"Error Assessing AI"
            }
            ) 

    except Exception as e:
        return jsonify({'error': str(e)})


# ... (your existing code)
if __name__ == '__main__':
    app.run(debug=True)
