from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    sign_up_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    num_saved: Mapped[int] = mapped_column(Integer(), default=0)
    liked_characters: Mapped[list["Liked_Characters"]] = relationship("Liked_Characters", back_populates="user")
    liked_planets: Mapped[list["Liked_Planets"]] = relationship("Liked_Planets", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "sign_up_date": self.sign_up_date.isoformat(),
            "name": self.name,
            "last_name": self.last_name,
            "num_saved": self.num_saved
        }
    
class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_name: Mapped[str] = mapped_column(String(40), nullable=False)
    specie: Mapped[str] = mapped_column(String(40), nullable=False)
    height: Mapped[int] = mapped_column(Integer(), nullable=False)
    liked_by: Mapped[list["Liked_Characters"]] = relationship("Liked_Characters", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "specie": self.specie,
            "height": self.height
        }    
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(60), nullable=False)
    climate: Mapped[str] = mapped_column(String(40), nullable=False) # or true cuz i lack data
    terrain: Mapped[str] = mapped_column(String(40), nullable=False) 
    liked_by: Mapped[list["Liked_Planets"]] = relationship("Liked_Planets", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "climate": self.climate,
            "terrain": self.terrain
        }    

class Liked_Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_character: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="liked_characters")
    character: Mapped["Characters"] = relationship("Characters", back_populates="liked_by")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_character": self.id_character,
            "date": self.date.isoformat()
        }
    
class Liked_Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_planet: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="liked_planets")
    planet: Mapped["Planets"] = relationship("Planets", back_populates="liked_by")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_planet": self.id_planet,
            "date": self.date.isoformat()
        }    