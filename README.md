# Guess_Who

My mini akinator project built using Python and MySQL.

## Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure MySQL is installed and running** on your machine.

3. **Configure your database credentials**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and set `DB_PASSWORD` (and `DB_USER`/`DB_HOST` if different
   from the defaults) to your own MySQL login. `.env` is git-ignored, so your
   password never gets committed.

   No database needs to be created manually — the app creates it
   automatically on first run if it doesn't already exist.

## Run

```bash
python main_file.py
```

Or use the interactive menu (play, add people, view database, reset):

```bash
python main_file.py --menu
```

## Notes

- Credentials are read from environment variables (via `.env`), never
  hardcoded in source.
- Sample data is loaded automatically the first time you run the game if
  the database is empty.
