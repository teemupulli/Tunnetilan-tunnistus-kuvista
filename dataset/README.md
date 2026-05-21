FER-2013-datasetti sijoitetaan tähän kansioon valmiina kuvahakemistorakenteena tai CSV-muodosta muunnettuna.

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

Jos datasetissä ei ole valmista validation-jakoa, train-datasta erotetaan erillinen validation-osuus. Tässä projektissa käytetty hakemistorakenne sisältää erilliset `train`, `val` ja `test` -osiot.
