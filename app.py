!apt-get update
!apt-get install mysql-server -y
!pip install flask pyngrok mysql-connector-python

!service mysql start

!sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"

!mysql -u root -proot -e "CREATE DATABASE forensic_db;"

!mysql -u root -proot -e 'USE forensic_db;'

!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE cases(case_id INT PRIMARY KEY, case_name VARCHAR(100), crime_type VARCHAR(100), status VARCHAR(50));'

!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE investigator(investigator_id INT PRIMARY KEY, name VARCHAR(100), rank_name VARCHAR(100));'

!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE evidence(evidence_id INT PRIMARY KEY, case_id INT, type VARCHAR(100), description VARCHAR(200), collected_date DATE, FOREIGN KEY(case_id) REFERENCES cases(case_id));'

!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE custody(custody_id INT PRIMARY KEY, evidence_id INT, investigator_id INT, date_received DATE, FOREIGN KEY(evidence_id) REFERENCES evidence(evidence_id), FOREIGN KEY(investigator_id) REFERENCES investigator(investigator_id));'

!mysql -u root -proot -e 'USE forensic_db; SHOW TABLES;'

!mysql -u root -proot -e "USE forensic_db; INSERT INTO cases VALUES (1,'Bank Robbery','Theft','Open'),(2,'City Murder','Homicide','Closed'),(3,'Cyber Fraud','Cyber Crime','Investigating'),(4,'Jewelry Theft','Burglary','Open'),(5,'Museum Artifact Theft','Artifact Smuggling','Closed');"

!mysql -u root -proot -e "USE forensic_db; INSERT INTO investigator VALUES (101,'Rahul Sharma','Inspector'),(102,'Aisha Khan','Sub Inspector'),(103,'Arjun Nair','Detective'),(104,'Sneha Reddy','Forensic Analyst'),(105,'Vikram Patel','Crime Officer');"

!mysql -u root -proot -e "USE forensic_db; INSERT INTO evidence VALUES (201,1,'Fingerprint','Fingerprint on vault','2025-01-10'),(202,2,'Knife','Knife recovered','2025-01-12'),(203,3,'Laptop','Hacked laptop','2025-01-15'),(204,4,'CCTV','Camera footage','2025-01-18'),(205,5,'Ancient Coin','Rare coin found','2025-02-02');"

!mysql -u root -proot -e "USE forensic_db; INSERT INTO custody VALUES (301,201,101,'2025-01-11'),(302,202,102,'2025-01-13'),(303,203,103,'2025-01-16'),(304,204,104,'2025-01-19'),(305,205,105,'2025-02-03');"

!mysql -u root -proot -e 'USE forensic_db; SELECT * FROM cases;'

!ngrok config add-authtoken 3CfhkN3bcx5fcp77723mgFCP4i1_3c9kHRqvxWb3NAbeaLeya

from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(public_url)

from flask import Flask, request, redirect

from flask import Flask, request, redirect, url_for

app = Flask(__name__, static_folder='static')

!mkdir static

!ls

!mv forensic.png static/

!ls static

from flask import Flask, request, redirect
import mysql.connector
from pyngrok import ngrok

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="forensic_db"
)

cursor = db.cursor()

# ================= TEMPLATE =================

def template(content):

    return f"""

    <html>

    <head>

    <title>Forensic Evidence Management System</title>

    <style>

    body {{
        font-family: Arial;
        background-color: #f4f4f4;
        margin:0;
        padding:0;
        text-align:center;
    }}

    .header {{
        background:#1e293b;
        color:white;
        padding:20px;
    }}

    .nav {{
        background:#0f172a;
        padding:15px;
    }}

    .nav a {{
        color:white;
        text-decoration:none;
        margin:10px;
        padding:10px 15px;
        background:#2563eb;
        border-radius:5px;
    }}

    table {{
        width:90%;
        margin:auto;
        border-collapse:collapse;
        background:white;
    }}

    th {{
        background:#1e293b;
        color:white;
    }}

    th, td {{
        padding:12px;
        border:1px solid #ddd;
    }}

    input {{
        padding:8px;
        margin:5px;
        width:250px;
    }}

    button {{
        padding:8px 15px;
        background:#2563eb;
        color:white;
        border:none;
        border-radius:5px;
    }}

    img {{
        width:80%;
        border-radius:10px;
        margin-top:20px;
    }}

    .card {{
        background:white;
        width:90%;
        margin:auto;
        padding:20px;
        border-radius:10px;
        box-shadow:0px 0px 10px lightgray;
    }}

    </style>

    </head>

    <body>

    <div class='header'>
    <h1>Forensic Evidence Management System</h1>
    </div>

    <div class='nav'>

    <a href='/'>Home</a>
    <a href='/cases'>Cases</a>
    <a href='/investigators'>Investigators</a>
    <a href='/evidence'>Evidence</a>
    <a href='/custody'>Custody</a>
    <a href='/dashboard'>Dashboard</a>

    </div>

    <br>

    <div class='card'>

    {content}

    </div>

    </body>

    </html>

    """

