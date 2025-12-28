# Porinanurkka - Keskustelusovellus

"Porinanurkka" on moderni keskustelusovellus, jossa käyttäjät voivat rekisteröityä, kirjautua sisään ja osallistua eri viestiketjuihin. Sovellus mahdollistaa lankojen aloittamisen, lukemisen, vastaamisen ja muokkaamisen. Käyttäjät voivat myös tehdä ja vastata kyselyihin sekä tykätä langoista.

## 📋 Ominaisuudet

### Käyttäjien hallinta ja kirjautuminen
- Käyttäjä voi rekisteröityä ja luoda oman tunnuksen
- Käyttäjä voi kirjautua sisään omilla tunnuksillaan
- Kaikki toiminnot vaativat tunnistautumisen

### Etusivu
- Näyttää kaikki viestiketjut (langat), jotka eri käyttäjät ovat julkaisseet
- Langat lajiteltuina uusimpien mukaaan

### Viestiketjut (Langat)
- Käyttäjä voi lukea lankoja ja vastata niihin
- Käyttäjä voi aloittaa uuden langan ja kirjoittaa aloitusviestin
- Käyttäjä voi muokata tai poistaa omaa lankaansa
- Käyttäjät voivat tykätä langoista (vain kerran per langa)

### Kyselyt (Polls)
- Rekisteröitynyt käyttäjä voi luoda uusia kyselyitä
- Käyttäjät voivat vastata kyselyihin ja nähdä tulokset
- Ainoastaan rekisteröityneet käyttäjät voivat osallistua

### Käyttäjäprofiili
- Käyttäjät voivat nähdä profiilin tiedot
- Mahdollisuus muokata profiilia

## 🚀 Käyttöönotto

### Vaatimukset
- Python 3.8+
- PostgreSQL
- Poetry
- Flask

### Asennus ja käynnistys

#### 1. Poetry asentaminen

Jos sinulla ei ole Poetry-työvälinettä asennettu, asenna se:

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Tai käyttäjellä Homebrew (macOS):

```shell
brew install poetry
```

#### 2. Ympäristömuuttujien asetus

Luo `.env`-tiedosto sovelluksen juurikansioon:

```shell
touch .env
```

Lisää tiedostoon seuraavat ympäristömuuttujat:

```env
DATABASE_URL="postgresql:///käyttäjänimi"
SECRET_KEY="salainenavaimen"
```

#### 3. Riippuvuuksien asentaminen Poetry:llä

```shell
poetry install
```

Tämä luo virtuaalisen ympäristön ja asentaa kaikki vaaditut pakettien `pyproject.toml`-tiedostosta.

#### 4. Tietokannan alustaminen

Varmista, että PostgreSQL-palvelin on käynnissä. Luo tietokanta ja aja migraatio:

```shell
psql < schematic.sql
```

**Huom:** Jos komento ei toimi, voit kopioida `schematic.sql`-taulut ja laittaa ne manuaalisesti PostgreSQL-terminaalin kautta.

#### 5. Sovelluksen käynnistäminen

```shell
poetry run flask run
```

Sovellus on nyt käytettävissä osoitteessa `http://localhost:5000`

---

## 📦 Poetry käyttäminen

### Uuden paketin lisääminen

```shell
poetry add paketinnimi
```

### Kehitysriippuvuuksien lisääminen

```shell
poetry add --group dev paketinnimi
```

### Virtual ympäristöön aktivoiminen

```shell
poetry shell
```

Nyt voit ajaa komentoja ilman `poetry run` etuliitettä.

---

## 📁 Projektin rakenne

```
├── app.py                    # Flask pääsovellus
├── db.py                     # Tietokantayhteyden hallinta
├── requirements.txt          # Python-riippuvuudet
├── schematic.sql             # Tietokannan rakenne
├── src/                      # Pääkoodi
│   ├── auth/                 # Kirjautuminen ja rekisteröinti
│   ├── threads/              # Viestiketjujen hallinta
│   ├── polls/                # Kyselyiden hallinta
│   └── profile/              # Käyttäjäprofiili
├── templates/                # HTML-mallit
├── static/                   # CSS ja muut staattisethiedostot
└── tests/                    # Testitiedostot
```

---

## 📝 Tietoa projektista

Tämä projekti aloitettiin TKT20019-kurssin osana, mutta kehitystä jatketaan aktiivisesti henkilökohtaisena projektina.

---


**Kiitos osallistumisesta Porinanurkka-projektiin! 🎉**






 
