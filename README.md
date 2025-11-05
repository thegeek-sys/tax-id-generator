# Tax ID generator
Italian Tax code generator in Flask using ajax to complete the "Comune" section based on "Province" selection (data stored in PostgreSQL databse)

<img width="711" height="362" alt="demo" src="https://github.com/user-attachments/assets/0f444f6a-8e8c-4d6e-9c70-ab848931a342" />

## Files
- `static`: directory for static files (JS and styling)
- `templates`: directory used to store `.html` page
- `Procfile`: specifies the commands executed by Heroku
- `app.py`: core file of the web application
- `comuni.csv`: list of all the Italian districts used to setup my PostgreSQL database
- `import.py`: Python program that parses `comuni.csv` and import it to my database

## Requirements
Install the required libraries via `pip` by using
```bash
pip install -r requirements.txt
```

## Usage
Run the app via `flask`
```bash
flask --app app run
```
