# Banking-System-Project
Welcome to my Banking System website! This platform showcases my journey and skills. I have created this project in Python language which runs in command line. This project also has a database and my sql has been used for the database.




## Authors

- Github : (https://github.com/Atul5641)
- Linkedln : (www.linkedin.com/in/atul-kumar-gupta-60678a330)
- X : (https://x.com/ATULGUPTA5641)

## 🚀 About Me
I'm a Passionate B.Tech Student | Seeking Opportunities in Web development and Artificial Intelligence



## Tech Stack
- PYTHON
- MYSQL


## Code Running Instructions

Steps to run this project and store data into MYSQL database

- Install my sql

- Set up environment

- Connect python and MYSQL database

### MYSQL connector code
import mysql.connector

conn = mysql.connector.connect(host='localhost', username='root', password='Atul@5641', database='banking_system')

my_cursor = conn.cursor()

conn.commit()

print("Connection successfully created!\n")



### Create tables to store data in MYSQL

 - users
- login
- transactions

 #### users table specification query

CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    contact VARCHAR(10) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(255),
    account_number BIGINT NOT NULL UNIQUE,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

#### login table specification query
CREATE TABLE login (

    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number BIGINT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    last_passwords JSON NULL, -- Optional: Store last passwords for password  history
    FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE);


#### Transactions table specification query

CREATE TABLE transactions (

    id INT AUTO_INCREMENT PRIMARY KEY,                    
    account_number VARCHAR(10),
    transaction_type VARCHAR(10),
    amount DECIMAL(10, 2),
    timestamp DATETIME,
    recipient_account_number VARCHAR(10) DEFAULT NULL);






## Feedback

If you have any feedback, suggestions, or would like to contribute to this project, your involvement is highly valued. Feel free to open an [issue](../../issues/) or submit a pull request with your ideas and enhancements. Remember, this template is a starting point, and the true magic lies in making it your own. Enjoy the journey of creating a stunning portfolio that represents your unique talents and accomplishments!

Happy coding and showcasing!
****