# ================= HOME =================

@app.route('/')
def home():

    return template("""

    <h2>Welcome to Forensic Evidence Management System</h2>

    <img
    src="/static/forensic.png"
    style="
    width:900px;
    height:450px;
    border-radius:15px;
    object-fit:cover;
    border:2px solid black;
    "

    >

    <br><br>

    <h3>
    Manage criminal investigations, evidence tracking,
    investigators and custody reports efficiently.
    </h3>

    """)

# ================= CASES =================

@app.route('/cases', methods=['GET','POST'])
def cases():

    if request.method == 'POST':

        keyword = request.form['search']

        cursor.execute("""

        SELECT * FROM cases

        WHERE
        case_id LIKE %s OR
        case_name LIKE %s OR
        crime_type LIKE %s OR
        status LIKE %s

        """,

        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        ))

    else:

        cursor.execute("SELECT * FROM cases")

    data = cursor.fetchall()

    content = """

    <h2>Cases</h2>

    <a href='/add_case'>Add Case</a>

    <br><br>

    <form method='post'>

    <input name='search' placeholder='Search anything in cases'>

    <button type='submit'>Search</button>

    </form>

    <br>

    <table>

    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Crime</th>
    <th>Status</th>
    <th>Action</th>
    </tr>

    """

    for row in data:

        content += f"""

        <tr>

        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>

        <td>

        <a href='/update_case/{row[0]}'>Update</a>

        |

        <a href='/delete_case/{row[0]}'>Delete</a>

        </td>

        </tr>

        """

    content += "</table>"

    return template(content)

# ================= ADD CASE =================

@app.route('/add_case', methods=['GET','POST'])
def add_case():

    if request.method == 'POST':

        cursor.execute(
            "INSERT INTO cases VALUES(%s,%s,%s,%s)",
            (
                request.form['id'],
                request.form['name'],
                request.form['crime'],
                request.form['status']
            )
        )

        db.commit()

        return redirect('/cases')

    return template("""

    <h2>Add Case</h2>

    <form method='post'>

    <input name='id' placeholder='Case ID'><br>

    <input name='name' placeholder='Case Name'><br>

    <input name='crime' placeholder='Crime Type'><br>

    <input name='status' placeholder='Status'><br>

    <button type='submit'>Add</button>

    </form>

    """)

@app.route('/delete_case/<int:id>')
def delete_case(id):

    # Find investigators linked to this case

    cursor.execute("""

    SELECT investigator_id

    FROM custody cu

    JOIN evidence e
    ON cu.evidence_id = e.evidence_id

    WHERE e.case_id = %s

    """, (id,))

    investigators = cursor.fetchall()

    # Delete custody records

    cursor.execute("""

    DELETE cu FROM custody cu

    JOIN evidence e
    ON cu.evidence_id = e.evidence_id

    WHERE e.case_id = %s

    """, (id,))

    # Delete evidence

    cursor.execute(
        "DELETE FROM evidence WHERE case_id=%s",
        (id,)
    )

    # Delete investigators connected to this case

    for inv in investigators:

        cursor.execute(
            "DELETE FROM investigator WHERE investigator_id=%s",
            (inv[0],)
        )

    # Delete case

    cursor.execute(
        "DELETE FROM cases WHERE case_id=%s",
        (id,)
    )

    db.commit()

    return redirect('/cases')

# ================= UPDATE CASE =================

@app.route('/update_case/<int:id>', methods=['GET','POST'])
def update_case(id):

    if request.method == 'POST':

        cursor.execute("""

        UPDATE cases

        SET
        case_name=%s,
        crime_type=%s,
        status=%s

        WHERE case_id=%s

        """,

        (
            request.form['name'],
            request.form['crime'],
            request.form['status'],
            id
        ))

        db.commit()

        return redirect('/cases')

    cursor.execute(
        "SELECT * FROM cases WHERE case_id=%s",
        (id,)
    )

    row = cursor.fetchone()

    return template(f"""

    <h2>Update Case</h2>

    <form method='post'>

    <input name='name' value='{row[1]}'><br>

    <input name='crime' value='{row[2]}'><br>

    <input name='status' value='{row[3]}'><br>

    <button type='submit'>Update</button>

    </form>

    """)

