# Tunnetilan tunnistus kuvista

Tämä projekti on loppuprojekti 4 kurssille. Tavoitteena on luokitella kasvojen ilmeitä eri tunnetiloihin käyttäen neuroverkkoja ja siirto-oppimista.

## Projektin tavoite

Rakennetaan kuvapohjainen tunnetilaluokittelija, joka tunnistaa ihmisten kasvoista perustunnetiloja. Ensimmäinen toteutus perustuu FER-2013-datasettiin ja siirto-oppimiseen. Tuloksia verrataan ainakin kahden malliasetelman välillä:

1. Oma baseline-CNN
2. Siirto-oppimismalli, esimerkiksi MobileNetV2 tai EfficientNetB0

Mahdollinen jatkolaajennus:

- fine-tuning siirto-oppimismallille
- usean mallin vertailu
- yksinkertainen ensemble kahdesta parhaasta mallista

## Datasetti

Suositeltu datasetti:

- FER-2013

Tyypilliset tunnetilaluokat:

- angry
- disgust
- fear
- happy
- sad
- surprise
- neutral

Datasetti sijoitetaan kansioon:

```text
dataset/raw/train/<class_name>/*.jpg
dataset/raw/val/<class_name>/*.jpg
dataset/raw/test/<class_name>/*.jpg
```

Jos FER-2013 tulee yhtenä CSV-tiedostona, se muunnetaan ensin yllä olevaan hakemistorakenteeseen.

## Projektin rakenne

- `project_plan.md` : lyhyt projektisuunnitelma
- `dataset/README.md` : datan asetteluohje
- `notebooks/01_emotion_recognition_fer2013.ipynb` : toistettava notebook-versio opettajaa ja palautusta varten
- `src/data_pipeline.py` : datan lataus ja augmentaatio
- `src/models.py` : baseline- ja transfer learning -mallit
- `src/train.py` : mallin koulutus
- `src/evaluate.py` : testiarviointi ja confusion matrix
- `src/inference.py` : yksittäisen kuvan ennustus
- `report/` : kuvat, tulokset ja raportti
- `notebooks/` : myöhempi notebook-versio palautusta varten

## Asennus

```bash
pip install -r requirements.txt
```

Jos notebook antaa virheen tyyliin `ModuleNotFoundError`, kyse on yleensä siitä että aktiiviseen Jupyter-kerneliin ei ole vielä asennettu projektin riippuvuuksia. Aja silloin samaan Python-ympäristöön:

```bash
pip install -r requirements.txt
```

Tarvittaessa voit rekisteröidä ympäristön myös omaksi Jupyter-kerneliksi:

```bash
python -m ipykernel install --user --name tunnetila-fer --display-name "Python (tunnetila-fer)"
```

## Koulutus

Projektin voi toteuttaa joko skripteillä tai notebookin kautta. Palautusta ja toistettavuutta varten suositeltu tapa on ajaa notebook:

```bash
jupyter notebook notebooks/01_emotion_recognition_fer2013.ipynb
```

Notebook sisältää:

- datasetin tarkistuksen
- baseline-CNN:n koulutuksen
- MobileNetV2 feature extraction -koulutuksen
- valinnaisen fine-tuning-vaiheen
- confusion matrixin ja luokitteluraportin

Skriptipohjainen ajo on edelleen hyödyllinen nopeissa kokeiluissa:

Baseline-CNN:

```bash
python src/train.py --mode cnn --data_dir dataset/raw --epochs 20 --batch_size 32 --image_size 96
```

Feature extraction MobileNetV2:lla:

```bash
python src/train.py --mode feature --data_dir dataset/raw --epochs 15 --batch_size 32 --image_size 96
```

Fine-tuning:

```bash
python src/train.py --mode finetune --data_dir dataset/raw --epochs 20 --batch_size 32 --image_size 96 --unfrozen_layers 20
```

## Arviointi

```bash
python src/evaluate.py --model_path models/feature_best.keras --data_dir dataset/raw --split test --image_size 96 --output_prefix report/feature_eval
```

## Palautusta varten

Tehtävänannon näkökulmasta lopullisessa palautuksessa pitäisi olla vähintään:

- notebook `.ipynb`
- notebookin `.html`-versio
- datasetin lähde tai linkki FER-2013-datasettiin
- koulutettujen mallien tiedostot tai ohjeet niiden uudelleenkouluttamiseen
- valmis raportti tai kattavasti dokumentoitu notebook
- tekoälyn käytön dokumentointi

HTML-version voi tehdä esimerkiksi komennolla:

```bash
jupyter nbconvert --to html notebooks/01_emotion_recognition_fer2013.ipynb
```

## Mitä tässä projektissa kannattaa analysoida

- mitkä tunnetilat sekoittuvat toisiinsa useimmin
- auttaako augmentaatio pieniä tai vaikeita luokkia
- kuinka paljon siirto-oppiminen parantaa baseline-malliin verrattuna
- missä määrin malli kärsii luokkaepätasapainosta
- tunnetilan tunnistuksen eettiset riskit ja rajoitukset

## Huomio

FER-2013 sisältää valmiiksi haastavia, pieniä ja usein matalakontrastisia kasvokuvia. Siksi täydellisiä tuloksia ei odoteta. Projektin vahvuus tulee siitä, että koulutusprosessi, vertailu ja virheanalyysi dokumentoidaan huolellisesti.
