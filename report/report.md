# Raportti

## Projektin tavoite ja motivaatio

Tämän projektin tavoitteena oli rakentaa neuroverkkoon perustuva tunnetilaluokittelija, joka tunnistaa ihmisten kasvojen ilmeistä perustunnetiloja kuvien perusteella. Aihe valittiin, koska se yhdistää kurssilla opittuja keskeisiä teemoja: konvoluutioneuroverkot, siirto-oppiminen, mallien vertailu, data-augmentaatio ja tulosten kriittinen analyysi.

Tunnetilan tunnistus on kiinnostava ongelma myös käytännön kannalta, koska sitä voidaan soveltaa esimerkiksi ihmisen ja tietokoneen vuorovaikutuksessa, opetusteknologiassa ja hyvinvointisovelluksissa. Samalla se on teknisesti haastava tehtävä, sillä ilmeet voivat olla hienovaraisia, kuvien laatu voi vaihdella paljon ja eri tunnetilat voivat muistuttaa toisiaan.

Projektin konkreettisena tavoitteena oli verrata kolmea lähestymistapaa samaan FER-2013-datasettiin:

1. alusta asti koulutettu baseline-CNN
2. MobileNetV2 feature extraction -malli
3. MobileNetV2 fine-tuned -malli

Tavoitteena ei ollut vain saada mahdollisimman korkea tarkkuus, vaan ymmärtää, miten eri malliratkaisut käyttäytyvät haastavassa tunnetilaluokittelutehtävässä.

## Datasetti ja esikäsittely

Projektissa käytettiin FER-2013-datasettiä, joka on tunnettu kasvojen tunnetilaluokittelun vertailudatasetti. Datasetti sisältää seitsemän tunnetilaluokkaa:

- angry
- disgust
- fear
- happy
- neutral
- sad
- surprise

Data järjestettiin projektia varten hakemistorakenteeseen:

```text
dataset/raw/train/<class_name>/*.jpg
dataset/raw/val/<class_name>/*.jpg
dataset/raw/test/<class_name>/*.jpg
```

Lopulliset kuvamäärät olivat:

- train: 21006 kuvaa
- val: 4303 kuvaa
- test: 7178 kuvaa

Luokkajakauma ei ollut tasainen. Erityisesti `disgust`-luokassa oli selvästi vähemmän kuvia kuin muissa luokissa. Tämä on tärkeä huomio, koska epätasapaino voi heikentää mallin kykyä oppia harvinaisempia luokkia luotettavasti.

Luokkakohtaiset määrät olivat:

- train: angry 3396, disgust 371, fear 3483, happy 6133, neutral 4221, sad 4106, surprise 2696
- val: angry 599, disgust 65, fear 614, happy 1082, neutral 744, sad 724, surprise 475
- test: angry 958, disgust 111, fear 1024, happy 1774, neutral 1233, sad 1247, surprise 831

Esikäsittelyssä kuvat ladattiin TensorFlow-datasetteinä kokoon `96 x 96`. Kuvat normalisoitiin välille `0-1` `Rescaling`-kerroksella. Harjoitusdatassa käytettiin myös data-augmentaatiota, jotta malli näkisi monipuolisempia variaatioita samoista ilmeistä. Käytetyt augmentaatiot olivat:

- vaakasuuntainen peilaus
- pieni rotaatio
- zoom
- kontrastin satunnaisvaihtelu
- pieni siirto x- ja y-suunnassa

Augmentaatiota käytettiin vain harjoitusdatalle, ei validointi- tai testidatalle, mikä vastaa hyvää koneoppimiskäytäntöä.

## Mallit

Projektissa verrattiin kolmea mallia.

### Baseline-CNN

Ensimmäinen malli oli alusta asti koulutettu oma konvoluutioneuroverkko. Se sisälsi useita `Conv2D`- ja `MaxPooling2D`-kerroksia, joiden jälkeen käytettiin `GlobalAveragePooling2D`-kerrosta, dropoutia ja dense-luokittelijaa. Tämän mallin tarkoitus oli toimia vertailutasona ilman esikoulutettua runkoa.

### MobileNetV2 feature extraction

Toinen malli perustui esikoulutettuun MobileNetV2-verkkoon. Tässä versiossa MobileNetV2:n runko pidettiin jäädytettynä, ja vain sen päälle lisätty luokittelupää koulutettiin FER-2013-datalla. Tämän lähestymistavan ideana oli hyödyntää valmiiksi opittuja kuvapiirteitä ilman koko verkon uudelleenkoulutusta.

