"""
Game Engine for Guess Who Game
Contains the main game logic and question-asking system.
"""

from typing import List, Optional
from person import Person
from database_manager import DatabaseManager
import random


class GuessWhoGame:
    """Main game engine for the Guess Who game."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the game with a database manager.
        
        Args:
            db_manager (DatabaseManager): Database manager instance
        """
        self.db_manager = db_manager
        self.people: List[Person] = []
        self.remaining_people: List[Person] = []
        self.questions_asked = 0
        self.max_questions = 20
    
    def load_people(self) -> bool:
        """
        Load all people from the database.
        
        Returns:
            bool: True if people loaded successfully
        """
        try:
            data = self.db_manager.get_all_people()
            self.people = [Person.from_tuple(row) for row in data]
            self.remaining_people = self.people.copy()
            print(f"Loaded {len(self.people)} people from database")
            return True
        except Exception as e:
            print(f"Error loading people: {e}")
            return False
    
    def start_new_game(self) -> bool:
        """
        Start a new game by loading people and resetting state.
        
        Returns:
            bool: True if game started successfully
        """
        if not self.load_people():
            return False
        
        self.questions_asked = 0
        print(f"\n🎮 Welcome to Guess Who!")
        print(f"I'm thinking of one of {len(self.people)} famous people.")
        print(f"You have {self.max_questions} questions to guess who it is!")
        print("Let's start!\n")
        return True
    
    def ask_gender_question(self) -> None:
        """Ask about the person's gender."""
        while True:
            answer = input("Is the person Male or Female? (M/F): ").strip().upper()
            if answer in ['M', 'F']:
                self.remaining_people = [p for p in self.remaining_people if p.gender == answer]
                self.questions_asked += 1
                print(f"Remaining possibilities: {len(self.remaining_people)}")
                break
            else:
                print("Please enter 'M' for Male or 'F' for Female")
    
    def ask_entertainment_question(self) -> str:
        """
        Ask about entertainment industry.
        
        Returns:
            str: 'entertainment' if in entertainment, 'other' if not
        """
        while True:
            answer = input("Is the person in an entertainment industry? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    self.remaining_people = [p for p in self.remaining_people if p.is_in_entertainment()]
                    return 'entertainment'
                else:
                    self.remaining_people = [p for p in self.remaining_people if not p.is_in_entertainment()]
                    return 'other'
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def ask_sports_question(self) -> None:
        """Ask more specific questions about sports."""
        if not any(p.plays_sport() for p in self.remaining_people):
            return
        
        while True:
            answer = input("Does the person play sports? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    self.remaining_people = [p for p in self.remaining_people if p.plays_sport()]
                else:
                    self.remaining_people = [p for p in self.remaining_people if not p.plays_sport()]
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
        
        # Further narrow down sports
        if len(self.remaining_people) > 3 and any(p.plays_tennis() for p in self.remaining_people):
            self._ask_tennis_question()
        
        if len(self.remaining_people) > 3 and any(p.plays_ball_sport() for p in self.remaining_people):
            self._ask_ball_sport_question()
    
    def _ask_tennis_question(self) -> None:
        """Ask if the person plays tennis."""
        while True:
            answer = input("Does the person play tennis? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    self.remaining_people = [p for p in self.remaining_people if p.plays_tennis()]
                else:
                    self.remaining_people = [p for p in self.remaining_people if not p.plays_tennis()]
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def _ask_ball_sport_question(self) -> None:
        """Ask if the person plays a ball sport."""
        while True:
            answer = input("Does the person play a ball sport? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    self.remaining_people = [p for p in self.remaining_people if p.plays_ball_sport()]
                else:
                    self.remaining_people = [p for p in self.remaining_people if not p.plays_ball_sport()]
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def ask_film_vs_music_question(self) -> None:
        """Distinguish between film and music industry."""
        while True:
            answer = input("Would this person be more popular on Netflix than Spotify? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    # More popular on Netflix = Film
                    self.remaining_people = [p for p in self.remaining_people if p.is_in_film()]
                else:
                    # More popular on Spotify = Music
                    self.remaining_people = [p for p in self.remaining_people if p.is_in_music()]
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def ask_nationality_question(self) -> None:
        """Ask about nationality if it helps narrow down."""
        if len(self.remaining_people) <= 2:
            return
        
        # Find the most common nationalities
        nationalities = {}
        for person in self.remaining_people:
            nat = person.nationality
            nationalities[nat] = nationalities.get(nat, 0) + 1
        
        # Ask about the most common nationality
        most_common = max(nationalities.keys(), key=lambda x: nationalities[x])
        if nationalities[most_common] > 1:
            while True:
                answer = input(f"Is the person from {most_common}? (Y/N): ").strip().upper()
                if answer in ['Y', 'N']:
                    self.questions_asked += 1
                    if answer == 'Y':
                        self.remaining_people = [p for p in self.remaining_people if p.nationality == most_common]
                    else:
                        self.remaining_people = [p for p in self.remaining_people if p.nationality != most_common]
                    break
                else:
                    print("Please enter 'Y' for Yes or 'N' for No")
    
    def ask_age_question(self) -> None:
        """Ask about age range."""
        if len(self.remaining_people) <= 2:
            return
        
        while True:
            answer = input("Is the person over 40 years old? (Y/N): ").strip().upper()
            if answer in ['Y', 'N']:
                self.questions_asked += 1
                if answer == 'Y':
                    self.remaining_people = [p for p in self.remaining_people if p.age > 40]
                else:
                    self.remaining_people = [p for p in self.remaining_people if p.age <= 40]
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def play_round(self) -> bool:
        """
        Play one round of questions.
        
        Returns:
            bool: True if should continue, False if game over
        """
        if len(self.remaining_people) == 1:
            print(f"\n🎉 I've figured it out!")
            print(f"🥁 DRUM ROLL...")
            print(f"✨ The person is: {self.remaining_people[0].name}!")
            print(f"🎯 Guessed in {self.questions_asked} questions!")
            return False
        
        if len(self.remaining_people) == 0:
            print("\n❌ Something went wrong - no people match your criteria!")
            return False
        
        if self.questions_asked >= self.max_questions:
            print(f"\n⏰ Out of questions! The remaining people are:")
            for person in self.remaining_people:
                print(f"  - {person.name}")
            return False
        
        print(f"\nQuestion {self.questions_asked + 1}/{self.max_questions}")
        print(f"Remaining people: {len(self.remaining_people)}")
        
        # Smart question asking based on remaining people
        if len(self.remaining_people) > 20:
            self.ask_gender_question()
        elif len(self.remaining_people) > 10:
            industry_type = self.ask_entertainment_question()
            if industry_type == 'entertainment':
                if any(p.plays_sport() for p in self.remaining_people):
                    self.ask_sports_question()
                else:
                    self.ask_film_vs_music_question()
        elif len(self.remaining_people) > 5:
            self.ask_nationality_question()
        else:
            self.ask_age_question()
        
        return True
    
    def play_game(self) -> None:
        """Play a complete game."""
        if not self.start_new_game():
            print("❌ Failed to start game. Please check database connection.")
            return
        
        while self.play_round():
            continue
        
        # Ask if player wants to play again
        while True:
            play_again = input("\nWould you like to play again? (Y/N): ").strip().upper()
            if play_again in ['Y', 'N']:
                if play_again == 'Y':
                    print("\n" + "="*50)
                    self.play_game()
                else:
                    print("Thanks for playing Guess Who! 👋")
                break
            else:
                print("Please enter 'Y' for Yes or 'N' for No")
    
    def show_remaining_people(self) -> None:
        """Show all remaining people (for debugging)."""
        print(f"\nRemaining {len(self.remaining_people)} people:")
        for person in self.remaining_people:
            print(f"  - {person}")
