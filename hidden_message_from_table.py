import requests
from bs4 import BeautifulSoup

def print_grid(url):
    # Fetch the Google Doc content
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the document using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table in the document
    table = soup.find('table')
    rows = table.find_all('tr')

    # Initialize a dictionary to store the characters and their positions
    char_map = {}
    
    # Skip the header row (first row)
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) == 3:
            try:
                x = int(cells[0].get_text(strip=True))
                char = cells[1].get_text(strip=True)
                y = int(cells[2].get_text(strip=True))
                char_map[(x, y)] = char
            except ValueError as e:
                print(f"Skipping row due to error: {e}")

    # Determine the dimensions of the grid
    if char_map:
        max_x = max(x for x, y in char_map.keys()) + 1
        max_y = max(y for x, y in char_map.keys()) + 1
    else:
        max_x = 0
        max_y = 0

    # Create the grid with spaces as default
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

    # Place characters in their respective positions
    for (x, y), char in char_map.items():
        grid[y][x] = char

    # Print the grid, reversing the row order to correct upside-down display
    for row in reversed(grid):
        print(''.join(row))

# Example usage
url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
print_grid(url)
