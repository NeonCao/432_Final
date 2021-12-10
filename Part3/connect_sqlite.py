import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

#################################################################### Creat Tables

#------------------# Entities

query = """
    CREATE TABLE Department(
    dep_id INT(12) NOT NULL UNIQUE,
    dep_Name VARCHAR(120) NOT NULL UNIQUE CHECK (dep_Name LIKE 'Department %'),
    chair_fName VARCHAR(40) NOT NULL,
    chair_lName VARCHAR(40) NOT NULL,
    dep_stuffPop INT(60),
    PRIMARY KEY (dep_id)
    );
    """
cursor.execute(query)

query = """
    CREATE TABLE Major(
    major_Code VARCHAR(3) NOT NULL UNIQUE CHECK (length(major_Code) = 3),
    major_Name VARCHAR(120) NOT NULL UNIQUE,
    dep_id INT(12) NOT NULL UNIQUE,
    PRIMARY KEY (major_Code),
    FOREIGN KEY (dep_id)  
    REFERENCES Department(dep_id)
    );
    """
cursor.execute(query)

query = """
    CREATE TABLE Event(
    event_id INT(12) NOT NULL UNIQUE,
    event_Name VARCHAR(120) NOT NULL,
    event_startDate TEXT NOT NULL,
    event_endDate TEXT NOT NULL,
    PRIMARY KEY (event_id),
    CHECK (event_startDate <= event_endDate)
    );
    """
    # event_CreationDate TEXT DEFAULT(sysdate),
    # CHECK (event_startDate > date(event_CreationDate, 'YYYY-MM-DD'))
    # CHECK (event_endDate > date(event_CreationDate, 'YYYY-MM-DD'))

    # CHECK (event_startDate > date('now'))
cursor.execute(query)

query = """
    CREATE TABLE Student(
    stu_id INT(12) NOT NULL UNIQUE,
    stu_fName VARCHAR(40) NOT NULL,
    stu_lName VARCHAR(40) NOT NULL,
    stu_Initial VARCHAR(3) NOT NULL CHECK (length(stu_Initial) > 1),
    PRIMARY KEY (stu_id)
    );
    """
cursor.execute(query)

# query = """
#     CREATE TRIGGER Event_dateCheck BEFORE INSERT ON Event
#     FOR EACH ROW
#     BEGIN
#         CASE 
#             WHEN event_startDate > date('now') AND event_endDate > date('now') THEN
#             'Good'
#             ELSE raise(ignore, 'event_endDate and event_startDate must be future')
#     END;
#     """
# cursor.execute(query)

#------------------# many-to-many relationships

query = """
    CREATE TABLE Department_Event (
    dep_id INT(12) NOT NULL,
    event_id INT(12) NOT NULL,
    PRIMARY KEY (dep_id, event_id),
    FOREIGN KEY (dep_id) REFERENCES Department(dep_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
    ); """
cursor.execute(query)

query = """
    CREATE TABLE Student_Event (
    stu_id INT(12) NOT NULL,
    event_id INT(12) NOT NULL,
    PRIMARY KEY (stu_id, event_id),
    FOREIGN KEY (stu_id) REFERENCES Student(stu_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
    ); """
cursor.execute(query)

query = """
    CREATE TABLE Major_Student (
    major_Code VARCHAR(3) NOT NULL CHECK (length(major_Code) = 3),
    stu_id INT(12) NOT NULL,
    PRIMARY KEY (major_Code, stu_id),
    FOREIGN KEY (major_Code) REFERENCES Major(major_Code),
    FOREIGN KEY (stu_id) REFERENCES Student(stu_id)
    ); """
cursor.execute(query)

# Execute query, the result is stored in cursor
# cursor.execute(query)

############################################################################ Insert row into table

cursor.executescript("""
    INSERT INTO Department VALUES (1, 'Department of Art and Science', 'Leo', 'South', '12');
    INSERT INTO Department VALUES (2, 'Department of Computer', 'Meow', 'Meao', '24');
    INSERT INTO Department VALUES (3, 'Department of Physics', 'Sa', 'Mumu', '36');
    INSERT INTO Department VALUES (4, 'Department of Photography', 'Sean', 'Black', '48');
    INSERT INTO Department VALUES (5, 'Department of Pancake', 'Chris', 'Roberts', '97');
""")

cursor.executescript("""
    INSERT INTO Major VALUES ('NEO', 'New Engineer Operation', 1);
    INSERT INTO Major VALUES ('CSS', 'Computer Science', 2);
    INSERT INTO Major VALUES ('PHY', 'Physics', 3);
    INSERT INTO Major VALUES ('PHO', 'Photgraphy', 4);
    INSERT INTO Major VALUES ('SCS', 'Star Citizen type of Scamology', 5);
""")