### MobileNetV2 fine-tuning

Kolmas malli oli muuten samaan MobileNetV2-runkoon perustuva, mutta sen viimeisiä kerroksia vapautettiin koulutettavaksi. Näin malli pystyi mukauttamaan esikoulutettuja piirteitä paremmin juuri tunnetilaluokittelun tarpeisiin. Tässä projektissa fine-tuning osoittautui hyödylliseksi, koska pelkkä feature extraction ei tuottanut yhtä hyvää tulosta.

## Koulutusprosessi

Projektin koulutus toteutettiin notebookissa, jotta ajot olivat helposti toistettavissa ja dokumentoitavissa. Koulutuksessa käytettiin seuraavia perusasetuksia:

- kuvan koko: `96 x 96`
- batch size: `32`
- loss-funktio: `categorical_crossentropy`
- optimointialgoritmi: `Adam`
- metriikka: `accuracy`

Mallikohtaiset asetukset olivat:

- baseline-CNN: learning rate `1e-3`, enintään `20` epochia
- feature extraction: learning rate `1e-3`, enintään `15` epochia
- fine-tuning: learning rate `1e-4`, enintään `15` epochia

Koulutuksessa käytettiin seuraavia callbackeja:

- `EarlyStopping`, jotta koulutus pysähtyy jos validointihäviö ei enää parane
- `ModelCheckpoint`, jotta paras malli tallentuu tiedostoon
- `ReduceLROnPlateau`, jotta oppimisnopeutta pienennetään automaattisesti, jos validointihäviö jämähtää

Notebookissa koulutettiin kaikki kolme mallia:

- baseline-CNN omana lähtötasona
- MobileNetV2 feature extraction -malli siirto-oppimisen kevyenä versiona
- MobileNetV2 fine-tuned -malli siirto-oppimisen jatkokehityksenä

Koulutusajat olivat käytännössä melko pitkiä, koska FER-2013 sisältää suuren määrän pieniä kasvokuvia ja jokainen malli ajettiin usean epookin ajan. Koulutuksen etenemistä seurattiin sekä validointihäviön että validointitarkkuuden avulla.

## Tulokset

Projektissa verrattiin kolmea eri malliasetelmaa:

1. baseline-CNN
2. MobileNetV2 feature extraction
3. MobileNetV2 fine-tuning

Notebook-ajon perusteella testitarkkuudet olivat seuraavat:

| Malli | Kuvaus | Test accuracy |
| --- | --- | ---: |
| Baseline-CNN | Alusta asti koulutettu oma konvoluutioneuroverkko | 0.5659 |
| MobileNetV2 feature extraction | Esikoulutettu runko jäädytettynä, vain luokittelupää koulutettiin | 0.4451 |
| MobileNetV2 fine-tuning | Esikoulutettu runko, jonka viimeisiä kerroksia vapautettiin koulutukseen | 0.5663 |

Tuloksista voidaan tehdä muutama keskeinen havainto. Ensinnäkin baseline-CNN toimi yllättävän hyvin ja saavutti noin 56.6 % testitarkkuuden. Toiseksi pelkkä feature extraction -lähestymistapa jäi selvästi heikommaksi noin 44.5 % tarkkuudella. Kolmanneksi fine-tuning nosti MobileNetV2-mallin suorituskyvyn takaisin baseline-mallin tasolle ja hieman sen yli.

Tämä on projektin kannalta kiinnostava tulos, koska siirto-oppiminen ei ollut automaattisesti paras ratkaisu ilman hienosäätöä. Vaikka esikoulutettu malli toi vahvan alkuperäisen piirreavaruuden, FER-2013-datasetin erityispiirteet näyttävät vaativan ainakin osittaista hienosäätöä, jotta malli pystyy mukautumaan tunnetilaluokitteluun riittävän hyvin.

Tulosten perusteella paras malli oli niukasti MobileNetV2:n fine-tuned versio, mutta ero baseline-CNN:ään oli hyvin pieni. Tämä tarkoittaa, että projektissa ei saatu vain yksinkertaista tulosta, jossa suurempi malli voittaa automaattisesti, vaan mallien välille syntyi oikeasti analysoitava ero. Juuri tällainen vertailu on loppuprojektin kannalta arvokas.

