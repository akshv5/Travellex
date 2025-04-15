from flask import Flask, send_from_directory, send_file, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'development-key-change-in-production')

# Serve static files from the 'static' directory
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for the register page
@app.route('/register')
def register():
    return render_template('register.html')

# Route for the plan trip page
@app.route('/plan-trip', methods=['GET', 'POST'])
def plan_trip():
    if request.method == 'POST':
        # Get form data
        destination = request.form.get('destination')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        travelers = request.form.get('travelers')
        budget = request.form.get('budget')
        
        # Get preferences (these will be lists if multiple options are selected)
        accommodation = request.form.getlist('accommodation[]')
        activities = request.form.getlist('activities[]')
        transportation = request.form.getlist('transportation[]')
        
        # Validate input
        if not destination or not start_date or not end_date:
            flash('Please fill in all required fields.', 'error')
            return render_template('plan-trip.html')
        
        # In a real application, you would use this data to generate a trip plan
        # For demo purposes, just create a simple summary
        preferences = []
        if accommodation:
            preferences.append(f"Accommodation: {', '.join(accommodation)}")
        if activities:
            preferences.append(f"Activities: {', '.join(activities)}")
        if transportation:
            preferences.append(f"Transportation: {', '.join(transportation)}")
            
        preferences_summary = " | ".join(preferences) if preferences else "No specific preferences"
        
        # Process the trip planning (in a real app, this would involve more complex logic)
        flash(f'Your trip to {destination} from {start_date} to {end_date} with a budget of ${budget} has been planned successfully!', 'success')
        flash(f'Preferences: {preferences_summary}', 'info')
        
        # For now, just redirect back to the form with a success message
        return redirect(url_for('plan_trip'))
    
    # If it's a GET request, just show the form
    return render_template('plan-trip.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 