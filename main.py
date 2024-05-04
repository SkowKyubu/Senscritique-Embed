# Importing necessary libraries
import requests  # For making HTTP requests
import re  # For regular expressions
from bs4 import BeautifulSoup  # For parsing HTML
from jinja2 import Template

# URL of the webpage to scrape
url = 'https://www.senscritique.com/skow'


# Function to scrape data from the webpage
def scrapping(url):
    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the HTML content of the webpage using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize an empty dictionary to store extracted data
    data = {}

    # Find all <div> elements with a specific class
    elements = soup.find_all('div', class_='sc-b088f2d1-2 fNczqX')

    # Store the translation of the French title in a dictionary
    translation = {'Total': 'Total',
                   'Films': 'Movies',
                   'Albums': 'Albums',
                   'BD': 'Comics',
                   'Séries': 'Dramas',
                   'Livres': 'Books',
                   'Morceaux': 'Songs',
                   'Jeux vidéo': 'Video Games'}

    # Iterate through each found <div> element
    for tag in elements:
        # Extract the text content of the current <div> element
        extracted_text = tag.text

        # Use regular expression to match numeric and alphabetical parts in the text content
        matches = re.match(r'(\d+)([A-Za-zÀ-ÖØ-öø-ÿ\s]+)', extracted_text)

        # If a match is found
        if matches:
            # Store the numeric part as the key and the alphabetical part as the value in the data dictionary
            data[matches.group(2)] = matches.group(1)

    # Apply the translation
    translated_dict = {translation[key]: value for key, value in data.items()}

    # Return the extracted data dictionary
    return translated_dict


# Call the function to scrape the data
data = scrapping(url)

# Load the HTML template
with open('template.html') as file:
    template = Template(file.read())

# Render the template with the extracted data
rendered_html = template.render(total_count=data['Total'],
                                movies_count=data['Movies'],
                                albums_count=data['Albums'],
                                comics_count=data['Comics'],
                                dramas_count=data['Dramas'],
                                books_count=data['Books'],
                                videogames_count=data['Video Games'],
                                url=url,
                                url_total=url + '/collection',
                                url_movies=url + '/collection?universe=1',
                                url_albums=url + '/collection?universe=7',
                                url_comics=url + '/collection?universe=6',
                                url_dramas=url + '/collection?universe=4',
                                url_books=url + '/collection?universe=2',
                                url_games=url + '/collection?universe=3')

# Save the rendered HTML to a file
with open('scraped_data.html', 'w') as file:
    file.write(rendered_html)

# Print message indicating successful completion
print("Data scraped and saved to scraped_data.html")
