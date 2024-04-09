import psycopg2
from psycopg2 import Error

def create_connection(username, password, database):
    # create connection to PostgreSQL database
    try:
        connection = psycopg2.connect(
            user=username,
            password=password,
            host="localhost",
            port="5432",
            database=database
        )
        return connection
    except (Exception, Error) as error:
        print("Error !! connecting to PostgreSQL", error)

def fetch_contacts(connection):
    #fetch active contacts from the database
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, country, phone, email FROM contacts WHERE active=true;")
        contacts = cursor.fetchall()
        return contacts
    except (Exception, Error) as error:
        print("Error !! fetching contacts:", error)

def generate_html_table(contacts):
    # HTML 
    table_html = """
    <html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <table class="table">
                <thead class="thead-dark">
                     <tr>
                     <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Country</th>
                        <th scope="col">Phone</th>
                        <th scope="col">Email</th>
                    </tr>
                </thead>
                <tbody>
    """
    row_number = 1
    for contact in contacts:
        country = contact[1] if contact[1] is not None else ""
        
        table_html += f"""
                    <tr>
                    <td>{row_number}</td>
                    <td>{contact[0]}</td>
                        <td>{country}</td>
                        <td>{contact[2]}</td>
                        <td>{contact[3]}</td>                        <td>{contact[3]}</td>
                    </tr>
        """
        row_number+=1
    table_html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    return table_html

def write_to_html(html_content):
    # write html content to file
    try:
        with open("pg_output.html", "w") as file:
            file.write(html_content)
    except IOError as e:
        print("Error !!  writing to file:", e)

def main():
    #database credentials
    username = input("Username: ")
    password = input("Password: ")
    database = input("Database name: ")

    #create connection to Postgres
    connection = create_connection(username, password, database)
    if connection:
        # fetch contacts from database
        contacts = fetch_contacts(connection)
        if contacts:
            html_content = generate_html_table(contacts)
            write_to_html(html_content)
        # closte database connection
        connection.close()

if __name__ == "__main__":
    main()