Raporttiin kannattaa liittää notebookista seuraavat visualisoinnit:

- baseline-CNN:n accuracy- ja loss-käyrät
- feature extraction -mallin accuracy- ja loss-käyrät
- fine-tuned mallin accuracy- ja loss-käyrät
- confusion matrix ainakin parhaalle mallille
- luokitteluraportit, jotta luokkakohtaiset erot näkyvät tarkemmin

Erityisen mielenkiintoinen jatkoanalyysin kohde on se, mitkä tunnetilat menivät useimmin sekaisin. FER-2013 on haastava datasetti, jossa ilmeet ovat pieniä, osin epäselviä ja luokkien väliset erot voivat olla hienovaraisia. Siksi noin 56 % tarkkuus ei ole oppimisprojektissa heikko tulos, vaan pikemminkin realistinen osoitus ongelman vaikeudesta.

## Virheanalyysi

Virheanalyysin perusteella vaikeimmat luokat olivat odotetusti sellaisia, joiden ilmeet ovat lähellä toisiaan tai joita datassa oli vähän. Erityisesti `disgust` osoittautui hankalaksi lähes kaikille malleille. Baseline-CNN ei tunnistanut sitä käytännössä lainkaan, sillä `disgust`-luokan recall jäi arvoon `0.00`. Feature extraction -malli ylsi vain recalliin `0.03`. Fine-tuning paransi tätä selvästi recalliin `0.17`, mutta luokka jäi edelleen projektin vaikeimmaksi.

Myös `fear` oli vaikea luokka. Baseline-CNN:n recall oli `0.13`, feature extraction -mallin `0.16` ja fine-tuned mallin `0.28`. Tämä viittaa siihen, että pelko sekoittui usein muihin ilmeisiin, todennäköisesti erityisesti `surprise`-luokkaan, koska niiden kasvonpiirteissä on osittaista samankaltaisuutta.

Parhaiten tunnistettavia luokkia olivat `happy` ja `surprise`. Baseline-CNN saavutti `happy`-luokassa precisionin ja recallin `0.81`, ja fine-tuned malli pääsi `happy`-luokan recallissa myös arvoon `0.81`. `Surprise` tunnistui myös melko hyvin kaikissa onnistuneimmissa malleissa: baseline-CNN:n recall oli `0.79` ja fine-tuned mallin `0.78`. Tämä on loogista, koska sekä iloinen että yllättynyt ilme ovat usein kuvissa visuaalisesti erottuvampia kuin esimerkiksi neutraalin, surullisen ja pelokkaan ilmeen väliset erot.

`Neutral` ja `sad` sijoittuivat vaikeudeltaan keskialueelle. Niiden tulokset olivat kohtalaisia, mutta eivät vahvoja. Fine-tuned malli saavutti `neutral`-luokassa precisionin ja recallin `0.52`, ja `sad`-luokassa precisionin `0.46` ja recallin `0.42`. Tämä viittaa siihen, että malli oppi osan olennaisista eroista, mutta ei pystynyt erottamaan kaikkia rajatapauksia luotettavasti.

Mallien välisessä vertailussa virheanalyysi tukee samoja johtopäätöksiä kuin kokonaisaccuracy:

- baseline-CNN oli yllättävän tasapainoinen vahvimmissa luokissa
- pelkkä feature extraction jäi useissa luokissa selvästi heikommaksi
- fine-tuning paransi erityisesti vaikeita ja harvinaisempia luokkia, kuten `disgust` ja `fear`

Tämä on tärkeä havainto, koska se osoittaa, että fine-tuning ei vain nostanut kokonaisaccuracyä hieman, vaan toi myös laadullista parannusta juuri niihin luokkiin, joissa ongelma oli vaikein. Silti mallin suorituskyky jäi selvästi alle täydellisen, mikä on täysin odotettavaa näin haastavassa tunnetilaluokittelutehtävässä.

## Eettiset näkökohdat

Tunnetilan tunnistukseen liittyy merkittäviä eettisiä kysymyksiä. Ensinnäkin kasvojen ilme ei aina vastaa ihmisen todellista tunnetilaa. Ihminen voi peittää tunteitaan, ilmaista niitä eri tavalla tai olla tilanteessa, jossa hetkellinen ilme ei kerro sisäisestä kokemuksesta juuri mitään.

