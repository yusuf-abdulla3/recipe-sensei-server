import os
from django.http import JsonResponse

def get_unsplash_image(query):
    api_key= os.environ.get("UNSPLASH_ACCESS_KEY")
    if not query:
      return JsonResponse({'error': 'Missing search query parameter'}, status=400)
    url = f'https://api.unsplash.com/search/photos?query={query}&client_id=YOUR_ACCESS_KEY'
    
    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()
      # Access the image URL from the first result (adjust based on your needs)
      image_url = data['results'][0]['urls']['regular']
      return {'image_url': image_url}
    else:
      return JsonResponse({'error': 'Unsplash API request failed'}, status=response.status_code)