"""
Data Loader for Guess Who Game
Handles loading initial data into the database.
"""

from typing import List
from database_manager import DatabaseManager
from person_model import Person


class DataLoader:
    """Handles loading initial data into the database."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize with database manager.
        
        Args:
            db_manager (DatabaseManager): Database manager instance
        """
        self.db_manager = db_manager
    
    def get_sample_data(self) -> List[List]:
        """
        Get sample data for the game.
        
        Returns:
            List[List]: Sample person data
        """
        return [
            [1, "Lionel Messi", "M", 36, "Football", "SPORTS", "Argentina"],
            [2, "Cristiano Ronaldo", "M", 38, "Football", "SPORTS", "Portugal"],
            [3, "Roger Federer", "M", 42, "Tennis", "SPORTS", "Switzerland"],
            [4, "Rafael Nadal", "M", 37, "Tennis", "SPORTS", "Spain"],
            [5, "Mohammad Ali", "M", 74, "Boxing", "SPORTS", "USA"],
            [6, "Floyd Mayweather", "M", 46, "Boxing", "SPORTS", "USA"],
            [7, "Serena Williams", "F", 41, "Tennis", "SPORTS", "USA"],
            [8, "Venus Williams", "F", 43, "Tennis", "SPORTS", "USA"],
            [9, "Simone Biles", "F", 26, "Gymnastics", "SPORTS", "USA"],
            [10, "Tiger Woods", "M", 47, "Golf", "SPORTS", "USA"],
            [11, "Tom Brady", "M", 46, "American Football", "SPORTS", "USA"],
            [12, "Michael Jordan", "M", 60, "Basketball", "SPORTS", "USA"],
            [13, "Magnus Carlsen", "M", 32, "Chess", "SPORTS", "Norway"],
            [14, "Lebron James", "M", 38, "Basketball", "SPORTS", "USA"],
            [15, "Virat Kohli", "M", 34, "Cricket", "SPORTS", "India"],
            [16, "Sachin Tendulkar", "M", 50, "Cricket", "SPORTS", "India"],
            [17, "Lewis Hamilton", "M", 38, "Racing", "SPORTS", "Great Britain"],
            [18, "Barack Obama", "M", 62, "Activist", "POLITICS", "USA"],
            [19, "Indira Gandhi", "F", 66, "Activist", "POLITICS", "India"],
            [20, "Mahatma Gandhi", "M", 78, "Lawyer", "POLITICS", "India"],
            [21, "Nelson Mandela", "M", 95, "Lawyer", "POLITICS", "South Africa"],
            [22, "Rosa Parks", "F", 92, "Activist", "POLITICS", "USA"],
            [23, "Martin Luther King Jr", "M", 39, "Philosopher", "POLITICS", "USA"],
            [24, "Malala Yousafzai", "F", 26, "Activist", "POLITICS", "Pakistan"],
            [25, "Margaret Thatcher", "F", 87, "Activist", "POLITICS", "Great Britain"],
            [26, "Angela Merkel", "F", 69, "Activist", "POLITICS", "Germany"],
            [27, "Mother Teresa", "F", 87, "Nun", "POLITICS", "Albania"],
            [28, "Isaac Newton", "M", 84, "Physicist", "SCIENCE", "Great Britain"],
            [29, "Albert Einstein", "M", 76, "Physicist", "SCIENCE", "Germany"],
            [30, "Galileo Galilei", "M", 77, "Astronomer", "SCIENCE", "Italy"],
            [31, "Marie Curie", "F", 66, "Chemist", "SCIENCE", "Poland"],
            [32, "Niels Bohr", "M", 77, "Physicist", "SCIENCE", "Denmark"],
            [33, "Stephen Hawking", "M", 76, "Physicist", "SCIENCE", "Great Britain"],
            [34, "Nikola Tesla", "M", 86, "Engineer", "SCIENCE", "Serbia"],  # Fixed gender
            [35, "André-Marie Ampère", "M", 61, "Physicist", "SCIENCE", "France"],
            
            # Additional entertainment figures to make the game more interesting
            [36, "Taylor Swift", "F", 34, "Singer", "MUSIC", "USA"],
            [37, "Ed Sheeran", "M", 32, "Singer", "MUSIC", "Great Britain"],
            [38, "Beyoncé", "F", 42, "Singer", "MUSIC", "USA"],
            [39, "Michael Jackson", "M", 50, "Singer", "MUSIC", "USA"],
            [40, "Elvis Presley", "M", 42, "Singer", "MUSIC", "USA"],
            
            [41, "Leonardo DiCaprio", "M", 49, "Actor", "FILM", "USA"],
            [42, "Meryl Streep", "F", 74, "Actress", "FILM", "USA"],
            [43, "Robert Downey Jr", "M", 58, "Actor", "FILM", "USA"],
            [44, "Jennifer Lawrence", "F", 33, "Actress", "FILM", "USA"],
            [45, "Tom Hanks", "M", 67, "Actor", "FILM", "USA"],
            
            # Business leaders
            [46, "Elon Musk", "M", 52, "Entrepreneur", "BUSINESS", "South Africa"],
            [47, "Bill Gates", "M", 68, "Entrepreneur", "BUSINESS", "USA"],
            [48, "Warren Buffett", "M", 93, "Investor", "BUSINESS", "USA"],
            [49, "Oprah Winfrey", "F", 70, "Media Mogul", "BUSINESS", "USA"],
            [50, "Jeff Bezos", "M", 60, "Entrepreneur", "BUSINESS", "USA"]
        ]
    
    def load_sample_data(self) -> bool:
        """
        Load sample data into the database.
        
        Returns:
            bool: True if data loaded successfully
        """
        try:
            sample_data = self.get_sample_data()
            success_count = self.db_manager.add_multiple_records(sample_data)
            
            if success_count == len(sample_data):
                print(f"✅ Successfully loaded all {success_count} records")
                return True
            else:
                print(f"⚠️ Loaded {success_count}/{len(sample_data)} records")
                return success_count > 0
                
        except Exception as e:
            print(f"❌")