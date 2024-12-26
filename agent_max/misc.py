import phonenumbers
import requests
import json
from .constants import REXERA_BASE_URL, REXERA_API_TOKEN, DIGIT_TO_WORD

# Function to format a phone number to US E.164 format
def format_to_us_phone_number(phone_number: str) -> str:
    try:
        # Parse the phone number with US as the default region
        parsed_number = phonenumbers.parse(phone_number, "US")
        # Format the parsed number to E.164 format
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        # Return None if the phone number cannot be parsed
        return None 

# Function to fetch loan details using a loan number
def fetch_loan_details(loan_number: str):
    # Construct the URL with the loan number
    url = f"{REXERA_BASE_URL}?loan_number={loan_number}"
    try:
        # Set up the headers with the API token for authorization
        REXERA_HEADERS = {
            "Authorization": f"Bearer {REXERA_API_TOKEN}"
        }
        # Make a GET request to the URL
        response = requests.get(url, headers=REXERA_HEADERS)
        # Raise an error if the request was unsuccessful
        response.raise_for_status()
        # Parse the response JSON
        data = response.json()
        # Return the data 
        return data
    except requests.exceptions.RequestException as e:
        # Print an error message if a request exception occurs
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError:
        # Print an error message if JSON decoding fails
        print("Failed to decode JSON response.")
        return None
    
def number_to_words_with_custom_dots(number):
    # Return empty string if number is None
    if not number:
        return ""
        
    # Define a mapping from digits to their word equivalents
    digit_to_word = DIGIT_TO_WORD

    # Remove any non-digit characters (like hyphens or spaces)
    cleaned_number = ''.join(filter(str.isdigit, str(number)))
    
    # Convert the cleaned number to a string and map each digit to its word equivalent
    words = [digit_to_word[digit] for digit in cleaned_number]
    length = len(words)

    # Handle cases based on the number length
    if length <= 3:
        # No dots, just convert to words
        return " ".join(words)
    elif length == 4:
        # Dots after every two words
        result = []
        for i in range(0, len(words), 2):
            chunk = words[i:i+2]
            result.append(" ".join(chunk))
        return ".. ".join(result)
    else:
        # Dots after every three words
        result = []
        for i in range(0, len(words), 3):
            chunk = words[i:i+3]
            result.append(" ".join(chunk))
        return ".. ".join(result)