import requests
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_user_input():
    prompt = input("Please enter the prompt for image generation: ")
    num_results = input("How many images would you like to generate? (1-4, default is 4): ")
    num_results = int(num_results) if num_results else 4
    
    print("Select the aspect ratio (default is '1:1'):")
    print("1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9")
    aspect_ratio = input("Enter the aspect ratio: ")
    aspect_ratio = aspect_ratio if aspect_ratio else "1:1"
    
    sync = input("Would you like the response to be synchronous? (y/n, default is 'n'): ")
    sync = sync.lower() == 'y'
    
    seed = input("Enter a seed value (optional): ")
    negative_prompt = input("Enter a negative prompt (optional): ")
    
    steps_num = input("Enter the number of iterations (20-50, default is 30): ")
    steps_num = int(steps_num) if steps_num else 30
    
    text_guidance_scale = input("Enter the text guidance scale (1-10, default is 5): ")
    text_guidance_scale = float(text_guidance_scale) if text_guidance_scale else 5.0
    
    medium = input("Select the medium (photography/art, optional): ")
    medium = medium if medium else None
    
    prompt_enhancement = input("Would you like to enable prompt enhancement? (y/n, default is 'n'): ")
    prompt_enhancement = prompt_enhancement.lower() == 'y'
    
    print("Select the model type:")
    print("1. Base model")
    print("2. Fast model")
    print("3. HD model")
    model_type = int(input("Enter the number corresponding to the model type (1/2/3): "))
    
    return {
        "prompt": prompt,
        "num_results": num_results,
        "aspect_ratio": aspect_ratio,
        "sync": sync,
        "seed": seed,
        "negative_prompt": negative_prompt,
        "steps_num": steps_num,
        "text_guidance_scale": text_guidance_scale,
        "medium": medium,
        "prompt_enhancement": prompt_enhancement,
        "model_type": model_type
    }

def get_model_endpoint(model_type):
    base_url = "https://engine.prod.bria-api.com/v1/text-to-image/"
    model_version = "2.3"  # Assuming model version 2.3 for all models
    if model_type == 1:
        return f"{base_url}base/{model_version}"
    elif model_type == 2:
        return f"{base_url}fast/{model_version}"
    elif model_type == 3:
        return f"{base_url}hd/{model_version}"
    else:
        raise ValueError("Invalid model type")

def save_image_from_url(url, image_path):
    image_response = requests.get(url)
    if image_response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(image_response.content)
        print(f"Image saved to {image_path}")
    else:
        print(f"Failed to download image: {image_response.status_code}")

def extract_image_urls(response_json):
    urls = []
    if 'result' in response_json:
        for result in response_json['result']:
            if 'urls' in result:
                urls.extend(result['urls'])
    return urls

def main():
    user_input = get_user_input()
    
    url = get_model_endpoint(user_input["model_type"])
    api_token = os.getenv('BRIA_API_KEY')
    if not api_token:
        print("Error: BRIA_API_KEY is not set in environment variables.")
        return
    
    headers = {'api_token': api_token}
    payload = {
        "prompt": user_input["prompt"],
        "num_results": user_input["num_results"],
        "aspect_ratio": user_input["aspect_ratio"],
        "sync": user_input["sync"],
        "steps_num": user_input["steps_num"],
        "text_guidance_scale": user_input["text_guidance_scale"],
        "medium": user_input["medium"],
        "prompt_enhancement": user_input["prompt_enhancement"]
    }
    if user_input["seed"]:
        payload["seed"] = user_input["seed"]
    if user_input["negative_prompt"]:
        payload["negative_prompt"] = user_input["negative_prompt"]

    print(f"Making request to URL: {url}")
    print(f"With headers: {headers}")
    print(f"And payload: {payload}")
    
    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    print("Response JSON:", response_json)
    
    if response.status_code == 200:
        image_urls = extract_image_urls(response_json)
        if image_urls:
            for i, image_url in enumerate(image_urls):
                image_path = os.path.join("images", f"generated_image_{i+1}.png")
                save_image_from_url(image_url, image_path)
        else:
            print("No image URLs found in the response.")
    else:
        print(f"Failed to get response: {response.status_code}")

if __name__ == "__main__":
    main()
