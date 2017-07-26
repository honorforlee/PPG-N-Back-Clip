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
│   │       ├── <participant>-<session_id>-<seconds_before_start>.json
│   │       └── ...
│   ├── segmented/
|   |   ├── incomplete/
|   |   |   ├── <participant>.json
│   |   |   └── ...
│   │   ├── <participant>.json
│   │   └── ...
│   ├── preprocessed/
│   │   ├── <participant>.json
│   │   └── ...
│   └── extracted/
│       ├── <participant>.json
│       └── ...
├── ppg/
│   ├── __init__.py
│   ├── parameter.py
│   ├── signal.py
│   ├── feature.py
│   ├── learn.py
│   └── utils.py
├── configure.py
├── segment.py
├── preprocess.py
├── extract.py
├── classify.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements
- [macOS](https://www.apple.com/macos/) (Recommended)
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
|PPG finger clip|PPG-45 (39 time-domain, 9 frequency-domain)|45|
||Stress-induced vascular response index (sVRI)|1|
|Skin conductance electrodes|Average skin conductance level|1|
||Minimum skin conductance level|1|
|ECG Electrodes|Heart rate (R-R interval, RRI)|1|
||Root mean squared successive difference (RMSSD)|1|
||Mid-frequency heart rate variability (MF-HRV)|1|
||High-frequency heart rate variability (HF-HRV)|1|

### PPG-45 Feature Definition
|#|Feature|Description|
|--:|:--|:--|
|1|`x`|Systolic peak|
|2|`y`|Diastolic peak|
|3|`z`|Dicrotic notch|
|4|<code>t<sub>pi</sub></code>|Pulse interval|
|5|`y/x`|Augmentation index|
|6|`(x-y)/x`|Relative augmentation index|
|7|`z/x`||
|8|`(y-z)/x`||
|9|<code>t<sub>1</sub></code>|Systolic peak time|
|10|<code>t<sub>2</sub></code>|Diastolic peak time|
|11|<code>t<sub>3</sub></code>|Dicrotic notch time|
|12|`∆T`|Time between systolic and diastolic peaks|
|13|`w`|Full width at half systolic peak|
|14|<code>A<sub>2</sub>/A<sub>1</sub></code>|Inflection point area ratio|
|15|<code>t<sub>1</sub>/x</code>|Systolic peak rising slope|
|16|<code>y/(t<sub>pi</sub>-t<sub>3</sub>)</code>|Diastolic peak falling slope|
|17|<code>t<sub>1</sub>/t<sub>pi</sub></code>||
|18|<code>t<sub>2</sub>/t<sub>pi</sub></code>||
|19|<code>t<sub>3</sub>/t<sub>pi</sub></code>||
|20|<code>∆T/t<sub>pi</sub></code>||
|21|<code>t<sub>a1</sub></code>||
|22|<code>t<sub>b1</sub></code>||
|23|<code>t<sub>e1</sub></code>||
|24|<code>t<sub>f1</sub></code>||
|25|<code>b<sub>2</sub>/a<sub>2</sub></code>||
|26|<code>e<sub>2</sub>/a<sub>2</sub></code>||
|27|<code>(b<sub>2</sub>+e<sub>2</sub>)/a<sub>2</sub></code>||
|28|<code>t<sub>a2</sub></code>||
|29|<code>t<sub>b2</sub></code>||
|30|<code>t<sub>a1</sub>/t<sub>pi</sub></code>||
|31|<code>t<sub>b1</sub>/t<sub>pi</sub></code>||
|32|<code>t<sub>e1</sub>/t<sub>pi</sub></code>||
|33|<code>t<sub>f1</sub>/t<sub>pi</sub></code>||
|34|<code>t<sub>a2</sub>/t<sub>pi</sub></code>||
|35|<code>t<sub>b2</sub>/t<sub>pi</sub></code>||
|36|<code>(t<sub>a1</sub>+t<sub>a2</sub>)/t<sub>pi</sub></code>||
|37|<code>(t<sub>b1</sub>+t<sub>b2</sub>)/t<sub>pi</sub></code>||
|38|<code>(t<sub>e1</sub>+t<sub>2</sub>)/t<sub>pi</sub></code>||
|39|<code>(t<sub>f1</sub>+t<sub>3</sub>)/t<sub>pi</sub></code>||
|40|<code>f<sub>base</sub></code>|Fundamental component frequency|
|41|<code>\|s<sub>base</sub>\|</code>|Fundamental component magnitude|
|42|<code>f<sub>2</sub></code>|2<sup>nd</sup> harmonic frequency|
|43|<code>\|s<sub>2</sub>\|</code>|2<sup>nd</sup> harmonic magnitude|
|44|<code>f<sub>3</sub></code>|3<sup>rd</sup> harmonic frequency|
|45|<code>\|s<sub>3</sub>\|</code>|3<sup>rd</sup> harmonic magnitude|

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
```sh
python classify.py
```

## API Reference
### Module: `configure`
Excerpt from `configure.py`:

```python
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
```

### Module: `ppg.parameter`
Excerpt from `ppg/parameter.py`:

```python
TOTAL_SESSION_NUM = 2
REST_DURATION = 5 * 60
BLOCK_DURATION = 2 * 60

MINIMUM_PULSE_CYCLE = 0.5
MAXIMUM_PULSE_CYCLE = 1.2

PPG_SAMPLE_RATE = 200
PPG_FIR_FILTER_TAP_NUM = 200
PPG_FILTER_CUTOFF = [0.5, 5.0]
PPG_SYSTOLIC_PEAK_DETECTION_THRESHOLD_COEFFICIENT = 0.5

BIOPAC_HEADER_LINES = 11
BIOPAC_MSEC_PER_SAMPLE_LINE_NUM = 2
BIOPAC_ECG_CHANNEL = 1
BIOPAC_SKIN_CONDUCTANCE_CHANNEL = 3

ECG_R_PEAK_DETECTION_THRESHOLD = 2.0
ECG_MF_HRV_CUTOFF = [0.07, 0.15]
ECG_HF_HRV_CUTOFF = [0.15, 0.5]
```

### Module: `ppg.signal`
#### Peak Finding
```python
extrema = find_extrema(signal)
```

#### PPG Signal Smoothing
```python
smoothed_ppg_signal = smooth_ppg_signal(
    signal, 
    sample_rate=PPG_SAMPLE_RATE,
    numtaps=PPG_FIR_FILTER_TAP_NUM, 
    cutoff=PPG_FILTER_CUTOFF
)
```

#### PPG Single-Waveform Validation
```python
result = validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

#### PPG Single-Waveform Extraction
```python
single_waveforms = extract_ppg_single_waveform(signal, sample_rate=PPG_SAMPLE_RATE)
```

#### RRI Extraction
```python
rri, rri_time = extract_rri(signal, sample_rate)
```

#### RRI Interpolation
```python
rri_interpolated = interpolate_rri(rri, rri_time, sample_rate)
```

### Module: `ppg.feature`
#### PPG Features
##### PPG-45
```python
extract_ppg45(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

##### Stress-Induced Vascular Response Index (sVRI)
```python
average_svri = extract_average_svri(single_waveform)
```

#### Skin Conductance Features
##### Average Skin Conductance Level
```python
average_skin_conductance_level = extract_average_skin_conductance_level(signal)
```

##### Minimum Skin Conductance Level
```python
minimum_skin_conductance_level = extract_minimum_skin_conductance_level(signal)
```

#### ECG Features
##### Heart Rate (R-R Interval, RRI)
```python
avarage_rri = extract_average_rri(rri)
```

##### Root Mean Squared Successive Difference (RMSSD)
```python
rmssd = extract_rmssd(rri)
```

##### Middle/High-Frequency Heart Rate Variability (MF/HF-HRV)
```python
mf_hrv_power, hf_hrv_power = extract_hrv_power(rri, sample_rate)
```

### Module: `ppg.learn`
```python
```

### Module: `ppg.utils`
```python
path_type = path_type(pathname)
```
```python
make_dirs_for_file(pathname)
```
```python
result = exist_file(pathname, overwrite=False, display_info=True)
```
```python
text_data = load_text(pathname, display_info=True)
```
```python
json_data = load_json(pathname, display_info=True)
```
```python
dump_json(data, pathname, overwrite=False, display_info=True)
```
```python
datetime = parse_iso_time_string(timestamp)
```
```python
result = next_pow2(x)
```
```python
scaled_data = scale(data)
```
```python
set_matplotlib_backend(backend=None)
```
```python
plot(args, backend=None)
```
```python
semilogy(args, backend=None)
```
