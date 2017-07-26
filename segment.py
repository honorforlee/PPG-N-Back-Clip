# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from datetime import datetime, timedelta
from configure import BASE_DIR
from ppg.parameter import TOTAL_SESSION_NUM, REST_DURATION, BLOCK_DURATION, PPG_SAMPLE_RATE
from ppg.parameter import BIOPAC_HEADER_LINES, BIOPAC_MSEC_PER_SAMPLE_LINE_NUM, BIOPAC_ECG_CHANNEL, BIOPAC_SKIN_CONDUCTANCE_CHANNEL
from ppg.utils import make_dirs_for_file, exist, load_text, load_json, dump_json, parse_iso_time_string


raw_meta_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'meta')
raw_ppg_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'ppg')
raw_biopac_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'biopac')
segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')


output_data = {}
completeness = {}


# Meta data
if exist(pathname=raw_meta_data_dir):
    for filename_with_ext in fnmatch.filter(os.listdir(raw_meta_data_dir), '*.json'):
        filename, file_ext = os.path.splitext(filename_with_ext)
        participant, session_id = filename.split('-')
        if participant not in output_data:
            output_data[participant] = {}
        if participant not in completeness:
            completeness[participant] = True
        output_data[participant][session_id] = {
            'rest': {},
            'blocks': []
        }
        pathname = os.path.join(raw_meta_data_dir, filename_with_ext)
        raw_json_data = load_json(pathname=pathname)
        if raw_json_data is not None:
            output_data[participant][session_id]['rest'] = {
                'start_time': parse_iso_time_string(raw_json_data['rest_start_timestamp']),
                'ppg': {
                    'sample_rate': None,
                    'signal': None,
                },
                'ecg': {
                    'sample_rate': None,
                    'signal': None,
                },
                'skin_conductance': {
                    'sample_rate': None,
                    'signal': None,
                },
            }
            for block in raw_json_data['blocks']:
                if block['stimuli'][0]['timestamp']['load'] is None:
                    print 'Skip one invalid block in \'%s\'.' % filename_with_ext
                    completeness[participant] = False
                    continue
                output_data[participant][session_id]['blocks'].append({
                    'level': block['level'],
                    'rsme': int(block['rsme']),
                    'start_time': parse_iso_time_string(block['stimuli'][0]['timestamp']['load']),
                    'stimuli': [{
                        'stimulus': item['stimulus'],
                        'is_target': item['is_target'],
                        'answer': item['answer'],
                        'correct': item['correct'],
                        'response_time': item['response_time'],
                    } for item in block['stimuli']],
                    'ppg': {
                        'sample_rate': None,
                        'signal': None,
                    },
                    'ecg': {
                        'sample_rate': None,
                        'signal': None,
                    },
                    'skin_conductance': {
                        'sample_rate': None,
                        'signal': None,
                    },
                })


# PPG data
if exist(pathname=raw_ppg_data_dir):
    for filename_with_ext in fnmatch.filter(os.listdir(raw_ppg_data_dir), '*.txt'):
        filename, file_ext = os.path.splitext(filename_with_ext)
        participant, session_id, time_str = filename.split('-')
        raw_ppg_data_start_time = datetime(*[int(item) for item in time_str.split('_')])
        if participant not in output_data or session_id not in output_data[participant]:
            completeness[participant] = False
            continue
        if raw_ppg_data_start_time > output_data[participant][session_id]['rest']['start_time']:
            print 'Recoding data started too late in \'%s\': %s > %s' % (filename_with_ext, raw_ppg_data_start_time, output_data[participant][session_id]['rest']['start_time'])
        pathname = os.path.join(raw_ppg_data_dir, filename_with_ext)
        raw_ppg_data = load_text(pathname=pathname)
        if raw_ppg_data is not None:
            raw_ppg_data = map(float, raw_ppg_data)
            tdelta = output_data[participant][session_id]['rest']['start_time'] - raw_ppg_data_start_time
            if tdelta.total_seconds() < 0:
                print 'Skip \'rest\' PPG data.'
                completeness[participant] = False
                continue
            start_index = int(tdelta.total_seconds() * PPG_SAMPLE_RATE)
            length = REST_DURATION * PPG_SAMPLE_RATE
            end_index = start_index + length
            ppg_data = raw_ppg_data[start_index:end_index]
            if len(ppg_data) < length:
                print 'Not enough \'rest\' PPG data (%s < %s). Skip.' % (len(ppg_data), length)
                completeness[participant] = False
                continue
            output_data[participant][session_id]['rest']['ppg']['sample_rate'] = PPG_SAMPLE_RATE
            output_data[participant][session_id]['rest']['ppg']['signal'] = ppg_data
            for block in output_data[participant][session_id]['blocks']:
                tdelta = block['start_time'] - raw_ppg_data_start_time
                if tdelta.total_seconds() < 0:
                    print 'Skip one block PPG data.'
                    completeness[participant] = False
                    continue
                start_index = int(tdelta.total_seconds() * PPG_SAMPLE_RATE)
                length = BLOCK_DURATION * PPG_SAMPLE_RATE
                end_index = start_index + length
                ppg_data = raw_ppg_data[start_index:end_index]
                if len(ppg_data) < length:
                    print 'Not enough one block PPG data (%s < %s). Skip.' % (len(ppg_data), length)
                    completeness[participant] = False
                    continue
                block['ppg']['sample_rate'] = PPG_SAMPLE_RATE
                block['ppg']['signal'] = ppg_data