# ================= INVESTIGATORS =================

@app.route('/investigators', methods=['GET','POST'])
def investigators():

    if request.method == 'POST':

        keyword = request.form['search']

        cursor.execute("""

        SELECT * FROM investigator

        WHERE
        investigator_id LIKE %s OR
        name LIKE %s OR
        rank_name LIKE %s

        """,

        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        ))

    else:

        cursor.execute("SELECT * FROM investigator")

    data = cursor.fetchall()

    content = "<h2>Investigators</h2>"

    content += "<a href='/add_investigator'>Add Investigator</a><br><br>"

    content += """

    <form method='post'>

    <input name='search' placeholder='Search anything'>

    <button>Search</button>

    </form>

    <br>

    <table>

    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Rank</th>
    <th>Action</th>
    </tr>

    """

    for row in data:

        content += f"""

        <tr>

        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>

        <td>

        <a href='/update_investigator/{row[0]}'>Update</a>

        |

        <a href='/delete_investigator/{row[0]}'>Delete</a>

        </td>

        </tr>

        """

    content += "</table>"

    return template(content)

# ================= ADD INVESTIGATOR =================

@app.route('/add_investigator', methods=['GET','POST'])
def add_investigator():

    if request.method == 'POST':

        cursor.execute(
            "INSERT INTO investigator VALUES(%s,%s,%s)",
            (
                request.form['id'],
                request.form['name'],
                request.form['rank']
            )
        )

        db.commit()

        return redirect('/investigators')

    return template("""

    <h2>Add Investigator</h2>

    <form method='post'>

    <input name='id' placeholder='ID'><br>

    <input name='name' placeholder='Name'><br>

    <input name='rank' placeholder='Rank'><br>

    <button>Add</button>

    </form>

    """)

@app.route('/delete_investigator/<int:id>')
def delete_investigator(id):

    cursor.execute(
        "DELETE FROM custody WHERE investigator_id=%s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM investigator WHERE investigator_id=%s",
        (id,)
    )

    db.commit()

    return redirect('/investigators')

# ================= UPDATE INVESTIGATOR =================

@app.route('/update_investigator/<int:id>', methods=['GET','POST'])
def update_investigator(id):

    if request.method == 'POST':

        cursor.execute("""

        UPDATE investigator

        SET
        name=%s,
        rank_name=%s

        WHERE investigator_id=%s

        """,

        (
            request.form['name'],
            request.form['rank'],
            id
        ))

        db.commit()

        return redirect('/investigators')

    cursor.execute(
        "SELECT * FROM investigator WHERE investigator_id=%s",
        (id,)
    )

    row = cursor.fetchone()

    return template(f"""

    <h2>Update Investigator</h2>

    <form method='post'>

    <input name='name' value='{row[1]}'><br>

    <input name='rank' value='{row[2]}'><br>

    <button>Update</button>

    </form>

    """)
# ================= EVIDENCE =================

@app.route('/evidence', methods=['GET','POST'])
def evidence():

    data = []

    if request.method == 'POST':

        keyword = request.form['search']

        query = """

        SELECT * FROM evidence

        WHERE

        evidence_id = %s OR
        case_id = %s OR

        type LIKE %s OR
        description LIKE %s OR

        CAST(collected_date AS CHAR) = %s

        """

        try:

            id_value = int(keyword)

        except:

            id_value = -1

        values = (

            id_value,
            id_value,

            '%' + keyword + '%',
            '%' + keyword + '%',

            keyword

        )

        cursor.execute(query, values)

        data = cursor.fetchall()

    else:

        cursor.execute("SELECT * FROM evidence")

        data = cursor.fetchall()

    content = """

    <h2>Evidence Records</h2>

    <a href='/add_evidence'>Add Evidence</a>

    <br><br>

    <form method='post'>

    <input
    name='search'
    placeholder='Search Evidence'
    style='padding:10px; width:300px;'
    >

    <button type='submit'>Search</button>

    </form>

    <br>

    <table>

    <tr>

    <th>Evidence ID</th>
    <th>Case ID</th>
    <th>Type</th>
    <th>Description</th>
    <th>Collected Date</th>
    <th>Action</th>

    </tr>

    """

    for row in data:

        content += f"""

        <tr>

        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>{row[4]}</td>

        <td>

        <a href='/update_evidence/{row[0]}'>Update</a>

        |

        <a href='/delete_evidence/{row[0]}'>Delete</a>

        </td>

        </tr>

        """

    content += "</table>"

    return template(content)

