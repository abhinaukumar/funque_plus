from typing import List, Dict, Any

import argparse
import os

import numpy as np
import pickle as pkl

from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler

from qualitylib.tools import import_python_file, read_dataset
from qualitylib.feature_extractor import get_fex
from qualitylib.runner import Runner
from qualitylib.cross_validate import random_cross_validation

from funque_plus.feature_extractors import *

np.random.seed(0)


class ScaledSVR:
    def __init__(self, *svr_args, **svr_kwargs) -> None:
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        self.reg = SVR(*svr_args, **svr_kwargs)

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        X_trans = self.scaler.fit_transform(X)
        self.reg.fit(X_trans, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.reg.predict(self.scaler.transform(X))


def print_agg_stats(stats: List[Dict[str, Any]]) -> None:
    sample_stats = stats[list(stats.keys())[0]]
    num_samples = len(sample_stats)
    lo_ci = (0.5 - 1.96*0.5/np.sqrt(num_samples))*100
    hi_ci = (0.5 + 1.96*0.5/np.sqrt(num_samples))*100

    key_stats = np.array([stat['SROCC'] for stat in stats])
    print('Stat,Median,LoCI,HiCI,Std')  # Not using spaces makes parsing text output as csv easier
    for stat_key in stats[0]:
        key_stats = np.array([stat[stat_key] for stat in stats])
        print(f'{stat_key},{np.median(key_stats):.4f},{np.percentile(key_stats, lo_ci):.4f},{np.percentile(key_stats, hi_ci):.4f},{np.std(key_stats):.4f}')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Conduct gridsearch crossvalidation')
    parser.add_argument('--dataset', help='Path to dataset file for which to extract features', type=str)
    parser.add_argument('--fex_name', help='Name of feature extractor', type=str)
    parser.add_argument('--fex_version', help='Version of feature extractor', type=str, default=None)
    parser.add_argument('--splits', help='Number of parallel processes', type=int, default=100)
    parser.add_argument('--processes', help='Number of parallel processes', type=int, default=100)
    parser.add_argument('--out_file', help='Path to output pickle file', type=str, required=False, default=None)
    return parser


def main() -> None:
    args = get_parser().parse_args()

    if args.out_file is not None and os.path.isfile(args.out_file):
        print('Result file exists already. Skipping..')
        return

    dataset = import_python_file(args.dataset)
    assets = read_dataset(dataset, shuffle=True)

    FexClass = get_fex(args.fex_name, args.fex_version)
    runner = Runner(FexClass, processes=args.processes, use_cache=True)  # Reads from stored results if available, else stores results.
    results = runner(assets, return_results=True)  # Extract features if necessary and return for cross-validation.

    agg_stats = random_cross_validation(ScaledSVR, results, splits=args.splits, test_fraction=0.2, processes=args.processes)
    print_agg_stats(agg_stats['stats'])

    if args.out_file is not None:
        with open(args.out_file, 'wb') as out_file:
            pkl.dump(agg_stats, out_file)


if __name__ == '__main__':
    main()