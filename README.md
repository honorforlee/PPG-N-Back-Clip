# PPG
Photoplethysmogram-based Real-Time Cognitive Load Assessment Using Multi-Feature Fusion Model

## File Structure
```
├── data/
│   ├── raw/
│   │   ├── meta/
│   │   ├── ppg/
│   │   └── biopac/
│   ├── segmented/
│   ├── preprocessed/
│   └── extracted/
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
- **Location:** `data/raw`

#### Meta Data
- **Location:** `data/raw/meta`
- **Filename format:** `<participant>-<session_id>.json`

#### PPG Data
- **Location:** `data/raw/ppg`
- **Filename format:** `<participant>-<session_id>-<year>_<month>_<day>_<hour>_<minute>_<second>.txt`

#### BIOPAC Data
- **Location:** `data/raw/biopac`
- **Filename format:** `<participant>-<session_id>-<seconds_before_start>.txt`

### Segmented Raw Data
- **Location:** `data/segmented`
- **Filename format:** `<participant>.json`

### Preprocessed Data
- **Location:** `data/segmented`
- **Filename format:** `<participant>.json`

### Extracted Feature Data
- **Location:** `data/extracted`
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
#### Smoothing
#### Single-Waveform Extraction
### Feature Extraction
#### PPG-45
#### Stress-Induced Vascular Response Index (sVRI)