# ================= ADD EVIDENCE =================

@app.route('/add_evidence', methods=['GET','POST'])
def add_evidence():

    if request.method == 'POST':

        cursor.execute(
            "INSERT INTO evidence VALUES(%s,%s,%s,%s,%s)",
            (
                request.form['id'],
                request.form['case_id'],
                request.form['type'],
                request.form['description'],
                request.form['date']
            )
        )

        db.commit()

        return redirect('/evidence')

    return template("""

    <h2>Add Evidence</h2>

    <form method='post'>

    <input name='id' placeholder='Evidence ID'><br>

    <input name='case_id' placeholder='Case ID'><br>

    <input name='type' placeholder='Type'><br>

    <input name='description' placeholder='Description'><br>

    <input name='date' placeholder='YYYY-MM-DD'><br>

    <button>Add</button>

    </form>

    """)

@app.route('/delete_evidence/<int:id>')
def delete_evidence(id):

    cursor.execute(
        "DELETE FROM custody WHERE evidence_id=%s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM evidence WHERE evidence_id=%s",
        (id,)
    )

    db.commit()

    return redirect('/evidence')

# ================= UPDATE EVIDENCE =================

@app.route('/update_evidence/<int:id>', methods=['GET','POST'])
def update_evidence(id):

    if request.method == 'POST':

        cursor.execute("""

        UPDATE evidence

        SET
        type=%s,
        description=%s,
        collected_date=%s

        WHERE evidence_id=%s

        """,

        (
            request.form['type'],
            request.form['description'],
            request.form['date'],
            id
        ))

        db.commit()

        return redirect('/evidence')

    cursor.execute(
        "SELECT * FROM evidence WHERE evidence_id=%s",
        (id,)
    )

    row = cursor.fetchone()

    return template(f"""

    <h2>Update Evidence</h2>

    <form method='post'>

    <input name='type' value='{row[2]}'><br>

    <input name='description' value='{row[3]}'><br>

    <input name='date' value='{row[4]}'><br>

    <button>Update</button>

    </form>

    """)
    # ================= CUSTODY =================

@app.route('/custody', methods=['GET','POST'])
def custody():

    if request.method == 'POST':

        keyword = request.form['search']

        cursor.execute("""

        SELECT * FROM custody

        WHERE
        custody_id LIKE %s OR
        evidence_id LIKE %s OR
        investigator_id LIKE %s OR
        date_received LIKE %s

        """,

        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        ))

    else:

        cursor.execute("SELECT * FROM custody")

    data = cursor.fetchall()

    content = """

    <h2>Custody Records</h2>

    <a href='/add_custody'>Add Custody</a>

    <br><br>

    <form method='post'>

    <input name='search' placeholder='Search custody records'>

    <button type='submit'>Search</button>

    </form>

    <br>

    <table>

    <tr>
    <th>Custody ID</th>
    <th>Evidence ID</th>
    <th>Investigator ID</th>
    <th>Date Received</th>
    <th>Action</th>
    </tr>

    """

    for row in data:

        content += f"""

        <tr>

        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>

        <td>

        <a href='/update_custody/{row[0]}'>Update</a>

        |

        <a href='/delete_custody/{row[0]}'>Delete</a>

        </td>

        </tr>

        """

    content += "</table>"

    return template(content)

# ================= ADD CUSTODY =================

@app.route('/add_custody', methods=['GET','POST'])
def add_custody():

    if request.method == 'POST':

        cursor.execute(
            "INSERT INTO custody VALUES(%s,%s,%s,%s)",
            (
                request.form['id'],
                request.form['evidence'],
                request.form['investigator'],
                request.form['date']
            )
        )

        db.commit()

        return redirect('/custody')

    return template("""

    <h2>Add Custody</h2>

    <form method='post'>

    <input name='id' placeholder='Custody ID'><br>

    <input name='evidence' placeholder='Evidence ID'><br>

    <input name='investigator' placeholder='Investigator ID'><br>

    <input name='date' placeholder='YYYY-MM-DD'><br>

    <button>Add Custody</button>

    </form>

    """)

@app.route('/delete_custody/<int:id>')
def delete_custody(id):

    cursor.execute(
        "DELETE FROM custody WHERE custody_id=%s",
        (id,)
    )

    db.commit()

    return redirect('/custody')
