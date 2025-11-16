# FAQ - Usein kysytyt kysymykset

## Yleinen

### Miksi Porinanurkka on nimetty näin?
Nimi on Porista ja "nurkka" (kulmasta). Se viittaa paikalliseen keskustelukanavaan.

### Mikä on projektin kieli?
Sovellus on pääasiassa suomenkielinen, mutta koodi on englanninkielisesti dokumentoitu.

### Voiko sovellusta käyttää tuotannossa?
Ei vielä täysin. Se on kehitysvaiheessa ja sisältää potentiaalisia turvallisuusongelmia. Käytä vastuullisesti!

---

## Tekniikka

### Miksi Flask?
Flask on kevyt, joustava ja helppo oppia. Se soveltuu hyvin pieniin ja keskikokoisiin projekteihin.

### Miksi PostgreSQL eikä SQLite?
PostgreSQL on tehokkaampi ja suurempia sovelluksia varten ja tukee parempia ominaisuuksia kuten JSONB.

### Kuinka pitkään sovellus on ollut kehityksen alla?
Sovellus aloitettiin TKT20019-kurssin projektina ja kehitystä jatketaan aktiivisesti.

### Voiko sovellusta käyttää mobiillilla?
Kyllä, sovellus on responsive design:lla toteutettu ja toimii myös mobiililaitteilla.

---

## Käyttö

### Kuinka monta käyttäjää sovellus voi tukea?
Samat rajat kuin PostgreSQL-tietokantasi. Testaamme noin 100 samanaikaisen käyttäjän kanssa.

### Kuinka pitkiä viestiketjuja voin luoda?
Teoriassa rajoitaton, käytännössä riippuu palvelimestasi.

### Voinko minä poistaa oman käyttäjätilini?
Tämä ominaisuus ei ole vielä toteutettu. Voit ottaa yhteyttä järjestelmänvalvojaan pyynnöllä tilisi poistamiseksi.

### Kuinka usein sovellusta päivitetään?
Kehitys on aktiivista. Uusia ominaisuuksia lisätään säännöllisesti.

---

## Turvallisuus

### Onko salasanani turvallinen?
Kyllä, salasanat hajautetaan Werkzeug:in check_password_hash -funktiolla.

### Kuinka suojattu on sovellus CSRF-hyökkäyksiltä?
Kaikissa lomakkeissa käytetään CSRF-tokeneita. Sovellus on suojattu tyypillisiltä CSRF-hyökkäyksiltä.

### Mitä jos unohdan salasanani?
Tällä hetkellä salasanan vaihtotoimintoa ei ole. Ota yhteyttä järjestelmänvalvojaan.

### Onko sovellus SSL/TLS-suojattu?
Kehitysympäristössä ei. Tuotannossa käytä HTTPS-sertifikaattia (esim. Let's Encrypt).

---

## Tekninen tuki

### Kuinka voin raportoida bugin?
Avaa GitHub Issue yksityiskohtaisella kuvauksella ja toistamisen vaiheilla.

### Kuinka voin ehdottaa uutta ominaisuutta?
Avaa GitHub Issue "enhancement"-labelin kanssa.

### Kuinka voin kontribuoida?
Katso `docs/DEVELOPMENT.md` ja README.md kontribuointiohjeille.

### Mitä kieliä sovellus tukee?
Tällä hetkellä pääasiassa suomea. Kansainvälisen tuen lisääminen on tulevassa roadmap:ssa.

---

## Kehitys

### Kuinka lisään uuden ominaisuuden?
Katso `docs/DEVELOPMENT.md` -osio "Uuden ominaisuuden lisääminen".

### Mitä koodin tyyli on?
PEP 8 Pythonille. Käytä `pylint` -validointiin.

### Kuinka testaan sovellusta?
Käytä Robot Framework:ia. Testit ovat `tests/`-kansiossa.

### Kuinka debuggaan sovellusta?
Käytä Flask:n debug-moodia ja pdb-debuggeria.

---

## Muut kysymykset

### Kuka on kehittäjä?
Pääkehittäjä: Eetu Huttula (EetuHuttula)

### Kuinka voin ottaa yhteyttä kehittäjään?
GitHub Issues tai sähköpostitse: eetuhuttula99@gmail.com

### Mitä tarkoittaa "Modernisoidumpi UI" roadmapissa?
"Modernisoidumpi UI" tarkoittaa käyttöliittymän päivittämistä:
- Siirtyminen nykyaikaisempaan JavaScript-frameworkiin (esim. React tai Vue.js)
- Parempi visuaalinen design ja käyttökokemus
- Responsiivisempi layout
- Parempi mobiili-tuki
- Uudet komponentit ja animaatiot

Tällä hetkellä sovellus käyttää perinteistä HTML/CSS/Jinja2-pohjaa.

### Mikä on projektin roadmap?
- [ ] Email-vahvistus
- [ ] Käyttäjäkuvat
- [ ] Etsi/suodata ominaisuudet
- [ ] Modernisoidumpi UI (React/Vue, parempi design)
- [ ] Kansainvälisyys (i18n)
- [ ] Tehtävähallinta
- [ ] Notifikaatiot

---

Etkö löytänyt vastausta? Avaa GitHub Issue!
