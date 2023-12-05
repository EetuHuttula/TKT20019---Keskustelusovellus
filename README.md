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

kyselyt: 
kukavain voi lisätä, vastata ja katsoa kyselyjä

**OHJEET KÄYTÖÖN:**

Avaa komentokehote tai terminaali.
Siirry sovelluksen juurikansioon.
Suorita pip install -r requirements.txt asentaaksesi tarvittavat Python-paketit.

Määritä tietokanta:
Varmista, että PostgreSQL-tietokantapalvelin on asennettu ja käynnissä.
Luo tietokanta ja käyttäjä sovellusta varten. (taulut löydät schematic.sql filestä)
aja komento psql < schematic.sql

Määritä ympäristömuuttujat:
Luo .env-tiedosto sovelluksen juurikansioon ja määritä tarvittavat ympäristömuuttujat, kuten tietokantayhteys ja salainen avain.

DATABASE_URL=(database linkitys)
SECRET_KEY=(oma secret key)

käynnistä sovellus komennolla flask run

**VÄLIPALAUTUS (3.12.2023)** 

Valmiit asiat:
-käyttäjä voi rekisteröityä ja kirjautua sisään omilla tunnuksillaan.
-lankojen aloittaminen ja niihin vastaaminen.
-käyttäjä voi muuttaa tai poistaa omaa lankaa.
-käyttäjä voi tehdä kyselyn, johon voi vastata kukavain.

Tällä hetkellä sivustolla on enään jäljellä ulkoasun muokkaus.
Päätin poistaa admin mahdollisuudet sivustolla sillä se ei luo lisä arvoa mielestäni projektille,
eikä minulla ole tarpeeksi aikaa enään tehdä sellaista ominaisuutta. 
Jätän kuitenkin databaseen ja kirjautumis/register functiolle alun tämän toteuttamiseen, siltä varalta
että palaan tekemään sen joskus.







 
