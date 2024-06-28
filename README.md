# Data Preprocessing for Lyrics Alignment and Transcription

This repository contains code for data preprocessing for lyrics alignment and transcription tasks.
The aim is to reduce the hassle of data preprocessing on DALI v2, MulJam v2, and MultiLang Jamendo v1.1,
including downloading, source separation, and segmentation.

## Configuration

Specify where to save the data by setting the environment variable `WORKING_PATH` to the root directory of this repository.
```
export WORKING_PATH=/path/to/save/data
```
Please have a look at `data_util.py` and customize it (datasets, paths, etc.).

## Downloading

Access to DALI dataset needs to be granted: [https://zenodo.org/records/3576083](https://zenodo.org/records/3576083)

To download MulJam and Jamendo, please run the following command and specify the dataset (`MulJam` or `Jamendo`):
```
python download.py --dataset MulJam
```

All the audio files will be saved in `mix_dir`.

## Source separation

To separate the vocals from the music, we use the pretrained [Demucs](https://github.com/facebookresearch/demucs) model.
By default, it applies on all the audio files in `mix_dir`. To specify a subset, please provide the `--ids_file` argument:

```
python separate.py [--ids_file ./input/dummy/dali_dummy_ids.npy]
```

All the source-separated files will be saved in `sepa_dir`.

## Segmentation

For segmentation, a metadata file is required to specify the start and end time of each lyric line. 
It needs to have the following information for each line (see `./input/dummy/*.meta` for example)

```csv
seg_id,song_file,line_start,line_end
```
Also specify the `--split` argument to indicate the split of the dataset (train, valid, or test),
because for training set we distribute files by their prefixes to improve file system performance.
```
python segment.py --meta_file ./input/preconstructed-split/jamendo_line.meta --split test
```

All the segmented files will be saved in `seg_dir`, and the utterances are organized as the following structure:
```
$seg_dir
├── train
    ├── 00/000_0.wav
    ├── 42/420_1.wav
    └── ...
├── valid
    ├── 126_43.wav
    ├── 731_9.wav
    └── ...
└── test
    ├── 999_0.wav
    ├── 999_1.wav
    └── ...
```

## Preconstructed Data Splits

Data splits for the latest version datasets are provided in `./input/preconstructed-split/`. 
Please read the README.md in that directory for more details.