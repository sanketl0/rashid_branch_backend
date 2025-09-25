import base64
import requests
from django.core.cache import cache
def image_url_to_base64(url):
    # Fetch the image from the remote URL
    result = cache.get(url)
    if not result:
        response = requests.get(url)
        # Ensure the request was successful
        if response.status_code == 200:
            # Encode the image content to Base64
            encoded_image = base64.b64encode(response.content).decode('utf-8')
            # Extract the image file type from the URL
            file_type = url.split('.')[-1]
            # Return the image as a Base64-encoded string with the appropriate prefix
            result = f"data:image/{file_type};base64,{encoded_image}"
            cache.set(url,result,60*60*24)
            return result
        else:
            return url
            raise Exception(f"Failed to fetch image from URL: {url}")
    else:
        print("from cache")
        return  result