Toiseksi ilmeiden tulkintaan liittyy kulttuurisia ja yksilöllisiä eroja. Malli voi oppia tietyn datasetin mukaisia ilmaisuja, mutta ei välttämättä yleisty tasapuolisesti kaikkiin ihmisiin. Tämä voi aiheuttaa vinoumia ja epäoikeudenmukaisia tulkintoja.

Kolmanneksi tunnetilan tunnistusta voidaan käyttää ongelmallisissa yhteyksissä, kuten valvonnassa, profiloinnissa tai ihmisten automaattisessa arvioinnissa ilman heidän suostumustaan. Siksi tällaisen teknologian kohdalla on tärkeää ymmärtää, että hyväkään luokittelutarkkuus ei tee mallista eettisesti neutraalia.

Tässä projektissa tunnetilan tunnistus nähdään ennen kaikkea oppimisprojektina, jonka avulla tutkitaan neuroverkkojen toimintaa haastavassa luokittelutehtävässä. Mahdolliset käytännön sovellukset pitää aina arvioida erikseen sekä teknisestä että eettisestä näkökulmasta.

## Johtopäätökset

Projektin paras malli oli MobileNetV2:n fine-tuned versio, joka saavutti testitarkkuuden `0.5663`. Ero baseline-CNN:ään oli kuitenkin hyvin pieni, sillä baseline saavutti lähes saman tuloksen (`0.5659`). Pelkkä MobileNetV2 feature extraction jäi selvästi heikommaksi (`0.4451`).

Projektin tärkeimmät opit olivat:

- siirto-oppiminen ei automaattisesti paranna tulosta, jos esikoulutettua mallia ei mukauteta tehtävään riittävästi
- fine-tuning voi olla tarpeellinen askel, kun tehtävä poikkeaa esikoulutetun mallin alkuperäisestä käyttökontekstista
- yksinkertainenkin baseline-malli voi toimia yllättävän kilpailukykyisesti
- luokkaepätasapaino ja vaikeat rajatapaukset vaikuttavat merkittävästi tunnetilaluokitteluun

Mahdollisia jatkokehitysideoita ovat:

- luokkapainojen käyttö harvinaisten luokkien, erityisesti `disgust`-luokan, tukemiseksi
- toisen siirto-oppimismallin, kuten EfficientNetB0:n, vertailu
- tarkempi virheanalyysi väärin luokitelluista esimerkeistä
- hyperparametrien systemaattinen viritys
- yksinkertainen ensemble kahden parhaan mallin välillä

Kokonaisuutena projekti osoitti hyvin, miten eri neuroverkkoratkaisuja voidaan soveltaa samaan ongelmaan, vertailla keskenään ja analysoida kriittisesti.

## Tekoälyn käyttö

Tässä projektissa tekoälyä käytettiin tukityökaluna projektin suunnittelussa, koodirungon ideoinnissa, dokumentaation rakentamisessa ja raportin jäsentelyssä. Tekoäly auttoi erityisesti seuraavissa asioissa:

- projektirungon suunnittelu
- tiedostorakenteen ja notebook-pohjan luonnostelu
- raporttipohjan laatiminen
- tulosten sanallinen tulkinta

Kaikki ratkaisut käytiin kuitenkin läpi ja niitä muokattiin projektin tarpeisiin sopiviksi. Datasetin rakenne, mallien ajaminen, tulosten tarkastelu ja lopullinen raportointi perustuivat projektissa itse tehtyihin valintoihin ja toteutuneisiin ajoihin.

Tekoälyn käyttö dokumentoidaan avoimesti, koska kurssin tehtävänannon mukaan olennaista ei ole vain käyttää apuvälineitä, vaan ymmärtää, mitä koodi tekee ja pystyä selittämään ratkaisut itse. Siksi projektissa käytetyt mallit, hyperparametrit ja analyysit perustuvat toteutuksen aikana tehtyihin päätöksiin, eivät sokeasti kopioituun sisältöön.

## Palautuschecklist

Varmista ennen palautusta:

- notebook on ajettu loppuun asti
- notebookista on tehty `.html`-versio
- datasetin lähde tai linkki on mukana
- mallien ajamiseen on selkeät ohjeet
- raportissa on sekä tekninen analyysi että eettinen pohdinta
