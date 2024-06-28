# Preconstructed Data Splits: DALI v2.0, MulJam v2, and MultiLang Jamendo v1.1

This directory contains preconstructed data splits for the datasets used for segmentation.

MulJam v2 files follow the official splits here: [https://github.com/zhuole1025/LyricWhiz/tree/main/MulJam_v2.0/preconstructed-split](https://github.com/zhuole1025/LyricWhiz/tree/main/MulJam_v2.0/preconstructed-split)

MultiLang Jamendo file is generated from the official annotation: [https://github.com/f90/jamendolyrics](https://github.com/f90/jamendolyrics)

![image](utterances.png)

Note that these splits are for the latest version datasets: DALI v2.0, MulJam v2, and MultiLang Jamendo v1.1. 
They are **NOT** the same splits used in a few previous papers, which uses older versions of the datasets.

*The latest version splits in this directory are recommended for future research. For reproducing purpose, please read further.

### Towards Building an End-to-End Multilingual Automatic Lyrics Transcription Model (EUSIPCO 2024)

This [paper](https://qmro.qmul.ac.uk/xmlui/bitstream/handle/123456789/97337/Huang%20Towards%20Building%20an%202024%20Accepted.pdf?sequence=2&isAllowed=y) ([repo](https://github.com/jhuang448/MultilingualALT)) uses DALI v2, MulJam v1, and MultiLang Jamendo v1.
MulJam v1 and MultiLang Jamendo v1 are also provided for reference in the `./input/v1/` directory. Below are the splits:
```
# train
./input/preconstructed-split/dali_train.meta
./input/v1/muljam_train.meta
# valid
./input/v1/muljam_valid.meta
# test
./input/v1/jamendo_line.meta
```

### More coming soon...