# ================= UPDATE CUSTODY =================

@app.route('/update_custody/<int:id>', methods=['GET','POST'])
def update_custody(id):

    if request.method == 'POST':

        cursor.execute("""

        UPDATE custody

        SET
        evidence_id=%s,
        investigator_id=%s,
        date_received=%s

        WHERE custody_id=%s

        """,

        (
            request.form['evidence'],
            request.form['investigator'],
            request.form['date'],
            id
        ))

        db.commit()

        return redirect('/custody')

    cursor.execute(
        "SELECT * FROM custody WHERE custody_id=%s",
        (id,)
    )

    row = cursor.fetchone()

    return template(f"""

    <h2>Update Custody</h2>

    <form method='post'>

    <input name='evidence' value='{row[1]}'><br>

    <input name='investigator' value='{row[2]}'><br>

    <input name='date' value='{row[3]}'><br>

    <button>Update</button>

    </form>

    """)

# ================= DASHBOARD =================

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

    data = []

    if request.method == 'POST':

        keyword = request.form['search']

        query = """

        SELECT

        c.case_id,
        c.case_name,
        c.crime_type,
        c.status,

        e.evidence_id,
        e.type,
        e.description,
        e.collected_date,

        i.investigator_id,
        i.name,
        i.rank_name,

        cu.custody_id,
        cu.date_received

        FROM cases c

        LEFT JOIN evidence e
        ON c.case_id = e.case_id

        LEFT JOIN custody cu
        ON e.evidence_id = cu.evidence_id

        LEFT JOIN investigator i
        ON cu.investigator_id = i.investigator_id

        WHERE

        c.case_id = %s OR
        e.evidence_id = %s OR
        i.investigator_id = %s OR
        cu.custody_id = %s OR

        c.case_name LIKE %s OR
        c.crime_type LIKE %s OR
        c.status LIKE %s OR

        e.type LIKE %s OR
        e.description LIKE %s OR
        CAST(e.collected_date AS CHAR) = %s OR

        i.name LIKE %s OR
        i.rank_name LIKE %s OR

        CAST(cu.date_received AS CHAR) = %s

        """

        try:

            id_value = int(keyword)

        except:

            id_value = -1

        values = (

            id_value,
            id_value,
            id_value,
            id_value,

            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%',

            '%' + keyword + '%',
            '%' + keyword + '%',
            keyword,

            '%' + keyword + '%',
            '%' + keyword + '%',

            keyword

        )

        cursor.execute(query, values)

        data = cursor.fetchall()

    else:

        cursor.execute("""

        SELECT

        c.case_id,
        c.case_name,
        c.crime_type,
        c.status,

        e.evidence_id,
        e.type,
        e.description,
        e.collected_date,

        i.investigator_id,
        i.name,
        i.rank_name,

        cu.custody_id,
        cu.date_received

        FROM cases c

        LEFT JOIN evidence e
        ON c.case_id = e.case_id

        LEFT JOIN custody cu
        ON e.evidence_id = cu.evidence_id

        LEFT JOIN investigator i
        ON cu.investigator_id = i.investigator_id

        """)

        data = cursor.fetchall()

    content = """

    <h2>Complete Investigation Dashboard</h2>

    <form method='post'>

    <input
    name='search'
    placeholder='Search anything'
    style='width:350px; padding:10px;'
    >

    <button type='submit'>Search</button>

    </form>

    <br>

    <table>

    <tr>

    <th>Case ID</th>
    <th>Case Name</th>
    <th>Crime</th>
    <th>Status</th>

    <th>Evidence ID</th>
    <th>Evidence Type</th>
    <th>Description</th>
    <th>Date</th>

    <th>Investigator ID</th>
    <th>Investigator</th>
    <th>Rank</th>

    <th>Custody ID</th>
    <th>Custody Date</th>

    </tr>

    """

    for row in data:

        content += f"""

        <tr>

        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>

        <td>{row[4]}</td>
        <td>{row[5]}</td>
        <td>{row[6]}</td>
        <td>{row[7]}</td>

        <td>{row[8]}</td>
        <td>{row[9]}</td>
        <td>{row[10]}</td>

        <td>{row[11]}</td>
        <td>{row[12]}</td>

        </tr>

        """

    content += "</table>"

    return template(content)
# ================= RUN WEBSITE =================

public_url = ngrok.connect(5000)

print("Website Link:", public_url)

app.run(port=5000)

