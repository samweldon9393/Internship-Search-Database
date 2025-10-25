# Internship Search Database 

This repo houses the code to interact with a little sqlite database I'm using 
to keep track of information about my search for an internship for 2025. 
Hopefully I will find something, and then the data I collected through the 
process can be used to see what worked and what didn't, and maybe that will 
allow me to pass on some good advice to others in the future!

---

## Overview

- A normalized database schema.
- Scripts for inserting, updating, and querying records.
- Data visualization scripts for exploratory analysis.

The code is modular and intended for demonstration, teaching, or portfolio purposes.

---

## Repository Structure

├── schema.sql # SQL file containing CREATE TABLE statements
├── insert.py # Script for inserting new records
├── count.py # Script for quickly seeing how many applications are in the database 
├── visualize.py # Script for generating plots from query results
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## Features

- Simple, human-readable SQLite schema.
- Secure parameterized queries to prevent SQL injection.
- Visualization with libraries (Matplotlib and Pandas).
- Easy to modify or extend for new datasets.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:samweldon9393/Internship-Search-Database.git
   cd Internship-Search-Database

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt


## Usage

1. **Initialize the database schema**
   ```bash
    sqlite3 applications.db < schema.sql

2. **Add new records using**
   ```bash
   python insert.py

3. **Run queries**
   ```bash
   sqlite3 applications.db

4. **Generate visualizations**
   ```bash
   python visualize.py
