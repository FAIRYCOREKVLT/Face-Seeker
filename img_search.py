import requests, json
from datetime import datetime

def save_to_file(strings, filename):
    with open(filename, 'a') as file:
        for s in strings:
            file.write(s + '\n')

def img_search(faceimg):
        # upload img on server

        url = 'https://uguu.se/upload.php'
        print(f"\033[1mUploading\033[0m {faceimg}...")

        with open(faceimg, 'rb') as file:
            data = {'files[]': (file.name, file)}
            response = requests.post(url, files=data)

        if response.status_code == 200:
            service_data = response.json()
            image_url = service_data['files'][0]['url']
            print(service_data['files'][0]['url'])

        # search code

        if image_url is not None:
            url = "https://reverse-image-search-by-copyseeker.p.rapidapi.com/"

            querystring = {"imageUrl":image_url}

            with open("api_key.txt", "r", encoding="utf-8") as file:
                api_key = file.read()

            with open("host.txt", "r", encoding="utf-8") as file:
                host = file.read()

            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": host
            }

            response = requests.get(url, headers=headers, params=querystring)

            # show results

            if response.status_code == 200:
                data = response.json()
                with open(f"{faceimg}_dump.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                data_str = json.dumps(data, ensure_ascii=False, indent=4)
                timestamp = f"Timestamp: {str(datetime.now().replace(microsecond=0))}"
                result_header = f"Result for {faceimg}:"
                save_to_file([timestamp, result_header, data_str, "\n"], "search_log.txt")

                page_urls = [page['Url'] for page in data['Pages']]
                entities = [page['Description'] for page in data['Entities']]
                similar_urls = data['VisuallySimilar']

                print(f"\033[1mResult for\033[0m {faceimg}:")

                print("\033[1mUrls:\033[0m")
                for number, url in enumerate(page_urls, start=1):
                    print(f"\033[1m{number}.\033[0m {url}")
                    
                print("\n\033[1mEntities:\033[0m")
                for number, text in enumerate(entities, start=1):
                    print(f"\033[1m{number}.\033[0m {text}")

                print("\n\033[1mVisually similar img urls:\033[0m")
                for number, url in enumerate(similar_urls, start=1):
                    print(f"\033[1m{number}.\033[0m {url}")
                    
                print(f"\n\033[1mEnd of\033[0m {faceimg} \033[1msearch\033[0m")
                print()

            else:
                print(f"Error sending request: {response.status_code}")
        else:
            print(f"Error loading img: {response.status_code}")