import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Prompt the user to input the image's file path
local_file_path = input("Please enter the path to the image file: ")

# Check if the file exists
if not os.path.isfile(local_file_path):
    print("The file does not exist. Please check the path and try again.")
else:
    # Remove background endpoint
    url = "https://engine.prod.bria-api.com/v1/background/remove"
    headers = {'api_token': '6a2b856855c14af2ac17366b7062a869'}

    # Open the file
    files = [
        ('file', (os.path.basename(local_file_path), open(local_file_path, 'rb'), 'image/jpeg'))
    ]

    # Make the API call
    response = requests.post(url, headers=headers, files=files)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        print("Response JSON:", data)  # Debug statement to print the entire response

        if "result_url" in data:
            image_url = data["result_url"]

            # Download the image
            image_response = requests.get(image_url)

            # Check if the image response is successful
            if image_response.status_code == 200:
                # Create images directory if it doesn't exist
                if not os.path.exists('images'):
                    os.makedirs('images')

                # Construct the new filename
                original_filename = os.path.basename(local_file_path)
                new_filename = f"{os.path.splitext(original_filename)[0]}_bg_removed.png"
                image_path = os.path.join('images', new_filename)

                # Save the image to the images directory
                with open(image_path, 'wb') as file:
                    file.write(image_response.content)
                
                print(f"Image saved to {image_path}")
            else:
                print(f"Failed to download image: {image_response.status_code}")
        else:
            print("No image results found in the response")
    else:
        print(f"Failed to get response: {response.status_code}")
        print("Response content:", response.content)  # Debug statement to print the response content if status code is not 200

# For demonstration, download the image from the previous response
previous_image_url = 'https://d1uzvjowrxhw13.cloudfront.net/api/res/b1b9e90d-b764-406d-9479-cde35b7bbf83.PNG?AWSAccessKeyId=ASIAUL5JH7ABDZVEK6LH&Signature=k65gW%2B%2BRbbYOaFgjWE5T8K1e81c%3D&x-amz-security-token=FwoGZXIvYXdzEK7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGnZlETbnLpTh2AtwCKXBIG6cUi%2Bxzfd4GuQxUm3caMz9WQ%2FylXclbe5HD1G3CzdjeQSyLl5QLn4CLUB05KmvvU34rqRqzpKO0A7G3YI%2FQqxRlp9M98K5%2FW1lbZ46T94WCd8vUxNJCTNG3ruRJVtOwBE5lVl1kXnfEOdQA23q18f4VFCIdQTKMYSPKpOvoXQSs8ddi56YMM1ldMIV1h4b3JJQl0Qa9bHdr4d8H3AXkJe7GjU2DFaGd4%2F88x17SkWHxm5%2BldY1zeQH0nJSnJTVlwhizLIytd2vsBgNAAtMYqVzb8sZbKP0wE8eoN7bBCr5XmHWnnmSPAQ4aaylO6DoRmzZTxNP9zL0hOjZbzr9xJxfRPu66E%2B5d38vJY8GfnOc%2FofupOpg10tyB5EyIZVxPNQAVHwagl79A2ugYEYyagx1G6pH9Ex4nnU2Fh5VQreAdKmfs5CsIxTK3soHz50QIMBvRdQAGG90Kftqoy74aU6bAGVlQTffnwh0uZURtcjzQRbjQgm0hx0OJ5YULbKlcR%2BfCRN6PCJXGfVaMq8gAEP7BdAust2J7zZ%2BUB5cd1Udn2GbCg1m2pUxvPzH2X%2F7mKQ7bko2qa6UhwlEw2k5m2elmC%2FlznurnWoOBA3eBarKV2PpPio6tFJ9Cv2RYTzIxB%2FyBHHBGZ6N0O02CwGG1TFwDjh3cfP36v46hAgXJT3UjvFAnq8ITCRon8f%2BP0FugpWKUNf9CMo8a2YswYyKpJmyngDO2XwUMl4UTv%2Brz9M3VdBVAeVGa9makPqAsRXsvIM28dfuLodDw%3D%3D'

# Download the previous image
previous_image_response = requests.get(previous_image_url)

if previous_image_response.status_code == 200:
    # Save the image to the images directory
    previous_image_path = os.path.join('images', 'previous_image_bg_removed.png')
    with open(previous_image_path, 'wb') as file:
        file.write(previous_image_response.content)
    
    print(f"Previous image saved to {previous_image_path}")
else:
    print(f"Failed to download previous image: {previous_image_response.status_code}")
