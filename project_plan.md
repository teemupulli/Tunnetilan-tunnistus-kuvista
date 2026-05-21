# Projektisuunnitelma: Tunnetilan tunnistus kuvista

## Aihe ja tavoite

Projektin aiheena on ihmisten tunnetilojen tunnistus kasvokuvista. Tavoitteena on kouluttaa kuvien luokittelumalli, joka tunnistaa kasvojen ilmeistä useita tunnetiloja, kuten ilon, surun, vihan, pelon, yllätyksen ja neutraalin ilmeen. Mallien vertailussa käytetään sekä itse rakennettua CNN-mallia että MobileNetV2-pohjaista siirto-oppimista.

## Datasetti

Projektissa käytetään FER-2013-datasettiä. Se sopii aiheeseen hyvin, koska se on tunnettu tunnetilaluokittelun vertailudatasetti ja sisältää valmiit tunnetilaluokat. Alkuvaiheen koeajoissa voidaan käyttää pienempää osajoukkoa, jotta datan lataus, mallit ja arviointi saadaan nopeasti toimimaan.

## Suunniteltu lähestymistapa

Toteutetaan kolme malliasetelmaa:

1. baseline-CNN, joka koulutetaan alusta asti
2. MobileNetV2 feature extraction, jossa esikoulutettu runko pidetään jäädytettynä
3. MobileNetV2 fine-tuning, jossa viimeisiä kerroksia vapautetaan koulutettavaksi

Harjoitusdatassa käytetään data-augmentaatiota. Mallien vertailussa tarkastellaan accuracya, luokkakohtaista precision/recall/F1-arviointia sekä confusion matrixia.

## Työn toteutus

Projekti tehdään yksilötyönä. Työ jakautuu kolmeen päävaiheeseen: ensin valmistellaan datasetti ja baseline-malli, sen jälkeen koulutetaan siirto-oppimismallit ja lopuksi tehdään arviointi, visualisoinnit, raportti ja esitysmateriaalit.

## Riskit ja varasuunnitelma

Suurimmat riskit liittyvät datasetin kokoon, luokkien epätasapainoon ja siihen, että jotkin tunnetilat ovat vaikeasti erotettavia. Jos koulutus osoittautuu raskaaksi, mallien epookkimäärää ja kuvan kokoa voidaan pienentää. Tulosten arvioinnissa painotetaan kokonaisaccuracyn lisäksi virheanalyysiä ja eettistä pohdintaa.
