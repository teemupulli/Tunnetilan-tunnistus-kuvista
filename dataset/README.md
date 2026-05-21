FER-2013-datasetti sijoitetaan tähän kansioon joko valmiina kuvahakemistorakenteena tai CSV-muodosta muunnettuna.

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

Jos FER-2013 on ladattu CSV-muodossa, se muunnetaan ensin kuvatiedostoiksi ja jaetaan train/val/test-kansioihin.

Jos datasetissä ei ole valmista validation-jakoa, käytetty jako voi olla esimerkiksi:

- train 70 %
- val 15 %
- test 15 %
