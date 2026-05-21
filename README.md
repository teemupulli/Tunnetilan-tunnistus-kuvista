# Tunnetilan tunnistus kuvista

Tämä projekti on loppuprojekti 4 kurssille. Tavoitteena on luokitella kasvojen ilmeitä eri tunnetiloihin käyttäen neuroverkkoja ja siirto-oppimista.

## Projektin tavoite

Rakennetaan kuvapohjainen tunnetilaluokittelija, joka tunnistaa ihmisten kasvoista perustunnetiloja. Toteutus perustuu FER-2013-datasettiin ja sisältää kolmen malliasetelman vertailun:

1. Oma baseline-CNN
2. MobileNetV2 feature extraction
3. MobileNetV2 fine-tuning

## Datasetti

Projektissa käytetty datasetti:

- FER-2013: https://www.kaggle.com/datasets/msambare/fer2013

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
- `notebooks/01_emotion_recognition_fer2013.ipynb` : projektin päänotebook, jossa datan tarkistus, koulutus ja arviointi on koottu yhteen
- `src/data_pipeline.py` : datan lataus ja augmentaatio
- `src/models.py` : baseline- ja transfer learning -mallit
- `src/train.py` : mallin koulutus
- `src/evaluate.py` : testiarviointi ja confusion matrix
- `src/inference.py` : yksittäisen kuvan ennustus
- `report/` : kuvat, tulokset ja raportti
- `notebooks/` : projektin notebookit ja niiden vientiversiot

## Asennus

```bash
pip install -r requirements.txt
```

Jos notebook antaa virheen tyyliin `ModuleNotFoundError`, aktiivinen Jupyter-kernel ei yleensä käytä samaa Python-ympäristöä, johon riippuvuudet on asennettu. Riippuvuudet asennetaan samaan ympäristöön komennolla:

```bash
pip install -r requirements.txt
```

Ympäristön voi rekisteröidä myös omaksi Jupyter-kerneliksi:

```bash
python -m ipykernel install --user --name tunnetila-fer --display-name "Python (tunnetila-fer)"
```

## Koulutus

Työnkulku voidaan ajaa joko skripteillä tai notebookin kautta. Projektin tulokset on koottu notebookiin:

```bash
jupyter notebook notebooks/01_emotion_recognition_fer2013.ipynb
```

Notebook sisältää:

- datasetin tarkistuksen
- baseline-CNN:n koulutuksen
- MobileNetV2 feature extraction -koulutuksen
- fine-tuning-vaiheen
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

## Repossa mukana

Projektin keskeiset tiedostot ja tuotokset ovat:

- notebook `.ipynb`
- notebookin `.html`-versio
- datasetin lähde ja datan asetteluohje
- ohjeet mallien uudelleenkouluttamiseen
- raportti, jossa käsitellään tekninen toteutus, tulokset, eettiset näkökohdat ja tekoälyn käyttö

Raakadataa ja koulutettuja mallipainoja ei versionoida repossa. Datasetti sijoitetaan paikallisesti `dataset/raw/`-kansioon ja mallit tallentuvat koulutuksen aikana `models/`-kansioon.

Notebookin HTML-versio tuotetaan komennolla:

```bash
jupyter nbconvert --to html notebooks/01_emotion_recognition_fer2013.ipynb
```

## Analyysin painopisteet

- tunnetilaluokkien sekoittuminen confusion matrixissa
- data-augmentaation merkitys haastaville luokille
- baseline-CNN:n, feature extractionin ja fine-tuningin erot
- luokkaepätasapainon vaikutus mallin toimintaan
- tunnetilan tunnistuksen eettiset riskit ja rajoitukset

## Huomio

FER-2013 sisältää valmiiksi haastavia, pieniä ja usein matalakontrastisia kasvokuvia. Siksi täydellisiä tuloksia ei odoteta. Projektin vahvuus tulee siitä, että koulutusprosessi, vertailu ja virheanalyysi dokumentoidaan huolellisesti.
