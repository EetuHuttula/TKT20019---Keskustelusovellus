# TKT20019---Keskustelusovellus

"Porinanurkka" on keskustelusovellus, jossa käyttäjät voivat rekisteröityä, kirjautua sisään ja osallistua eri viestiketjuihin. Sovellus mahdollistaa lankojen aloittamisen, lukemisen, vastaamisen ja muokkaamisen. Anonyymiä aloittamista ei sallita. Käyttäjät voivat myös tehdä ja vastata kyselyihin. Lopullisessa palautuksessa on lisäksi toiminnallisuuksia kuten tykkääminen langoista ja käyttäjäprofiilin tietojen näyttäminen.

Toiminnallisuus:

Käyttäjien hallinta ja kirjautuminen:
   - Käyttäjä voi rekisteröityä ja luoda oman tunnuksen.
   - Käyttäjä voi kirjautua sisään omilla tunnuksillaan.

Etusivu:
   - Näyttää kaikki viestiketjut (langat), jotka eri käyttäjät ovat julkaisseet.

Langat:
   - Käyttäjä voi lukea lankoja ja vastata niihin.
   - Käyttäjä voi aloittaa uuden langan ja kirjoittaa aloitusviestin.
   - Käyttäjä voi muokata oman langan aloitusviestiään.

Anonyymit langan aloitukset:
   - Lankoja ei voi aloittaa anonyyminä, vaan käyttäjän tulee luoda tunnus.

kyselyt: 
   - Käyttäjä tulee luoda tunnus ja olla kirjautuneena sisään jos haluaa luoda kyselyn.

**Lopullinen palautus (17.12.2023)** 

**Valmiit asiat**
   - käyttäjä voi rekisteröityä ja kirjautua sisään omilla tunnuksillaan.
   - lankojen aloittaminen ja niihin vastaaminen.
   - käyttäjä voi muuttaa tai poistaa oma lanka.
   - käyttäjä voi tykätä langoista, mutta ainoastaan kerran.
   - käyttäjä voi tehdä kyselyn.
   - Ainoastaan rekisteöitynyt käyttäjä voi vastata kyselyihin.
   - Käyttäjä näkee omasta profiilista tietoa.


**OHJEET KÄYTÖÖN:**

Sovellusta ei saa fly.iosta

Määritä ympäristömuuttujat:
   - Luo .env-tiedosto sovelluksen juurikansioon
   - ja määritä tarvittavat ympäristömuuttujat, kuten tietokantayhteys ja salainen avain.
```shell
DATABASE_URL="postgresql:///user"
SECRET_KEY=""
```

Avaa terminaali ja suorita seuraavat komennot.

```shell 
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
 ```

Määritä tietokanta:
   - Varmista, että PostgreSQL-tietokantapalvelin on asennettu ja käynnissä.
   - Luo tietokanta sovellusta varten.

aja komento:  
```shell 
psql < schematic.sql 
``` 
Jos tämä ei toimi voit kopioida schematic.sql taulut ja manuaalisesti laittaa ne psql terminaalin kautta haluamaasi tietokantaan.

käynnistä sovellus komennolla 
```shell
flask run
```






 
