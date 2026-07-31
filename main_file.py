#!/usr/bin/env python3
"""
Main entry point for the Guess Who Game
Run this file to start the game.
"""

import sys
import os
from database_manager import DatabaseManager
from game_engine import GuessWhoGame
from data_loader import DataLoader


def setup_database():
    """Set up the database and load initial data if needed."""
    print("🔧 Setting up database...")
    
    with DatabaseManager() as db:
        if not db.connection:
            print("❌ Failed to connect to database")
            print("Please ensure MySQL is running and credentials are correct")
            return None
        
        # Create table
        if not db.create_table():
            print("❌ Failed to create table")
            return None
        
        # Check if data exists
        existing_data = db.get_all_people()
        
        if not existing_data:
            print("📊 No data found. Loading sample data...")
            loader = DataLoader(db)
            if loader.load_sample_data():
                print("✅ Sample data loaded successfully!")
            else:
                print("❌ Failed to load sample data")
                return None
        else:
            print(f"✅ Database ready with {len(existing_data)} people")
        
        return db


def main():
    """Main function to run the game."""
    print("=" * 60)
    print("🎯 WELCOME TO GUESS WHO GAME!")
    print("=" * 60)
    
    # Setup database
    db = setup_database()
    if not db:
        print("\n❌ Database setup failed. Exiting...")
        sys.exit(1)
    
    # Start game
    try:
        with DatabaseManager() as db_manager:
            game = GuessWhoGame(db_manager)
            game.play_game()
    
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted by user. Goodbye!")
    
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your database connection and try again.")
    
    finally:
        print("\n🎮 Thanks for playing!")


def show_menu():
    """Show main menu options."""
    print("\n" + "=" * 40)
    print("GUESS WHO GAME - MAIN MENU")
    print("=" * 40)
    print("1. Play Game")
    print("2. Add New People to Database")
    print("3. View All People in Database")
    print("4. Setup/Reset Database")
    print("5. Exit")
    print("=" * 40)


def interactive_menu():
    """Run interactive menu system."""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                main()
            
            elif choice == '2':
                with DatabaseManager() as db:
                    if db.connection:
                        loader = DataLoader(db)
                        loader.interactive_data_entry()
                    else:
                        print("❌ Database connection failed")
            
            elif choice == '3':
                with DatabaseManager() as db:
                    if db.connection:
                        people = db.get_all_people()
                        print(f"\n📋 {len(people)} people in database:")
                        print("-" * 80)
                        for person in people:
                            print(f"{person[0]:2d}. {person[1]} ({person[2]}, {person[3]}, {person[4]}, {person[5]}, {person[6]})")
                        print("-" * 80)
                    else:
                        print("❌ Database connection failed")
            
            elif choice == '4':
                print("⚠️  This will reset the database and reload sample data.")
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    setup_database()
                else:
                    print("❌ Database reset cancelled")
            
            elif choice == '5':
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    # Check if user wants interactive menu or direct game
    if len(sys.argv) > 1 and sys.argv[1] == "--menu":
        interactive_menu()
    else:
        main()
