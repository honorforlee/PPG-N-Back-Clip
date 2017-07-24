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

## Sensors and Features
|Sensor|Feature|Dimension|
|:--|:--|:-:|
|PPG Finger Clip|PPG-45|45|
||Stress-Induced Vascular Response Index (sVRI)|1|
|Skin Conductance Electrodes|Mean Skin Conductance Level|1|
||Minimum Skin Conductance Level|1|
|ECG Electrodes|Heart Rate (R-R Interval, RRI)|1|
||Root Mean Squared Successive Difference (RMSSD)|1|
||Mid-Frequency Heart Rate Variability (MF-HRV)|1|
||High-Frequency Heart Rate Variability (HF-HRV)|1|

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
### Module: `configure`
Excerpt from `configure.py`:

```python
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
```

### Module: `ppg.common`
```python
make_dirs_for_file(filename)
```
```python
exist_file(filename, overwrite=False, display_info=True)
```
```python
load_text(filename, display_info=True)
```
```python
load_json(filename, display_info=True)
```
```python
dump_json(data, filename, overwrite=False, display_info=True)
```
```python
parse_iso_time_string(timestamp)
```
```python
next_pow2(x)
```
```python
scale(data)
```
```python
set_matplotlib_backend(backend=None)
```
```python
plot(args)
```

### Module: `ppg.parameter`
Excerpt from `ppg/parameter.py`:

```python
REST_DURATION = 5 * 60
BLOCK_DURATION = 2 * 60

PPG_SAMPLE_RATE = 200
PPG_FIR_FILTER_TAP_NUM = 200
PPG_FILTER_CUTOFF = [0.5, 5.0]

BIOPAC_HEADER_LINES = 11
BIOPAC_MSEC_PER_SAMPLE_LINE_NUM = 2
BIOPAC_ECG_CHANNEL = 1
BIOPAC_SKIN_CONDUCTANCE_CHANNEL = 3
```
### Module: `ppg.signal`
#### Peak Finding
```python
find_extrema(signal)
```

#### PPG Signal Smoothing
```python
smooth_ppg_signal(
    signal, 
    sample_rate=PPG_SAMPLE_RATE,
    numtaps=PPG_FIR_FILTER_TAP_NUM, 
    cutoff=PPG_FILTER_CUTOFF
)
```

#### PPG Single-Waveform Validation
```python
validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

#### PPG Single-Waveform Extraction
```python
extract_ppg_single_waveform(signal, sample_rate=PPG_SAMPLE_RATE)
```

### Module: `ppg.feature`
#### PPG Features
##### PPG-45
```python
extract_svri(single_waveform)
```

##### Stress-Induced Vascular Response Index (sVRI)
```python
extract_ppg45(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

#### Skin Conductance Features
##### Mean Skin Conductance Level
##### Minimum Skin Conductance Level
#### ECG Features
##### Heart Rate (R-R Interval, RRI)
##### Root Mean Squared Successive Difference (RMSSD)
##### Mid-Frequency Heart Rate Variability (MF-HRV)
##### High-Frequency Heart Rate Variability (HF-HRV)
