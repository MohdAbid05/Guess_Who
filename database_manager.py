"""
Database Manager for Guess Who Game
Handles all database operations including connection, table creation, and data management.
"""

import mysql.connector
from mysql.connector import Error
import os
from typing import List, Tuple, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional; env vars can still be set manually
    pass


class DatabaseManager:
    """Manages database connections and operations for the Guess Who game."""
    
    def __init__(self, host=None, user=None, password=None, database=None):
        """
        Initialize database connection parameters.

        Values fall back to environment variables (loaded from a .env file
        if present) and finally to sensible local defaults. No credentials
        are hardcoded in source.

        Args:
            host (str): Database host
            user (str): Database username
            password (str): Database password (set via DB_PASSWORD env var / .env file)
            database (str): Database name
        """
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD')
        self.database = database or os.getenv('DB_NAME', 'computerproject')

        if not self.password:
            raise ValueError(
                "No database password found. Set DB_PASSWORD in a .env file "
                "(see .env.example) or as an environment variable."
            )
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Establish database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # First connect without a target database so we can create it
            # if it doesn't exist yet (keeps setup to a single command).
            bootstrap_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            bootstrap_cursor = bootstrap_conn.cursor()
            bootstrap_cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.database}"
            )
            bootstrap_cursor.close()
            bootstrap_conn.close()

            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Database connection established successfully")
                return True
                
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def create_table(self) -> bool:
        """
        Create the guess_who table if it doesn't exist.
        
        Returns:
            bool: True if table created/exists, False if error
        """
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS guess_who (
                sno INT PRIMARY KEY,
                P_name CHAR(40),
                GENDER CHAR(1),
                Age INT,
                OCCUPATION CHAR(30),
                INDUSTRY CHAR(35),
                Nationality CHAR(25)
            )
            """
            
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table 'guess_who' ready")
            return True
            
        except Error as e:
            print(f"Error creating table: {e}")
            return False
    
    def add_record(self, record_data: List) -> bool:
        """
        Add a single record to the database.
        
        Args:
            record_data (List): List containing [sno, name, gender, age, occupation, industry, nationality]
            
        Returns:
            bool: True if record added successfully, False otherwise
        """
        try:
            query = """
            INSERT INTO guess_who (sno, P_name, GENDER, Age, OCCUPATION, INDUSTRY, Nationality) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Ensure proper data types
            processed_data = [
                int(record_data[0]),  # sno
                str(record_data[1]),  # name
                str(record_data[2]).upper()[0],  # gender (first letter, uppercase)
                int(record_data[3]),  # age
                str(record_data[4]),  # occupation
                str(record_data[5]).upper(),  # industry (uppercase)
                str(record_data[6])   # nationality
            ]
            
            self.cursor.execute(query, processed_data)
            self.connection.commit()
            print(f"Record added: {processed_data[1]}")
            return True
            
        except Error as e:
            print(f"Error adding record: {e}")
            return False
        except (ValueError, IndexError) as e:
            print(f"Invalid data format: {e}")
            return False
    
    def add_multiple_records(self, records: List[List]) -> int:
        """
        Add multiple records to the database.
        
        Args:
            records (List[List]): List of record data lists
            
        Returns:
            int: Number of records successfully added
        """
        success_count = 0
        for record in records:
            if self.add_record(record):
                success_count += 1
        
        print(f"Added {success_count}/{len(records)} records successfully")
        return success_count
    
    def get_all_people(self) -> List[Tuple]:
        """
        Retrieve all people from the database.
        
        Returns:
            List[Tuple]: List of tuples containing person data
        """
        try:
            query = "SELECT * FROM guess_who ORDER BY sno"
            self.cursor.execute(query)
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"Error retrieving data: {e}")
            return []
    
    def get_people_by_criteria(self, **criteria) -> List[Tuple]:
        """
        Get people matching specific criteria.
        
        Args:
            **criteria: Keyword arguments for filtering (gender, industry, etc.)
            
        Returns:
            List[Tuple]: List of matching people
        """
        try:
            query = "SELECT * FROM guess_who WHERE "
            conditions = []
            values = []
            
            for key, value in criteria.items():
                if key.upper() == 'GENDER':
                    conditions.append("GENDER = %s")
                    values.append(value.upper())
                elif key.upper() == 'INDUSTRY':
                    conditions.append("INDUSTRY = %s")
                    values.append(value.upper())
                elif key.upper() == 'OCCUPATION':
                    conditions.append("OCCUPATION LIKE %s")
                    values.append(f"%{value}%")
                # Add more criteria as needed
            
            if not conditions:
                return self.get_all_people()
            
            query += " AND ".join(conditions) + " ORDER BY sno"
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"Error filtering data: {e}")
            return []
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