cursor.executescript("""
    INSERT INTO Event (event_id, event_Name, event_startDate, event_endDate) VALUES (0097, 'Due Rushing Party', '2022-10-10', '2022-10-24');
    INSERT INTO Event VALUES (0063, 'Photography Discussion Party', '2022-10-10', '2022-10-30');
    INSERT INTO Event VALUES (0074, 'How to Code better', '2022-02-25', '2022-02-26');
    INSERT INTO Event VALUES (0001, 'No More Exam Activity', '2022-08-10', '2022-09-10');
    INSERT INTO Event VALUES (2042, 'IAE 2951 Scam Event', '2951-11-20', '2951-12-01');
""")

cursor.executescript("""
    INSERT INTO Student VALUES (123456789012, 'Sa', 'Mumu', 'SM');
    INSERT INTO Student VALUES (472429492383, 'Leo', 'South', 'LS');
    INSERT INTO Student VALUES (583573458245, 'Meow', 'Meao', 'MM');
    INSERT INTO Student VALUES (248067949334, 'Sean', 'Black', 'SB');
    INSERT INTO Student VALUES (104843472984, 'Chris', 'Roberts', 'CR');
""")

cursor.executescript("""
    INSERT INTO Department_Event VALUES (1, 0097);
    INSERT INTO Department_Event VALUES (2, 0063);
    INSERT INTO Department_Event VALUES (3, 0074);
    INSERT INTO Department_Event VALUES (4, 0001);
    INSERT INTO Department_Event VALUES (5, 2042);
    INSERT INTO Department_Event VALUES (1, 2042);
    INSERT INTO Department_Event VALUES (2, 2042);
    INSERT INTO Department_Event VALUES (3, 2042);
    INSERT INTO Department_Event VALUES (4, 2042);

    INSERT INTO Student_Event VALUES (123456789012, 0097);
    INSERT INTO Student_Event VALUES (472429492383, 0063);
    INSERT INTO Student_Event VALUES (583573458245, 0074);
    INSERT INTO Student_Event VALUES (248067949334, 0001);
    INSERT INTO Student_Event VALUES (104843472984, 2042);

    INSERT INTO Major_Student VALUES ('NEO', 123456789012);
    INSERT INTO Major_Student VALUES ('CSS', 472429492383);
    INSERT INTO Major_Student VALUES ('PHY', 583573458245);
    INSERT INTO Major_Student VALUES ('PHO', 248067949334);
    INSERT INTO Major_Student VALUES ('SCS', 104843472984);
    INSERT INTO Major_Student VALUES ('PHY', 123456789012);
    INSERT INTO Major_Student VALUES ('PHO', 472429492383);

""")
# query = """
#     INSERT INTO Department
#     VALUES (1, 'Department of Art and Science', 'Leo', 'South', '12');
#     """
# cursor.execute(query)

# query = """
#     INSERT INTO Major
#     VALUES ('NEO', 'New Engineer Operation', 0001);
#     """
# cursor.execute(query)

# query = """
#     INSERT INTO Event
#     VALUES (0097, 'Due Rushing Party', '2022-10-10', '2022-10-24');
#     """
# cursor.execute(query)

# query = """
#     INSERT INTO Student
#     VALUES (123456789012, 'Sa', 'Mumu', 'SM');
#     """
# cursor.execute(query)

# Select data

############################################################################ 5 quires

#query1# List all the student whose major is computer science

query = """
    SELECT a.*, c.major_Name
    FROM Student a, Major c
    JOIN Major_Student AS b
    ON a.stu_id = b.stu_id AND b.major_Code = c.major_Code
    Where c.major_Name = 'Computer Science';
    """
cursor.execute(query)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print(df)
print(df.columns)

#query2# List all Events that’s ends after a select date

query = """
    SELECT *
    FROM Event
    Where event_startDate <= '2024-12-31';
    """
cursor.execute(query)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print(df)
print(df.columns)

#query3# Find all deprtments with over or equals to 30 pops, sorting them by pop number high to low.

query = """
    SELECT *
    FROM Department
    Where dep_stuffPop >= 30
    ORDER BY dep_stuffPop DESC;
    """
cursor.execute(query)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print(df)
print(df.columns)

#query4# Find all events a student has attended with student’s Name

query = """
    SELECT a.*, c.stu_fName, c.stu_lName
    FROM Event a, Student c
    JOIN Student_Event AS b
    ON a.event_id = b.event_id AND b.stu_id = c.stu_id
    Where c.stu_fName = 'Sean' AND c.stu_lName = 'Black';
    """
cursor.execute(query)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print(df)
print(df.columns)

#query5# List all students and its major, order by student's firstName ASC

query = """
    SELECT a.*, c.major_Name
    FROM Student a, Major c
    JOIN Major_Student AS b
    ON a.stu_id = b.stu_id AND b.major_Code = c.major_Code
    ORDER BY stu_fName ASC;
    """
cursor.execute(query)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print(df)
print(df.columns)

query = """
    SELECT *
    FROM Department
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)

# Examine dataframe
print(df)
print(df.columns)

# Example to extract a specific column
# print(df['name'])


# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
