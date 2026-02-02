#!/usr/bin/env python3
"""Check book IDs in the JSON file."""
import urllib.request
import json

# Download NVI to check book IDs
url = 'https://raw.githubusercontent.com/MaatheusGois/bible/main/versions/pt-br/nvi.json'
with urllib.request.urlopen(url, timeout=30) as response:
    data = json.loads(response.read().decode('utf-8-sig'))

# List all book IDs
print("Book IDs in NVI JSON:")
for i, book in enumerate(data):
    book_id = book.get('id', 'unknown')
    book_name = book.get('name', 'unknown')
    print(f'{i+1}. ID="{book_id}" Name="{book_name}"')
