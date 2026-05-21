# Projektisuunnitelma: Tunnetilan tunnistus kuvista

## Aihe ja tavoite

Projektin aiheena on ihmisten tunnetilojen tunnistus kasvokuvista. Tavoitteena on kouluttaa kuvien luokittelumalli, joka tunnistaa kasvojen ilmeistä useita tunnetiloja, kuten ilon, surun, vihan, pelon, yllätyksen ja neutraalin ilmeen. Lisäksi vertaillaan yksinkertaista omaa CNN-mallia ja siirto-oppimiseen perustuvaa mallia.

## Datasetti

Projektissa käytetään ensisijaisesti FER-2013-datasettiä. Se sopii hyvin kurssiprojektiin, koska se on tunnettu tunnetilaluokittelun vertailudatasetti, sisältää valmiit tunnetilaluokat ja mahdollistaa tulosten vertailun kirjallisuudessa nähtyihin suuntiin. Jos tarvitaan kevyempi kokeilu, datasetistä voidaan käyttää ensin osajoukkoa nopeaan prototypointiin.

## Suunniteltu lähestymistapa

Toteutetaan vähintään kaksi mallia:

1. baseline-CNN, joka koulutetaan alusta asti
2. siirto-oppimismalli, esimerkiksi MobileNetV2 tai EfficientNetB0

Lisäksi kokeillaan data-augmentaatiota ja mahdollisesti hienosäätöä vapauttamalla osa esikoulutetun mallin viimeisistä kerroksista. Mallien vertailussa käytetään ainakin accuracya, luokkakohtaista precision/recall/F1-arviointia sekä confusion matrixia.

## Työn toteutus

Projekti toteutettiin yksilötyönä. Työ eteni vaiheittain siten, että ensin valmisteltiin datasetti ja baseline-malli, sen jälkeen koulutettiin siirto-oppimismallit ja lopuksi tehtiin arviointi, visualisoinnit, raportti ja esitysmateriaalit.

## Riskit ja varasuunnitelma

Suurimmat riskit liittyvät datasetin kokoon, luokkien epätasapainoon ja siihen, että jotkin tunnetilat ovat vaikeasti erotettavia. Jos koulutus on raskasta tai tulokset jäävät heikoiksi, projekti voidaan pitää realistisena vertailemalla baselinea ja yhtä vahvaa siirto-oppimismallia sekä keskittymällä virheanalyysiin ja eettiseen pohdintaan.
