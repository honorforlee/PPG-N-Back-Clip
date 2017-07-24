# PPG
Photoplethysmogram-based Real-Time Cognitive Load Assessment Using Multi-Feature Fusion Model

## File Structure
```
├── data/
│   ├── raw/
│   │   ├── meta/
│   │   │   ├── <participant>-<session_id>.json
│   │   │   └── ...
│   │   ├── ppg/
│   │   │   ├── <participant>-<session_id>-<year>_<month>_<day>_<hour>_<minute>_<second>.json
│   │   │   └── ...
│   │   └── biopac/
│   │   │   ├── <participant>-<session_id>-<seconds_before_start>.json
│   │   │   └── ...
│   ├── segmented/
│   │   ├── <participant>.json
│   │   └── ...
│   ├── preprocessed/
│   │   ├── <participant>.json
│   │   └── ...
│   └── extracted/
│   │   ├── <participant>.json
│   │   └── ...
├── ppg/
│   ├── __init__.py
│   ├── common.py
│   ├── feature.py
│   ├── parameter.py
│   └── signal.py
├── configure.py
├── segment.py
├── preprocess.py
├── extract.py
├── learn.py
├── classify.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements
- [Python 2.7+](https://docs.python.org/2/)
- [Pip](https://pypi.python.org/pypi/pip)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

## Installation
```sh
git clone https://github.com/iROCKBUNNY/PPG.git
cd PPG
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Data Format
### Raw Data
#### Meta Data
- **Location:** `data/raw/meta/`
- **Filename format:** `<participant>-<session_id>.json`

#### PPG Data
- **Location:** `data/raw/ppg/`
- **Filename format:** `<participant>-<session_id>-<year>_<month>_<day>_<hour>_<minute>_<second>.txt`

#### BIOPAC Data
- **Location:** `data/raw/biopac/`
- **Filename format:** `<participant>-<session_id>-<seconds_before_start>.txt`

### Segmented Raw Data
- **Location:** `data/segmented/`
- **Filename format:** `<participant>.json`

### Preprocessed Data
- **Location:** `data/preprocessed/`
- **Filename format:** `<participant>.json`

### Extracted Feature Data
- **Location:** `data/extracted/`
- **Filename format:** `<participant>.json`

## Procedures
### Raw Data Segmentation
```sh
python segment.py
```

### Preprocessing
```sh
python preprocess.py
```

### Feature Extraction
```sh
python extract.py
```

### Classification

## API Reference
### Configuration
### Common Tools
### Parameter Setting
### Signal Processing
#### PPG Signal Smoothing
#### PPG Single-Waveform Extraction
### Feature Extraction
#### PPG Features
##### PPG-45
- **Dimension:** 45

##### Stress-Induced Vascular Response Index (sVRI)
- **Dimension:** 1

#### Skin Conductance Features
##### Mean Skin Conductance Level
- **Dimension:** 1

##### Minimum Skin Conductance Level
- **Dimension:** 1

#### ECG Features
##### Heart Rate (R-R Interval, RRI)
- **Dimension:** 1

##### Root Mean Squared Successive Difference (RMSSD)
- **Dimension:** 1

##### Mid-Frequency Heart Rate Variability (MF-HRV)
- **Dimension:** 1

##### High-Frequency Heart Rate Variability (HF-HRV)
- **Dimension:** 1
