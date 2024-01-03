from flask import Flask, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def download_images(url):
    try:
        img_name = url.split('/')[-1]
        img_bytes = requests.get(url).content
        with open(img_name, 'wb') as img_file:
            img_file.write(img_bytes)
            print(f"{img_name} was downloaded")
        return {'status': 'success', 'message': f"{img_name} was downloaded"}
    except requests.exceptions.MissingSchema as e:
        error_message = f"Invalid URL: {url}. Error: {e}"
        print(error_message)
        return {'status': 'error', 'message': error_message}

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    img_urls = data.get('urls', [])
    if not img_urls:
        return jsonify({'message': 'No URLs provided'}), 400

    # multi
    responses = []
    
    max_threads = 5
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        download_tasks = {executor.submit(download_images, url): url for url in img_urls}
        for task in download_tasks:
            response = task.result()
            responses.append(response)
        
    # Single 
    # responses = []
    # for url in img_urls:
    #     response = download_images(url)
    #     responses.append(response)
    return jsonify({'responses': responses})

if __name__ == '__main__':
    app.run(debug=True)
