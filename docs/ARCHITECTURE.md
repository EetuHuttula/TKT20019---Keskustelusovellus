# Porinanurkka - Arkkitehtuuri

## Yleiskatsaus

Porinanurkka on Flask-pohjainen web-sovellus, joka noudattaa MVC (Model-View-Controller) -arkkitehtuuria. Sovellus käyttää PostgreSQL-tietokantaa ja Flask-SQLAlchemy ORM:ää.

## Teknologia

- **Framework:** Flask 3.1.2
- **Tietokanta:** PostgreSQL
- **ORM:** SQLAlchemy 2.0.44
- **Kirjautuminen:** Werkzeug (salasanojen hajautus)
- **Frontend:** HTML5, CSS3, Jinja2-mallit

## Kansiorakenne

```
Porinanurkka/
├── app.py                 # Flask-sovelluksen alustus
├── db.py                  # Tietokannan yhteyden hallinta
├── requirements.txt       # Python-riippuvuudet
├── pyproject.toml         # Poetry-konfiguraatio
├── schematic.sql          # Tietokannan skriptit
│
├── src/                   # Pääsovelluksen koodi
│   ├── secrets_token.py   # CSRF-tokenin luonti
│   ├── auth/              # Kirjautumisen ja rekisteröinnin logiikka
│   │   ├── user_login.py
│   │   ├── user_register.py
│   │   └── validate_registeration.py
│   ├── threads/           # Viestiketjujen hallinta
│   │   ├── thread_create.py
│   │   ├── thread_view.py
│   │   ├── thread_reply.py
│   │   ├── thread_management.py (muokkaus/poistaminen)
│   │   └── thread_like.py
│   ├── polls/             # Kyselyiden hallinta
│   │   ├── polls_create.py
│   │   ├── polls_delete.py
│   │   └── polls_view_answer.py
│   └── profile/           # Käyttäjäprofiili
│       ├── profile_routes.py
│       └── profile_context.py
│
├── templates/             # Jinja2 HTML-mallit
│   ├── frontpage.html
│   ├── login.html
│   ├── register.html
│   ├── view_thread.html
│   ├── edit_thread.html
│   ├── poll.html
│   ├── polls.html
│   ├── profile.html
│   ├── result.html
│   └── components/        # Uudelleenkäytettävät komponentit
│       ├── navbar.html
│       ├── footer.html
│       ├── newthread.html
│       └── makepolls.html
│
├── static/                # Staattiset resurssit
│   ├── css/
│   │   ├── style.css
│   │   ├── form.css
│   │   ├── components.css
│   │   └── thread.css
│   └── uploads/           # Käyttäjien lataamat kuvat ja videot
│
└── tests/                 # Testitiedostot (Robot Framework)
```

## Tietokannan rakenne

### Päätaulut

- **users** - Käyttäjätiedot (id, username, password_hash, jne)
- **threads** - Viestiketjut (id, title, content, user_id, created_at, jne)
- **replies** - Vastaukset viestiketjuihin (id, thread_id, user_id, content, jne)
- **polls** - Kyselyt (id, title, user_id, created_at, jne)
- **poll_options** - Kyselyvaihtoehdot (id, poll_id, option_text, jne)
- **poll_answers** - Käyttäjien vastaukset (id, poll_option_id, user_id, jne)
- **likes** - Tykkäykset (id, thread_id, user_id, jne)

## Moduulit

### auth/ - Kirjautuminen ja rekisteröinti
Vastaa käyttäjien hallinnasta ja todentamisesta.

**Funktiot:**
- `login()` - Käyttäjän kirjautuminen
- `register()` - Uuden käyttäjän rekisteröinti
- `validate_password()` - Salasanan validointi

### threads/ - Viestiketjujen hallinta
Vastaa viestiketjujen CRUD-operaatioista.

**Funktiot:**
- `send()` - Uuden ketjun luominen
- `view_thread()` - Ketjun ja vastausten näyttäminen
- `reply()` - Vastauksen lisääminen
- `edit()` - Ketjun muokkaaminen
- `delete()` - Ketjun poistaminen
- `like()` - Ketjulle tykkääminen

### polls/ - Kyselyiden hallinta
Vastaa kyselyiden luomisesta, näyttämisestä ja vastausten keräämisestä.

**Funktiot:**
- `create_poll()` - Uuden kyselyn luominen
- `view_poll()` - Kyselyn ja vastausvaihtoehtojen näyttäminen
- `answer_poll()` - Vastauksen antaminen
- `delete_poll()` - Kyselyn poistaminen

### profile/ - Käyttäjäprofiili
Vastaa käyttäjäprofiilin tietojen näyttämisestä.

**Funktiot:**
- `profile()` - Profiilin näyttäminen

## Tiedon virta

### Viestiketjun luominen
1. Käyttäjä täyttää lomakkeen frontend-sovelluksessa
2. `thread_create.py:send()` vastaanottaa POST-pyynnön
3. Validoidaan käyttäjän syöte ja tiedosto (kuvat/videot)
4. Tieto tallennetaan tietokantaan
5. Ohjataan etusivulle

### Käyttäjän kirjautuminen
1. Käyttäjä lähettää tunnuksensa
2. `user_login.py:login()` tarkistaa tiedot
3. Vertaillaan salasanaa tietokannan hajautettuun salasanaan
4. Jos kelvollinen, luodaan sessio
5. Ohjataan etusivulle

## Turvallisuus

- **CSRF-suojaus:** Kaikissa lomakkeissa käytetään CSRF-tokeneita
- **Salasananhajautus:** Werkzeug:n check_password_hash
- **SQL-injektio suojaus:** SQLAlchemy parametrisoidut kyselyt
- **Istunnon hallinta:** Flask-sessiot

## Virheenkäsittely

- Kaikissa tietokantaoperaatioissa käytetään try-except -lohkoja
- SQLAlchemyError -virheet käsitellään asianmukaisesti
- Käyttäjälle näytetään flash-viestit virheistä

## Tulevat parannukset

- Tehtävähallintajärjestelmän lisääminen
- Email-vahvistus rekisteröinnille
- Käyttäjäkuvien profiilissa
- Etsiä/suodatusta viestiketjuille
- Modernisoidumpi frontend
