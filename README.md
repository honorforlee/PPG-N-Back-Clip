[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)][repository]
[![Python](https://img.shields.io/badge/Python-2.7-blue.svg)][python]
[![License](https://img.shields.io/github/license/iROCKBUNNY/PPG.svg)][license]
[![Watchers](https://img.shields.io/github/watchers/iROCKBUNNY/PPG.svg?style=social&label=Watch)][watch]
[![Stargazers](https://img.shields.io/github/stars/iROCKBUNNY/PPG.svg?style=social&label=Star)][star]
[![Forks](https://img.shields.io/github/forks/iROCKBUNNY/PPG.svg?style=social&label=Fork)][fork]

# PPG
Photoplethysmogram-based Real-Time Cognitive Load Assessment Using Multi-Feature Fusion Model

## Installation
### Requirements
- [macOS][macos] (Recommended)
- [Python 2.7][python]
- [Pip][pip]
- [Virtualenv][virtualenv]

### Installing with Virtualenv
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
git clone https://github.com/iROCKBUNNY/PPG.git
cd PPG
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
./scripts/process_data.sh
./scripts/classify.sh
```

## Usage
### Data Processing
##### Raw data segmentation
```sh
python segment.py
```

##### Preprocessing
```sh
python preprocess.py
```

##### Feature extraction
```sh
python extract.py
```

##### Training set and test set spliting
```sh
python split.py
```

### Classification
```sh
python classify.py
```

## Data Definition
### N-Back Task Meta Data
- **Location:** `data/raw/meta/`
- **Filename format:** `<participant>-<session_id>.json`

###### Sample Data
```js
{
  "rest_start_timestamp": <timestamp>,
  "blocks": [
    {
      "level": <level>,
      "level_alias": <level_alias>,
      "header": <header>,
      "image_src": <image_src>,
      "image_alt": <image_alt>,
      "stimuli": [
        {
          "stimulus": <stimulus>,
          "load_time": <value>,
          "unload_time": <value>,
          "response_time": <value>,
          "is_target": <bool>,
          "answer": <bool>,
          "correct": <bool>,
          "timestamp": {
            "load": <timestamp>,
            "response": <timestamp>
          }
        },
        ...
      ],
      "total_time": <value>,
      "rsme": <rsme>
    },
    ...
  ]
}
```

### PPG Signal Data
- **Location:** `data/raw/ppg/`
- **Filename format:** `<participant>-<session_id>-<year>_<month>_<day>_<hour>_<minute>_<second>.txt`

###### Sample Data
```
109
110
109
109
...
```

### BIOPAC Signal Data
- **Location:** `data/raw/biopac/`
- **Filename format:** `<participant>-<session_id>-<seconds_before_start>.txt`

###### Sample Data
```
SampleData.acq
1 msec/sample
3 channels
ECG - ECG100C
mV
PPG - PPG100C
Volts
Skin conductance - GSR100C
microsiemens
min	CH1	CH2	CH9
	1161418	1161418	1161418
0	-2.26685	-0.194092	3.43475
1.66667E-05	-2.25769	-0.197449	3.44086
3.33333E-05	-2.24915	-0.198975	3.4378
...
```

### Segmented Signal Data
- **Location (complete data):** `data/segmented/`
- **Location (incomplete data):** `data/segmented/incomplete/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "1": {
    "rest": {
      "ppg": {
        "sample_rate": <value>,
        "signal": [ ... ]
      },
      "ecg": {
        "sample_rate": <value>,
        "signal": [ ... ]
      },
      "skin_conductance": {
        "sample_rate": <value>,
        "signal": [ ... ]
      }
    },
    "blocks": [
      {
        "level": <level>,
        "stimuli": [
          {
            "stimulus": <stimulus>,
            "correct": <bool>,
            "is_target": <bool>,
            "answer": <bool>,
            "response_time": <value>
          },
          ...
        ],
        "rmse": <rmse>,
        "ppg": {
          "smaple_rate": <value>,
          "signal": [ ... ]
        },
        "ecg": {
          "smaple_rate": <value>,
          "signal": [ ... ]
        },
        "skin_conductance": {
          "smaple_rate": <value>,
          "signal": [ ... ]
        }
      },
      ...
    ]
  },
  "2": { ... }
}
```

### Preprocessed Data
- **Location:** `data/preprocessed/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "1": {
    "rest": {
      "ppg": {
        "sample_rate": <value>,
        "single_waveforms": [
          [ ... ]
          ...
        ]
      },
      "ecg": {
        "sample_rate": <value>,
        "rri": [ ... ],
        "rri_interpolated": [ ... ]
      },
      "skin_conductance": {
        "sample_rate": <value>,
        "signal": [ ... ]
      }
    },
    "blocks": [
      {
        "level": <level>,
        "stimuli": [
          {
            "stimulus": <stimulus>,
            "correct": <bool>,
            "is_target": <bool>,
            "answer": <bool>,
            "response_time": <value>
          },
          ...
        ],
        "rmse": <rmse>,
        "ppg": {
          "smaple_rate": <value>,
          "single_waveforms": [
            [ ... ],
            ...
          ]
        },
        "ecg": {
          "smaple_rate": <value>,
          "rri": [ ... ],
          "rri_interpolated": [ ... ]
        },
        "skin_conductance": {
          "smaple_rate": <value>,
          "signal": [ ... ]
        }
      },
      ...
    ]
  },
  "2": { ... }
}
```

### Extracted Feature Data
- **Location:** `data/extracted/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "1": {
    "rest": {
      "ppg": {
        "sample_rate": <value>,
        "ppg45": [
            [ ... ],
            ...
        ],
        "svri": [ ... ]
      },
      "skin_conductance": {
        "sample_rate": <value>,
        "average_level": <value>,
        "minimum_level": <value>
      },
      "ecg": {
        "sample_rate": <value>,
        "average_rri": <value>,
        "rmssd": <value>,
        "mf_hrv_power": <value>,
        "hf_hrv_power": <value>
      }
    },
    "blocks": [
      {
        "level": <level>,
        "stimuli": [
          {
            "stimulus": <stimulus>,
            "correct": <bool>,
            "is_target": <bool>,
            "answer": <bool>,
            "response_time": <value>
          },
          ...
        ],
        "rmse": <value>,
        "ppg": {
          "smaple_rate": <value>,
          "ppg45": [
            [ ... ],
            ...
          ],
          "svri": [ ... ]
        },
        "skin_conductance": {
          "sample_rate": <value>,
          "average_level": <value>,
          "minimum_level": <value>
        },
        "ecg": {
          "sample_rate": <value>,
          "average_rri": <value>,
          "rmssd": <value>,
          "mf_hrv_power": <value>,
          "hf_hrv_power": <value>
        }
      },
      ...
    ]
  },
  "2": { ... }
}
```

### Splited Feature Data
- **Location:** `data/splited/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "train": {
    "0": [
      {
        "ppg45": [
          [ ... ],
          ...
        ],
        "ppg45_cr": [
          [ ... ],
          ,,,
        ],
        "svri": [ ... ],
        "svri_cr": [ ... ],
        "average_skin_conductance_level": <value>,
        "average_skin_conductance_level_cr": <value>,
        "minimum_skin_conductance_level": <value>,
        "minimum_skin_conductance_level_cr": <value>,
        "average_rri": <value>,
        "average_rri_cr": <value>,
        "rmssd": <value>,
        "rmssd_cr": <value>,
        "mf_hrv_power": <value>,
        "mf_hrv_power_cr": <value>,
        "hf_hrv_power": <value>,
        "hf_hrv_power_cr": <value>
      },
      ...
    ],
    "1": [ ... ],
    "2": [ ... ]
  },
  "test": { ... }
}
```

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

## API Reference
### Module: `ppg`
Excerpt from `ppg/__init__.py`:

```python
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
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

TRAINING_DATA_RATIO = 0.75
```

### Module: `ppg.signal`
##### Peak Finding
```python
extrema = find_extrema(signal)
```

##### PPG Signal Smoothing
```python
smoothed_ppg_signal = smooth_ppg_signal(
    signal,
    sample_rate=PPG_SAMPLE_RATE,
    numtaps=PPG_FIR_FILTER_TAP_NUM,
    cutoff=PPG_FILTER_CUTOFF
)
```

##### PPG Single-Waveform Validation
```python
result = validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

##### PPG Single-Waveform Extraction
```python
single_waveforms = extract_ppg_single_waveform(signal, sample_rate=PPG_SAMPLE_RATE)
```

##### RRI Extraction
```python
rri, rri_time = extract_rri(signal, sample_rate)
```

##### RRI Interpolation
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
svri = extract_svri(single_waveform)
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
##### Get Feature Set
```python
train_features, train_labels, test_features, test_labels = get_feature_set(data, task_levels, feature_types)
```

#### Classifiers
##### Logistic Regression Classifier
```python
classifier = logistic_regression_classifier(features, labels)
```

##### Support Vector Classifier
```python
classifier = support_vector_classifier(features, labels)
```

##### Gaussian Naïve Bayes Classifier
```python
classifier = gaussian_naive_bayes_classifier(features, labels)
```

##### Decision Tree Classifier
```python
classifier = decision_tree_classifier(features, labels)
```

##### Random Forest Classifier
```python
classifier = random_forest_classifier(features, labels)
```

##### AdaBoost Classifier
```python
classifier = adaboost_classifier(features, labels)
```

##### Gradient Boosting Classifier
```python
classifier = gradient_boosting_classifier(features, labels)
```

##### Voting Classifier
```python
classifier = voting_classifier(estimators, features, labels)
```

### Module: `ppg.utils`
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
classifier_object = load_model(pathname, display_info=True)
```
```python
dump_model(model, pathname, overwrite=False, display_info=True)
```
```python
datetime = parse_iso_time_string(timestamp)
```
```python
change_ratio = get_change_ratio(data, baseline)
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
├── models/
│   └── ...
├── ppg/
│   ├── __init__.py
│   ├── parameter.py
│   ├── signal.py
│   ├── feature.py
│   ├── learn.py
│   └── utils.py
├── scripts/
│   └── process_data.sh
├── segment.py
├── preprocess.py
├── extract.py
├── split.py
├── classify.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## License
[MIT License][license]

[repository]: https://github.com/iROCKBUNNY/PPG "iROCKBUNNY/PPG"
[license]: https://github.com/iROCKBUNNY/PPG/LICENSE "License"
[watch]: https://github.com/iROCKBUNNY/PPG/watchers "Watchers"
[star]: https://github.com/iROCKBUNNY/PPG/stargazers "Stargazers"
[fork]: https://github.com/iROCKBUNNY/PPG/network "Forks"

[macos]: https://www.apple.com/macos/ "macOS"
[python]: https://docs.python.org/2/ "Python 2.7"
[pip]: https://pypi.python.org/pypi/pip "Pip"
[virtualenv]: https://virtualenv.pypa.io/en/stable/ "Virtualenv"
