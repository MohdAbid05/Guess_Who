"""
Person model for the Guess Who game.
Represents a person with all their attributes.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Person:
    """Represents a person in the Guess Who game."""
    
    sno: int
    name: str
    gender: str
    age: int
    occupation: str
    industry: str
    nationality: str
    
    def __post_init__(self):
        """Validate and normalize data after initialization."""
        self.gender = self.gender.upper() if self.gender else ''
        self.industry = self.industry.upper() if self.industry else ''
    
    @classmethod
    def from_tuple(cls, data: Tuple) -> 'Person':
        """
        Create Person instance from database tuple.
        
        Args:
            data (Tuple): Database row data
            
        Returns:
            Person: Person instance
        """
        return cls(
            sno=data[0],
            name=data[1].strip() if data[1] else '',
            gender=data[2].strip() if data[2] else '',
            age=data[3],
            occupation=data[4].strip() if data[4] else '',
            industry=data[5].strip() if data[5] else '',
            nationality=data[6].strip() if data[6] else ''
        )
    
    @classmethod
    def from_list(cls, data: List) -> 'Person':
        """
        Create Person instance from list data.
        
        Args:
            data (List): List containing person data
            
        Returns:
            Person: Person instance
        """
        return cls(
            sno=int(data[0]),
            name=str(data[1]),
            gender=str(data[2]),
            age=int(data[3]),
            occupation=str(data[4]),
            industry=str(data[5]),
            nationality=str(data[6])
        )
    
    def to_list(self) -> List:
        """
        Convert Person to list format for database insertion.
        
        Returns:
            List: Person data as list
        """
        return [
            self.sno,
            self.name,
            self.gender,
            self.age,
            self.occupation,
            self.industry,
            self.nationality
        ]
    
    def matches_criteria(self, **criteria) -> bool:
        """
        Check if person matches given criteria.
        
        Args:
            **criteria: Keyword arguments for matching
            
        Returns:
            bool: True if person matches all criteria
        """
        for key, value in criteria.items():
            key = key.lower()
            
            if key == 'gender' and self.gender.upper() != value.upper():
                return False
            elif key == 'industry' and self.industry.upper() != value.upper():
                return False
            elif key == 'occupation' and value.lower() not in self.occupation.lower():
                return False
            elif key == 'nationality' and self.nationality.lower() != value.lower():
                return False
            elif key == 'age_min' and self.age < value:
                return False
            elif key == 'age_max' and self.age > value:
                return False
        
        return True
    
    def is_in_entertainment(self) -> bool:
        """Check if person is in entertainment industry."""
        entertainment_industries = ['SPORTS', 'MUSIC', 'FILM']
        return self.industry in entertainment_industries
    
    def plays_sport(self) -> bool:
        """Check if person is in sports."""
        return self.industry == 'SPORTS'
    
    def is_in_music(self) -> bool:
        """Check if person is in music industry."""
        return self.industry == 'MUSIC'
    
    def is_in_film(self) -> bool:
        """Check if person is in film industry."""
        return self.industry == 'FILM'
    
    def plays_tennis(self) -> bool:
        """Check if person plays tennis."""
        return 'tennis' in self.occupation.lower()
    
    def plays_ball_sport(self) -> bool:
        """Check if person plays a ball sport."""
        ball_sports = ['football', 'basketball', 'tennis', 'cricket', 'baseball']
        return any(sport in self.occupation.lower() for sport in ball_sports)
    
    def __str__(self) -> str:
        """String representation of the person."""
        return f"{self.name} ({self.gender}, {self.age}, {self.occupation}, {self.industry}, {self.nationality})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Person(sno={self.sno}, name='{self.name}', gender='{self.gender}', "
                f"age={self.age}, occupation='{self.occupation}', industry='{self.industry}', "
                f"nationality='{self.nationality}')")
