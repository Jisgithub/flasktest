import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """
    This route handles both displaying the submission form (GET)
    and processing the submitted confession (POST).
    """
    if request.method == 'POST':
        # Get the message from the form's <textarea>
        # The name 'message' must match the name attribute in the HTML
        message = request.form.get('message')

        if message:
            data_to_insert = {"message": message}
            supabase.table('confessions').insert(data_to_insert).execute()

            # After posting, redirect the user to the page with all confessions
            # This is a standard pattern called Post/Redirect/Get (PRG)
            return redirect(url_for('show_all_confessions'))

    # If it's a GET request, just show the homepage with the form
    return render_template('index.html')


@app.route('/confessions')
def show_all_confessions():
    """
    This route fetches all confessions from the database and
    displays them on a dedicated page.
    """
    # Fetch all rows from the 'confessions' table
    # We order by 'created_at' in descending order to show newest first
    response = supabase.table('confessions').select('*').order('created_at', desc=True).execute()
    
    # The actual data is in the 'data' attribute of the response
    all_confessions = response.data
    
    # Render the confessions page, passing the list of confessions to the template
    return render_template('confessions.html', confessions=all_confessions)
