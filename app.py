import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

# Configure Flask to use 'views' for templates and static assets
# static_url_path='' maps static files to the root URL so 'img/logo.png' works
app = Flask(__name__, template_folder='views', static_folder='views', static_url_path='')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.php')
def index_php():
    return redirect(url_for('index'))

@app.route('/allocation.php')
def allocation():
    return render_template('allocation.html')

@app.route('/get_hostel.php', methods=['POST'])
def get_hostel():
    reg_no = request.form.get('reg_no', '').strip()
    
    # Check if current date is before August 3, 2026
    allocation_start_date = datetime.date(2026, 8, 3)
    current_date = datetime.date.today()
    
    if current_date < allocation_start_date:
        message = "Please wait till room allocation starts on 3rd August 2026."
        return render_response(message)
    
    if not reg_no:
        error_msg = '''<b>Warning</b>:  Undefined array key "reg_no" in <b>/var/www/html/hostels/get_hostel.php</b> on line <b>31</b><br />
There is no room allocation corresponding to the Admission Number entered. For any further clarification, please contact <a href= 'http://accommodation.ku.ac.ke/' target='_blank'>Accommodation Services Directorate </a>'''
        return render_response(error_msg)
        
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM students WHERE student_id = ?', (reg_no,)).fetchone()
    conn.close()
    
    if not row or row['application_status'] != 'Allocated' or not row['allocated_hostel']:
        error_msg = '''There is no room allocation corresponding to the Admission Number entered. For any further clarification, please contact <a href= 'http://accommodation.ku.ac.ke/' target='_blank'>Accommodation Services Directorate </a>'''
        return render_response(error_msg)
        
    success_msg = f"Congratulations <b>{row['full_name']}</b>, You have been allocated a room at <b>{row['allocated_hostel']}</b>"
    return render_response(success_msg)

def render_response(message):
    html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
  	<title>Kenyatta University Hostel Allocations</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
 	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="js/formapp.js"></script>
    <meta charset="utf-8">
		<link href='https://fonts.googleapis.com/css?family=Quicksand' rel='stylesheet'>
<style>
body {{
    font-family: 'Quicksand';font-size: 22px;
}}
</style>
	
  </head>
  <body>
  <div class="container" style="display:block;overflow:auto;">
	
	<div class="container-fluid" style="background-color:#003366; border-radius: 5px;">
	<img class="img-responsive" src="img/logo.png" width="550px" alt="KU logo">
	</div> 
    <div class="container-fluid" style="background-color:#eeeeee; border-radius: 5px; min-height:400px;">
  	
	   <div class="row" style= "margin-top:30px;margin-bottom:20px;"><div class="col-xs-12 text-center"><h1>2026/2027 ROOM ALLOCATION</h1></div></div>
	  
<br />
{message}
<div class="row text-center" style= "margin-top:30px;margin-bottom:20px;">
<a href="index.php"><button type="button" class="btn btn-primary btn-lg"><span class="glyphicon glyphicon-circle-arrow-left glyphicon-lg"></span> Go Back</button></a>
</div>
	 
	</div>
	
	<nav class="navbar navbar-inverse">
	  <div class="container-fluid">
		<div class="navbar-header">
		  <a class="navbar-brand" href="#"> &copy; 2026 Kenyatta University</a>
		</div>
	  </div>
	</nav>
	</div>
	<!--    The following is the user accessibility script  -->

<script>
(function(d){{
var s = d.createElement("script");
/* uncomment the following line to override default position*/
s.setAttribute("data-position", 2);

s.setAttribute("data-account", "peHkTc4v1K");
s.setAttribute("src", "https://cdn.userway.org/widget.js");
(d.body || d.head).appendChild(s);}})(document)
</script>

<!--  Accessibility SCRIPT ENDS      -->	
  </body>
</html>'''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
