from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Genre, Game
from datetime import date

engine = create_engine('sqlite:///videogamecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# Users
User1 = User(name="Tinny Tim", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
dbsession.add(User1)
dbsession.commit()

User2 = User(name="Johnny Appleseed", email="iloveapples@mailinator.com",
             picture='https://farm3.staticflickr.com/2399/3838746058_440bb367b0_m.jpg')
dbsession.add(User2)
dbsession.commit()

# Genres
Genre1 = Genre(name="Action")
dbsession.add(Genre1)
dbsession.commit()

Genre2 = Genre(name="Racing")
dbsession.add(Genre2)
dbsession.commit()

Genre3 = Genre(name="RPG")
dbsession.add(Genre3)
dbsession.commit()

Genre4 = Genre(name="Sports")
dbsession.add(Genre4)
dbsession.commit()

Genre5 = Genre(name="Simulation")
dbsession.add(Genre5)
dbsession.commit()

Genre6 = Genre(name="Strategy")
dbsession.add(Genre6)
dbsession.commit()

Genre7 = Genre(name="FPS")
dbsession.add(Genre7)
dbsession.commit()

# Games
Game1 = Game(name="Grand Theft Auto V",
             description="Assemble your crew for the biggest online adventure yet.",
             price="$69.99",
             developer="Rockstar Games",
             release_date=date(2015, 4, 14),
             platform="PC",
             genre_id="1",
             user_id="1"
             )
dbsession.add(Game1)
dbsession.commit()

Game2 = Game(name="Rocket League",
             description="Soccer meets driving!",
             price="$21.00",
             developer="RPsyonix Inc",
             release_date=date(2015, 7, 7),
             platform="XBOX",
             genre_id="2",
             user_id="2"
             )
dbsession.add(Game2)
dbsession.commit()

Game3 = Game(name="Fallout 4",
             description="Fight to survive in this next generation open world game.",
             price="$41.00",
             developer="Bethesda Game Studios",
             release_date=date(2015, 11, 1),
             platform="PS4",
             genre_id="3",
             user_id="1"
             )
dbsession.add(Game3)
dbsession.commit()

Game4 = Game(name="NBA 2K17",
             description="The NBA 2K franchise continues to stake its claim as the most authentic sports video game.",
             price="$89.99",
             developer="Visual Concepts",
             release_date=date(2016, 9, 20),
             platform="XBOX",
             genre_id="4",
             user_id="2"
             )
dbsession.add(Game4)
dbsession.commit()

Game5 = Game(name="Euro Truck Simulator 2",
             description="Travel across Eurpoe and build your trucking company.",
             price="$69.99",
             developer="SCS Software",
             release_date=date(2013, 6, 16),
             platform="PS4",
             genre_id="5",
             user_id="1"
             )
dbsession.add(Game5)
dbsession.commit()

Game6 = Game(name="Sid Meier's Civilization VI",
             description="Interact with your world, expand your empire, advance your culture, and compete against history's greatest leaders.",
             price="$52.49",
             developer="Firaxis",
             release_date=date(2016, 10, 20),
             platform="PC",
             genre_id="6",
             user_id="2"
             )
dbsession.add(Game6)
dbsession.commit()

Game7 = Game(name="Counter-Strike: Global Offensive",
             description="Fast actioned, team based, economy and strategy driven first person shooter.",
             price="$16.99",
             developer="Valve",
             release_date=date(2012, 8, 21),
             platform="PC",
             genre_id="7",
             user_id="1"
             )
dbsession.add(Game7)
dbsession.commit()

print "Games and genres successfully added!"
