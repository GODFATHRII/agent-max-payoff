import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, render_template, request, redirect, url_for, flash
from agent_max.max import make_api_call
from datetime import datetime
from agent_max.constants import FLASH_APP_SECRET_KEY

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASH_APP_SECRET_KEY
app.secret_key = FLASH_APP_SECRET_KEY  # Required for flashing messages

# Define the route for the homepage, allowing both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve form data
        loan_number = request.form.get('loan_number')
        phone_number = request.form.get('phone_number')
        good_through_date = request.form.get('good_through_date')
        borrower_name = request.form.get('borrower_name')
        ssn_full = request.form.get('ssn_full')  # Optional field

        # If all required fields are present, make an API call
        if loan_number and phone_number and good_through_date and borrower_name:
            # Convert the date to yyyy-mm-dd format
            if good_through_date:
                try:
                    date_object = datetime.strptime(good_through_date, '%m/%d/%Y')
                    good_through_date = date_object.strftime('%Y-%m-%d')
                except ValueError:
                    flash('Invalid date format. Please use MM/DD/YYYY.', 'error')
                    return redirect(url_for('index'))
            
            make_api_call(loan_number, phone_number, good_through_date, ssn_full, borrower_name)
            # Redirect to the index page after processing
            return redirect(url_for('index'))

    # Render the index.html template for GET requests or after processing POST
    return render_template('index.html')

# Run the application in debug mode
if __name__ == '__main__':
    app.run(debug=True) 