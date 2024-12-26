# Flask App Secret Key
FLASH_APP_SECRET_KEY = "a7f6e9d4358b4f72b2c3197d4eab6e58"

# Rexera API Configuration
REXERA_BASE_URL = "https://api.rexera.com/power_automate/payoffDetails"
REXERA_API_TOKEN = "HWBRKSEGFFTJFVXMCBMD"

# VAPI API Configuration
VAPI_BASE_URL = "https://api.vapi.ai/call"
VAPI_API_TOKEN = "8654368c-6482-4610-97a5-4cf17e2b5f21"
VAPI_ASSISTANT_ID = "e51b9070-1114-4c6a-8dd0-340f3d223058"
VAPI_PHONE_NUMBER_ID = "28f52250-bce6-4f3a-b53b-ea7d5a4407e2"

# VAPI LLM Configuration
VAPI_MAIN_LLM_PROVIDER = "openai"
VAPI_MAIN_LLM_MODEL = "gpt-4o"
VAPI_MAIN_LLM_FALLBACK_MODELS = ["gpt-4-turbo"]

# VAPI Voice Configuration
VAPI_VOICE_PROVIDER = "11labs"
VAPI_VOICE_VOICE_ID = "RNnkVeW25AwKYxZgnHBH"
VAPI_VOICE_ENABLED_SSML_PARSING = True

# VAPI Voicemail Detection Configuration
VAPI_VOICEMAIL_DETECTION_PROVIDER = "twilio"
VAPI_VOICEMAIL_DETECTION_ENABLED = False

# VAPI Miscellaneous Configuration
VAPI_SEMANTIC_CACHING_ENABLED = False
VAPI_FIRST_MESSAGE_MODE = "assistant-waits-for-user"
VAPI_SUCCESS_EVALUATION_PLAN_ENABLED = False
VAPI_NUMBER_E164_CHECK_ENABLED = True

# Agent and Company Information
AGENT_NAME = "Max Sterling"
YOUR_COMPANY_NAME = "Rexera"
REXERA_PHONE_NUMBER = "plus one.. four one five.. two three six.. two five seven seven"
REXERA_CONTACT_EMAIL = "contact us at rexera dot com"
REXERA_FAX_NUMBER = "plus one.. seven six five.. three seven four.. zero seven nine five"

# Digit to Word Mapping
DIGIT_TO_WORD = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine'
    }