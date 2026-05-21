Sijoita FER-2013-datasetti tai siitä muodostettu kuvahakemistorakenne tähän kansioon.

Suositeltu rakenne:

```text
dataset/raw/train/<class_name>/*.jpg
dataset/raw/val/<class_name>/*.jpg
dataset/raw/test/<class_name>/*.jpg
```

Esimerkki luokista:

```text
dataset/raw/train/angry/*.jpg
dataset/raw/train/disgust/*.jpg
dataset/raw/train/fear/*.jpg
dataset/raw/train/happy/*.jpg
dataset/raw/train/sad/*.jpg
dataset/raw/train/surprise/*.jpg
dataset/raw/train/neutral/*.jpg
```

Jos lataamasi FER-2013-versio tulee CSV-muodossa, tee siitä ensin kuvatiedostot ja jaa ne train/val/test-kansioihin. Tätä varten voi myöhemmin lisätä erillisen muunnosskriptin.

Jos datasetissä ei ole valmista validation-jakoa, voit tehdä esimerkiksi jaon:

- train 70 %
- val 15 %
- test 15 %
