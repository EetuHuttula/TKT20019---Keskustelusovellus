# TKT20019---Keskustelusovellus

Porinanurkka - Keskustelusovellus

Toiminnallisuus:

Käyttäjien hallinta ja kirjautuminen:
Käyttäjä voi rekisteröityä ja luoda oman tunnuksen.
Käyttäjä voi kirjautua sisään omilla tunnuksillaan.

Etusivu:
Näyttää kaikki viestiketjut (langat), jotka eri käyttäjät ovat julkaisseet.

Langat:
Käyttäjä voi lukea lankoja ja vastata niihin.
Käyttäjä voi aloittaa uuden langan ja kirjoittaa aloitusviestin.
Käyttäjä voi muokata oman langan aloitusviestiään.

Ylläpitäjän toiminnot:
Ylläpitäjä voi lisätä uusia lankoja.
Ylläpitäjä voi poistaa lankoja tarvittaessa.

Anonyymit langan aloitukset:
Lankoja ei voi aloittaa anonyyminä, vaan käyttäjän tulee luoda tunnus.

VÄLIPALAUTUS (19.11.2023) 
Valmiit asiat:

Rekisteröityminen ja kirjautuminen: 
Käyttäjät voivat rekisteröityä ja luoda tunnuksen sekä kirjautua sisään omilla tunnuksillaan.

Lankojen aloittaminen ja niihin vastaaminen:
Käyttäjät voivat aloittaa uusia lankoja, lukea olemassa olevia ja vastata niihin.

OHJEET KÄYTÖÖN:

Avaa komentokehote tai terminaali.
Siirry sovelluksen juurikansioon.
Suorita pip install -r requirements.txt asentaaksesi tarvittavat Python-paketit.

Määritä tietokanta:
Varmista, että PostgreSQL-tietokantapalvelin on asennettu ja käynnissä.
Luo tietokanta ja käyttäjä sovellusta varten. (taulut löydät schematic.sql filestä)

Määritä ympäristömuuttujat:
Luo .env-tiedosto sovelluksen juurikansioon ja määritä tarvittavat ympäristömuuttujat, kuten tietokantayhteys ja salainen avain.

DATABASE_URL=(database linkitys)
SECRET_KEY=(oma secret key)

käynnistä sovellus komennolla flask run







 
