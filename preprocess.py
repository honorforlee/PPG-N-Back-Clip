# -*- coding: utf-8 -*-

import sys


reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from datetime import datetime, timedelta
from common import BASE_DIR, make_dirs_for_file, exist_file, parse_iso_time_string
from config import REST_DURATION, BLOCK_DURATION, PPG_SAMPLE_RATE


raw_json_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'json')
raw_ppg_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'ppg')
raw_biopac_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'biopac')
segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')


output_data = {}


# JSON data
for filename_with_ext in fnmatch.filter(os.listdir(raw_json_data_dir), '*.json'):
    filename, file_ext = os.path.splitext(filename_with_ext)
    participant, session_id = filename.split('-')
    if participant not in output_data:
        output_data[participant] = {}
    output_data[participant][session_id] = {
        'rest': {},
        'blocks': []
    }
    full_filename = os.path.join(raw_json_data_dir, filename_with_ext)
    if exist_file(full_filename, display_info=True):
        with open(full_filename, 'r') as f:
            raw_json_data = json.load(f)
            output_data[participant][session_id]['rest'] = {
                'start_time': parse_iso_time_string(raw_json_data['rest_start_timestamp']),
                'ppg': {
                    'sample_rate': None,
                    'data': None,
                },
                'ecg': {
                    'sample_rate': None,
                    'data': None,
                },
                'skin_conductance': {
                    'sample_rate': None,
                    'data': None,
                },
            }
            for block in raw_json_data['blocks']:
                if block['stimuli'][0]['timestamp']['load'] is None:
                    print 'Skip one invalid block in \'%s\'.' % filename_with_ext
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
                        'data': None,
                    },
                    'ecg': {
                        'sample_rate': None,
                        'data': None,
                    },
                    'skin_conductance': {
                        'sample_rate': None,
                        'data': None,
                    },
                })


# PPG data
for filename_with_ext in fnmatch.filter(os.listdir(raw_ppg_data_dir), '*.txt'):
    filename, file_ext = os.path.splitext(filename_with_ext)
    participant, session_id, time_str = filename.split('-')
    raw_ppg_data_start_time = datetime(*[int(item) for item in time_str.split('_')])
    if participant not in output_data or session_id not in output_data[participant]:
        continue
    if raw_ppg_data_start_time > output_data[participant][session_id]['rest']['start_time']:
        print 'Recoding data started too late in \'%s\': %s > %s' % (filename_with_ext, raw_ppg_data_start_time, output_data[participant][session_id]['rest']['start_time'])
    full_filename = os.path.join(raw_ppg_data_dir, filename_with_ext)
    if exist_file(full_filename, display_info=True):
        with open(full_filename, 'r') as f:
            raw_ppg_data = [float(line.strip()) for line in f.readlines()]
            tdelta = output_data[participant][session_id]['rest']['start_time'] - raw_ppg_data_start_time
            if tdelta.total_seconds() < 0:
                print 'Skip \'rest\' PPG data.'
                continue
            start_index = int(tdelta.total_seconds() * PPG_SAMPLE_RATE)
            length = REST_DURATION * PPG_SAMPLE_RATE
            end_index = start_index + length
            ppg_data = raw_ppg_data[start_index:end_index]
            if len(ppg_data) != length:
                print 'Not enough \'rest\' PPG data (%s < %s). Skip.' % (len(ppg_data), length)
                continue
            output_data[participant][session_id]['rest']['ppg']['sample_rate'] = PPG_SAMPLE_RATE
            output_data[participant][session_id]['rest']['ppg']['data'] = ppg_data
            for block in output_data[participant][session_id]['blocks']:
                tdelta = block['start_time'] - raw_ppg_data_start_time
                if tdelta.total_seconds() < 0:
                    print 'Skip one block PPG data.'
                    continue
                start_index = int(tdelta.total_seconds() * PPG_SAMPLE_RATE)
                length = BLOCK_DURATION * PPG_SAMPLE_RATE
                end_index = start_index + length
                ppg_data = raw_ppg_data[start_index:end_index]
                if len(ppg_data) != length:
                    print 'Not enough one block PPG data (%s < %s). Skip.' % (len(ppg_data), length)
                    continue
                block['ppg']['sample_rate'] = PPG_SAMPLE_RATE
                block['ppg']['data'] = ppg_data


