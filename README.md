# FUNQUE+: Efficient Full-Reference Quality Modeling
This repository contains the official implementation of the FUNQUE and FUNQUE+ suite of models proposed in the following papers.

1. A. K. Venkataramanan, C. Stejerean and A. C. Bovik, "FUNQUE: Fusion of Unified Quality Evaluators," 2022 IEEE International Conference on Image Processing (ICIP), Bordeaux, France, 2022, pp. 2147-2151, doi: 10.1109/ICIP46576.2022.9897312.
2. A. K. Venkataramanan, C. Stejerean, I. Katsavounidis, and A. C. Bovik, "One Transform To Compute Them All: Efficient Fusion-Based Full-Reference Video Quality Assessment," arXiv preprint arXiv:2304.03412 (2023)

These models have been shown to be strong alternatives to SOTA quality models such as VMAF, promising greater accuracy at a fraction of the computational cost. For more details, refer to our [arXiv preprint](https://arxiv.org/abs/2304.03412)!

## Features of FUNQUE+
1. An efficient unified transform used by all atom quality models to introduce sensitivity to human perception while maximizing computation sharing.

2. Using the Self-Adaptive Scale Transform (SAST) to rescale videos prior to quality assessment.

3. Computing Multi-Scale Enhanced SSIM directly from wavelet coefficients.

## Accuracy and Efficiency of FUNQUE+
The FUNQUE and FUNQUE+ models offer the best performance, both in terms of accuracy and efficiency! 

*Note: running speeds were measured using comparable implementations in Python over 150 1080p frames on an Intel Core i7-8700 CPU having a clock frequency of 3.2GHz.*

| Model | Test Performance | Running Speed (FPS)
| ---------- | ------- | ---------
|MS-SSIM | 0.7849 | 3.46
|VMAF | 0.8312 | 1.78
|Enhanced VMAF | 0.8377 | 0.20
|__FUNQUE__ | __0.8409__ | __10.88__
|__Y-FUNQUE+__ | __0.8660__ | __19.53__
|__3C-FUNQUE+__ | __0.8754__ | __6.83__

## Usage
### Setting up the environment
Create and activate a virtual environment using
```
python3 -m virtualenv .venv
source .venv/bin/activate
```
Install all required dependencies
```
python3 -m pip install 
```
### Extract features from one video pair
To compute features from one video pair for either the FUNQUE(+) models or the baseline models, use the command

```
python3 extract_features.py --ref_video <path to reference video> --dis_video <path to distorted video> --fex_name <name of feature extractor>
```

Refer to the `NAME` attributes of feature extractors defined in [funque_plus/feature_extractors](https://github.com/abhinaukumar/funque_plus/tree/main/funque_plus/feature_extractors) for the names of various feature extractors. For example, the name of the FUNQUE, Y-FUNQUE+, and 3C-FUNQUE+ feature extractors are `FUNQUE_fex`, `Y_FUNQUE_Plus_fex`, and `3C_FUNQUE_Plus_fex` respectively.

For more options, run
```
python3 extract_features.py --help
```

### Extract features for all videos in a dataset
First, define a subjective dataset file using the same format as those in [datasets/](https://github.com/abhinaukumar/funque_plus/tree/main/datasets). Then, run
```
python3 extract_features_from_dataset.py --dataset <path to dataset file> --fex_name <name of feature extractor> --processes <number of parallel processes to use>
```
*Note: This command computes features and saves the results to disk. It does __not__ print any features. Saved features may be used for downstream tasks - example below*

### Run cross-validation
To evaluate features using content-separated random cross-validation, run
```
python3 crossval_features_on_dataset.py --dataset <path to dataset file> --fex_name <name of feature extractor> --splits <number of random train-test splits> --processes <number of parallel processes to use>
```

*Note: This command may be run without running `extract_features_from_dataset.py` first. In that case, features will be extracted and saved first, before performing cross-validation*

This script is an example of down-stream tasks that can be performed easily after feature extraction.

## References
[1] [https://www.github.com/Netflix/vmaf](https://www.github.com/Netflix/vmaf).

[2] K. Gu, G. Zhai, X. Yang and W. Zhang, "Self-adaptive scale transform for IQA metric," 2013 IEEE International Symposium on Circuits and Systems (ISCAS), Beijing, 2013, pp. 2365-2368, doi: 10.1109/ISCAS.2013.6572353.

[3] A. K. Venkataramanan, C. Wu, A. C. Bovik, I. Katsavounidis and Z. Shahid, "A Hitchhiker’s Guide to Structural Similarity," in IEEE Access, vol. 9, pp. 28872-28896, 2021, doi: 10.1109/ACCESS.2021.3056504.

[4] [https://www.github.com/utlive/enhanced_ssim](https://www.github.com/utlive/enhanced_ssim).

[5] F. Zhang, A. Katsenou, C. Bampis, L. Krasula, Z. Li and D. Bull, "Enhancing VMAF through New Feature Integration and Model Combination," 2021 Picture Coding Symposium (PCS), 2021, pp. 1-5, doi: 10.1109/PCS50896.2021.9477458.