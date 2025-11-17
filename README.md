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

## 🤝 Osallistuminen ja Kontribuointi

Toivotamme kaikkien osallistuvan projektin kehittämiseen! Seuraavassa on ohjeet, miten voit kontribuoida.

### Koodin kontribuoiminen

1. **Forkkaa repositorio**
   - Klikkaa "Fork"-nappia GitHubissa

2. **Kloonaa omasi versio**
   ```shell
   git clone https://github.com/SINUN_KÄYTTÄJÄNIMI/TKT20019---Keskustelusovellus.git
   cd TKT20019---Keskustelusovellus
   ```

3. **Luo feature-branch**
   ```shell
   git checkout -b feature/uuden-ominaisuuden-nimi
   ```

4. **Tee muutokset ja testaa**
   - Varmista, että koodi noudattaa projektissa käytettyjä käytäntöjä
   - Testaa muutokset paikallisesti

5. **Committoi muutokset**
   ```shell
   git add .
   git commit -m "Kuvaava viesti: mitä muutit ja miksi"
   ```

6. **Pushaa branch GitHubiin**
   ```shell
   git push origin feature/uuden-ominaisuuden-nimi
   ```

7. **Avaa Pull Request**
   - Mene GitHubiin ja luo Pull Request
   - Kirjoita selkeä kuvaus muutoksistasi

### Kontribuoimisen ohjeet

- **Koodityyli:** Noudattaa PEP 8 -standardia Pythonissa
- **Viestien selkeys:** Committiviestejen tulee olla selkeät ja kuvaavat
- **Testaaminen:** Varmista, että uudet ominaisuudet on testattu
- **Dokumentaatio:** Päivitä dokumentaatio tarvittaessa

### Bugien ilmoittaminen

Löysitkö bugin? 
1. Tarkista, ettei bugia ole jo ilmoitettu Issues-osiossa
2. Avaa uusi Issue seuraavalla informaatiolla:
   - Selkeä otsikko
   - Yksityiskohtainen kuvaus ongelmasta
   - Vaiheet, joilla ongelma toistuu
   - Odotettavissa oleva ja todellinen käyttäytyminen

### Parannusehdotukset

Onko sinulla ideaa sovelluksen parantamiseksi?
- Avaa GitHub Issue "enhancement"-labelin kanssa
- Kuvaile ominaisuus yksityiskohtaisesti
- Selitä, miksi se olisi hyödyllinen

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

## ❓ Apua ja tuki

- Katso projektiin liittyviä dokumenteja
- Avaa GitHub Issue kysymyksiä varten

---

**Kiitos osallistumisesta Porinanurkka-projektiin! 🎉**






 
