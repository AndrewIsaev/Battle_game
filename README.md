# Battle game
A small game with a web interface about the battle of heroes in the style of old-school browser games.
***
## Features
- Authorization/Authentication users
- Distribution of roles between users
- CRUD for advertisement
- Search advertisement
- Comments for advertisement
***
## Technology stack
- Python 3.10.6
- Flask 2.0.2
- gunicorn 20.1.0
- Jinja2 3.0.3
- marshmallow 3.14.1
- marshmallow-dataclass 8.5.3
- mypy 0.991
***
## Start app
1. Clone project
   ```
   git clone https://github.com/AndrewIsaev/Advertisement_Service.git
2. Create virtual environment
   ```
    python3 -m venv venv
3. Activate virtual environment
   ```
    source venv/bin/activate
4. Install requirements
   ```
    pip install -r requirements.txt
5. Run flask application
   ```
    export FLASK_APP=run.py
    flask run
***
## Project structure
- `data/`: weapon data
- `templates/`: templates
- `app.py`: main app
- `base.py`: arena entity
- `classes.py`: unit entity
- `equipment.py`: equipment entity
- `skills.py`: skills entity
- `unit.py`: unit entity