# BIOPAC data
if exist(pathname=raw_biopac_data_dir):
    for filename_with_ext in fnmatch.filter(os.listdir(raw_biopac_data_dir), '*.txt'):
        filename, file_ext = os.path.splitext(filename_with_ext)
        participant, session_id, seconds_str = filename.split('-')
        pre_tdelta = timedelta(seconds=int(seconds_str))
        if participant not in output_data or session_id not in output_data[participant]:
            completeness[participant] = False
            continue
        pathname = os.path.join(raw_biopac_data_dir, filename_with_ext)
        raw_biopac_data = load_text(pathname=pathname)
        if raw_biopac_data is not None:
            sample_rate = 1000 / int(raw_biopac_data[BIOPAC_MSEC_PER_SAMPLE_LINE_NUM-1].split(' ')[0].strip())
            raw_ecg_data = [float(line.split('\t')[BIOPAC_ECG_CHANNEL].strip()) for line in raw_biopac_data[BIOPAC_HEADER_LINES:]]
            raw_skin_conductance_data = [float(line.split('\t')[BIOPAC_SKIN_CONDUCTANCE_CHANNEL].strip()) for line in raw_biopac_data[BIOPAC_HEADER_LINES:]]
            tdelta = pre_tdelta
            if tdelta.total_seconds() < 0:
                print 'Skip \'rest\' ECG/skin conductance data.'
                completeness[participant] = False
                continue
            start_index = int(tdelta.total_seconds() * sample_rate)
            length = REST_DURATION * sample_rate
            end_index = start_index + length
            ecg_data = raw_ecg_data[start_index:end_index]
            skin_conductance_data = raw_skin_conductance_data[start_index:end_index]
            if len(ecg_data) < length:
                print 'Not enough \'rest\' ECG/skin conductance data (%s < %s). Skip.' % (len(ecg_data), length)
                completeness[participant] = False
                continue
            output_data[participant][session_id]['rest']['ecg']['sample_rate'] = sample_rate
            output_data[participant][session_id]['rest']['ecg']['signal'] = ecg_data
            output_data[participant][session_id]['rest']['skin_conductance']['sample_rate'] = sample_rate
            output_data[participant][session_id]['rest']['skin_conductance']['signal'] = skin_conductance_data
            for block in output_data[participant][session_id]['blocks']:
                tdelta = block['start_time'] - output_data[participant][session_id]['rest']['start_time'] + pre_tdelta
                if tdelta.total_seconds() < 0:
                    print 'Skip one block ECG/skin conductance data.'
                    completeness[participant] = False
                    continue
                start_index = int(tdelta.total_seconds() * sample_rate)
                length = BLOCK_DURATION * sample_rate
                end_index = start_index + length
                ecg_data = raw_ecg_data[start_index:end_index]
                skin_conductance_data = raw_skin_conductance_data[start_index:end_index]
                if len(ecg_data) < length:
                    print 'Not enough one block ECG/skin conductance data (%s < %s). Skip.' % (len(ecg_data), length)
                    completeness[participant] = False
                    continue
                block['ecg']['sample_rate'] = sample_rate
                block['ecg']['signal'] = ecg_data
                block['skin_conductance']['sample_rate'] = sample_rate
                block['skin_conductance']['signal'] = skin_conductance_data


# Clean up time data
for participant in output_data:
    for session_id in output_data[participant]:
        del output_data[participant][session_id]['rest']['start_time']
        for block in output_data[participant][session_id]['blocks']:
            del block['start_time']


# Save segmented signal data
for participant in output_data:
    output_filename = '%s.json' % participant
    if completeness[participant] and len(output_data[participant]) == TOTAL_SESSION_NUM:
        dump_json(data=output_data[participant], pathname=os.path.join(segmented_data_dir, output_filename), overwrite=True)
    else:
        dump_json(data=output_data[participant], pathname=os.path.join(segmented_data_dir, 'incomplete', output_filename), overwrite=True)