# BIOPAC data
for filename_with_ext in fnmatch.filter(os.listdir(raw_biopac_data_dir), '*.txt'):
    filename, file_ext = os.path.splitext(filename_with_ext)
    participant, session_id, seconds_str = filename.split('-')
    pre_tdelta = timedelta(seconds=int(seconds_str))
    if participant not in output_data or session_id not in output_data[participant]:
        continue
    full_filename = os.path.join(raw_biopac_data_dir, filename_with_ext)
    if exist_file(full_filename, display_info=True):
        with open(full_filename, 'r') as f:
            raw_biopac_data = [line.strip() for line in f.readlines()]
            sample_rate = 1000 / int(raw_biopac_data[1].split(' ')[0].strip())
            raw_ecg_data = [float(line.split('\t')[1].strip()) for line in raw_biopac_data[11:]]
            raw_skin_conductance_data = [float(line.split('\t')[3].strip()) for line in raw_biopac_data[11:]]
            tdelta = pre_tdelta
            if tdelta.total_seconds() < 0:
                print 'Skip \'rest\' ECG/skin conductance data.'
                continue
            start_index = int(tdelta.total_seconds() * sample_rate)
            length = REST_DURATION * sample_rate
            end_index = start_index + length
            ecg_data = raw_ecg_data[start_index:end_index]
            skin_conductance_data = raw_skin_conductance_data[start_index:end_index]
            if len(ecg_data) != length:
                print 'Not enough \'rest\' ECG/skin conductance data (%s < %s). Skip.' % (len(ecg_data), length)
                continue
            output_data[participant][session_id]['rest']['ecg']['sample_rate'] = sample_rate
            output_data[participant][session_id]['rest']['ecg']['data'] = ecg_data
            output_data[participant][session_id]['rest']['skin_conductance']['sample_rate'] = sample_rate
            output_data[participant][session_id]['rest']['skin_conductance']['data'] = skin_conductance_data
            for block in output_data[participant][session_id]['blocks']:
                tdelta = block['start_time'] - output_data[participant][session_id]['rest']['start_time'] + pre_tdelta
                if tdelta.total_seconds() < 0:
                    print 'Skip one block ECG/skin conductance data.'
                    continue
                start_index = int(tdelta.total_seconds() * sample_rate)
                length = BLOCK_DURATION * sample_rate
                end_index = start_index + length
                ecg_data = raw_ecg_data[start_index:end_index]
                skin_conductance_data = raw_skin_conductance_data[start_index:end_index]
                if len(ecg_data) != length:
                    print 'Not enough one block ECG/skin conductance data (%s < %s). Skip.' % (len(ecg_data), length)
                    continue
                block['ecg']['sample_rate'] = sample_rate
                block['ecg']['data'] = ecg_data
                block['skin_conductance']['sample_rate'] = sample_rate
                block['skin_conductance']['data'] = skin_conductance_data


# Clean up time data
for participant in output_data:
    for session_id in output_data[participant]:
        del output_data[participant][session_id]['rest']['start_time']
        for block in output_data[participant][session_id]['blocks']:
            del block['start_time']


# Save segmented data
for participant in output_data:
    output_filename = '%s.json' % participant
    full_output_filename = os.path.join(segmented_data_dir, output_filename)
    make_dirs_for_file(full_output_filename)
    if not exist_file(full_output_filename, overwrite=True, display_info=True):
        print 'Write to file: %s' % full_output_filename
        with open(full_output_filename, 'w') as f:
            json.dump(output_data[participant], f)