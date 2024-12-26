import requests
import json
from flask import flash, redirect, url_for
from .constants import (
    VAPI_API_TOKEN, VAPI_BASE_URL, VAPI_ASSISTANT_ID, VAPI_PHONE_NUMBER_ID,
    VAPI_MAIN_LLM_PROVIDER, VAPI_MAIN_LLM_MODEL, VAPI_MAIN_LLM_FALLBACK_MODELS,
    VAPI_VOICE_PROVIDER, VAPI_VOICE_VOICE_ID, VAPI_VOICE_ENABLED_SSML_PARSING,
    VAPI_SEMANTIC_CACHING_ENABLED, VAPI_FIRST_MESSAGE_MODE,
    VAPI_VOICEMAIL_DETECTION_PROVIDER, VAPI_VOICEMAIL_DETECTION_ENABLED,
    VAPI_SUCCESS_EVALUATION_PLAN_ENABLED, VAPI_NUMBER_E164_CHECK_ENABLED,
    YOUR_COMPANY_NAME, REXERA_PHONE_NUMBER, REXERA_CONTACT_EMAIL, REXERA_FAX_NUMBER,
    AGENT_NAME
)
from .misc import format_to_us_phone_number, fetch_loan_details, number_to_words_with_custom_dots
from .prompts import SYSTEM_PROMPT_MESSAGE, VOICEMAIL_MESSAGE, INTRODUCTORY_MESSAGE

def make_api_call(loan_number, to_number, good_through_date, ssn_full, borrower_name):
    # Fetch loan details using the provided loan number
    loan_details = fetch_loan_details(loan_number)

    # If ssn_full is provided, add it to the system prompt
    if ssn_full:
        # Convert the ssn_full to words with dots
        ssn_full = number_to_words_with_custom_dots(ssn_full)
        ssn_full = f"9. Full SSN Number: {ssn_full}"
    else:
        ssn_full = ""
        
    # If loan details are found, extract relevant information
    if loan_details:
        order_id = loan_details[0].get("order_id")
        property_address = loan_details[0].get("address_full")
        loan_number = loan_details[0].get("loan_number")
        ssn = loan_details[0].get("ssn")
        lender_name = loan_details[0].get("lender_name")
        client_name = loan_details[0].get("client_name")
        address_zipcode = loan_details[0].get("address_zipcode")
    else:
        flash('Loan details could not be retrieved!', 'error')
        return redirect(url_for('index'))

    if not ssn:
        flash('SSN is missing!', 'error')
        return redirect(url_for('index'))
    if not address_zipcode:
        flash('Zipcode is missing!', 'error')
        return redirect(url_for('index'))
        
    # Format the phone number to US standard
    to_number = format_to_us_phone_number(to_number)
    if not to_number:
            flash('Phone number is not formatted properly!', 'error')
            return redirect(url_for('index'))
    
    #Convert the loan details to words with dots
    loan_number = number_to_words_with_custom_dots(loan_number)
    ssn = number_to_words_with_custom_dots(ssn)
    address_zipcode = number_to_words_with_custom_dots(address_zipcode)
    
    # Format the system prompt with the loan details
    system_prompt = SYSTEM_PROMPT_MESSAGE.format(
                        property_address=property_address,
                        loan_number=loan_number,
                        ssn=ssn,
                        good_through_date=good_through_date,
                        borrower_name=borrower_name,
                        lender_name=lender_name,
                        address_zipcode=address_zipcode,
                        ssn_full=ssn_full,
                        your_company_name=YOUR_COMPANY_NAME,
                        rexera_phone_number=REXERA_PHONE_NUMBER,
                        rexera_contact_email=REXERA_CONTACT_EMAIL,
                        rexera_fax_number=REXERA_FAX_NUMBER,
                        agent_name=AGENT_NAME,
                        client_name=client_name,
                        introductory_message=INTRODUCTORY_MESSAGE
                    )
    
    # Format the voicemail message with the loan details
    selected_voicemail = VOICEMAIL_MESSAGE.format(
                            loan_number=loan_number,
                            your_company_name=YOUR_COMPANY_NAME,
                            rexera_phone_number=REXERA_PHONE_NUMBER,
                            agent_name=AGENT_NAME,
                            client_name=client_name,
                        )

    # Construct the payload for the API call
    payload = {
        "assistantOverrides": {
            "model": {
                "messages": [
                    {
                        "role": "system",
                        "content": f"{system_prompt}"
                    },
                ],
                "provider": VAPI_MAIN_LLM_PROVIDER,
                "model": VAPI_MAIN_LLM_MODEL,
                "fallbackModels": VAPI_MAIN_LLM_FALLBACK_MODELS,
                "semanticCachingEnabled": VAPI_SEMANTIC_CACHING_ENABLED
            },
            "voice": {
                "provider": VAPI_VOICE_PROVIDER,
                "voiceId": VAPI_VOICE_VOICE_ID,
                "enableSsmlParsing": VAPI_VOICE_ENABLED_SSML_PARSING,
                "fallbackPlan": {
                    "voices": []
                }
            },
            "voicemailDetection": {
                "provider": VAPI_VOICEMAIL_DETECTION_PROVIDER,
                "enabled": VAPI_VOICEMAIL_DETECTION_ENABLED
            },
            "voicemailMessage": f"{selected_voicemail}",
            "firstMessageMode": VAPI_FIRST_MESSAGE_MODE,
            "analysisPlan": {
                "successEvaluationPlan": {
                    "enabled": VAPI_SUCCESS_EVALUATION_PLAN_ENABLED
                }
            }
        },
        "name": f"{order_id}",
        "assistantId": VAPI_ASSISTANT_ID,
        "phoneNumberId": VAPI_PHONE_NUMBER_ID,
        "customer": {
            "numberE164CheckEnabled": VAPI_NUMBER_E164_CHECK_ENABLED,
            "number": f"{to_number}"
        }
    }

    # Set headers for the API request
    headers = {
        "Authorization": f"Bearer {VAPI_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Make the API request
    vapi_api_response = requests.request("POST", VAPI_BASE_URL, json=payload, headers=headers)
    print(vapi_api_response.json())

    # Attempt to extract and print the call ID from the response
    if vapi_api_response.status_code == 201:
        try:
            vapi_call_id = vapi_api_response.json().get("id")
            flash(f'Call Initiated! Max is ordering the payoff for Loan number: {loan_number} with Order ID: {order_id}. Call ID: {vapi_call_id}', 'success')
            return redirect(url_for('index'))
        except json.JSONDecodeError:
            flash('Failed to decode API response.', 'error')
            return redirect(url_for('index'))
    else:
        flash(f"API call failed with status code {vapi_api_response.status_code}.", 'error')
        return redirect(url_for('index'))
