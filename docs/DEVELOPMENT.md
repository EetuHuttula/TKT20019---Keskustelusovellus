# Kehitysopas

## Kehitysympäristön asennus

Seuraa pääsovelluksen README.md:n asennusohjeita, mutta varmista että asennat myös kehitystyökalut:

```bash
poetry install  # Asentaa kaikki riippuvuudet
poetry shell    # Aktivoi virtual environmentin
```

## Koodin rakenteet

### Pyöritys paikallisesti

```bash
poetry run flask run
```

Sovellus on käytettävissä osoitteessa `http://localhost:5000`

### Debuggaus

Flask:n debug-moodissa olevat muutokset latautuvat automaattisesti. Voit käyttää pdb-debuggeria:

```python
import pdb; pdb.set_trace()
```

### Tietokannan palautus

Tyhjennä tietokanta ja luo uudelleen:

```bash
psql < schematic.sql
```

## Koodityyli

Noudata PEP 8 -standardia. Käytä:

```bash
pylint src/
```

Tarkista pylint-konfiguraatio tiedostosta `src/.pylintrc`

## Testit

Projektissa käytetään Robot Framework -testejä. Testit sijaitsevat `tests/`-kansiossa.

### Testien ajaminen

```bash
robot tests/
```

### Uuden testin luominen

1. Luo uusi `.robot`-tiedosto
2. Käytä seuraavaa pohjaa:

```robot
*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary

*** Test Cases ***
Esimerkki testi
    [Documentation]    Kuvaus testistä
    Log    Tämä on testi
```

## Tietokanta

### Uuden taulun lisääminen

1. Muokkaa `schematic.sql`-tiedostoa
2. Luo migraatioskripti tai tyhjennä tietokanta ja luo uudelleen:

```bash
psql < schematic.sql
```

### Tietokannan palautus

```bash
psql
\connect keskustelu  # tai sovelluksen tietokannan nimi
\dt  # Näytä taulut
\d users  # Näytä taulun rakenne
```

## Uuden ominaisuuden lisääminen

### Vaihe 1: Tietokannan muuttaminen

Päivitä `schematic.sql` tarvittavilla SQL-komennoilla.

### Vaihe 2: Backend-logiikka

1. Luo tai muokkaa tiedostoa sopivassa `src/`-alikansiossa
2. Kirjoita funktiot ja reititykset

Esimerkki uudelle reitille:

```python
from flask import redirect, request, session, url_for, flash
from sqlalchemy import text
from app import app
from db import db

@app.route("/new-feature", methods=["GET", "POST"])
def new_feature():
    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("Invalid CSRF token")
            return redirect(url_for("index"))
        
        # Logiikka tähän
        
        return redirect(url_for("index"))
    
    return render_template("new_feature.html")
```

### Vaihe 3: Frontend-malli

1. Luo HTML-sivu `templates/`-kansioon
2. Käytä Jinja2-syntaksia

Esimerkki:

```html
{% extends "components/navbar.html" %}

{% block content %}
<div class="container">
    <h1>Uusi ominaisuus</h1>
    <form method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
        <input type="text" name="title" placeholder="Otsikko" required>
        <button type="submit">Lähetä</button>
    </form>
</div>
{% endblock %}
```

### Vaihe 4: Testi

1. Luo robotista testi `tests/`:iin
2. Testaa manuaalisesti paikallisesti

## Projektin rakenne

```
src/
├── auth/          # Käyttäjien hallinta
├── threads/       # Viestiketjujen logiikka
├── polls/         # Kyselyiden logiikka
└── profile/       # Profiilin logiikka
```

Jokainen moduuli sisältää:
- Reitit (@app.route)
- Validointi
- Tietokannan operaatiot

## Bugien korjaaminen

1. Tunnista bugi ja sen sijainti
2. Kirjoita testi, joka toistaa bugin
3. Korjaa bugi
4. Varmista, että testi menee läpi
5. Tarkista, että muut testit menevät läpi


## Hyödyllisiä komentoja

```bash
# Poetry:lla
poetry add package_name          # Lisää paketti
poetry show                       # Näytä kaikki paketit
poetry lock                       # Lukitse versiot

# Flask
export FLASK_ENV=development     # Kehitysympäristö
flask shell                       # Flask Python REPL

# PostgreSQL
psql -l                          # Listaa kaikki tietokannat
psql -c "SELECT * FROM users"   # Aja komento

# Git
git status                       # Näytä muutokset
git diff                         # Näytä muutoksien sisältö
git log --oneline               # Näytä commit-historia
```

## Yleiset virheet

### ImportError: No module named 'X'
- Ratkasu: `poetry install`

### Connection refused to PostgreSQL
- Ratkasu: Varmista, että PostgreSQL palvelin on käynnissä
- Linux: `sudo systemctl start postgresql`
- macOS: `brew services start postgresql`

### CSRF token validation failed
- Ratkasu: Varmista, että lomakkeessa on `csrf_token`-kenttä

### Static files not loading
- Ratkasu: Tarkista, että `static/`-kansio on olemassa ja sisältää tiedostot

## Lisätietoa

- Flask dokumentaatio: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/docs/
