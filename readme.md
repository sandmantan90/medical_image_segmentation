
# Medical Image Segmentation Pipeline

A comprehensive pipeline for medical CT image segmentation using TotalSegmentator, featuring 3D data augmentation, orientation correction, and segmentation quality evaluation.

## Overview

This pipeline provides an end-to-end solution for processing and analyzing CT scans, with a focus on:
- Automated segmentation using TotalSegmentator
- Advanced 3D data augmentation techniques
- Quality assessment through Dice score metrics
- Orientation correction for optimal alignment

## Quick Start

### Prerequisites

- Python 3.7+
- TotalSegmentator (follow [official installation guide](https://github.com/wasserth/TotalSegmentator))

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

1. Configure your settings in `config.yml`:
```yaml
CT_PATH: "path/to/dataset"
OUTPUT_DIRECTORY: "path/to/output"
TASK: "total"
```

2. Run the pipeline:
```bash
python main.py
```

## Features

### 🔍 Segmentation
- Automated processing of CT scans using TotalSegmentator
- Support for multiple segmentation tasks
- Batch processing capabilities

### 🔄 Data Augmentation
- Noise injection
- Gaussian blur (simulating breathing artifacts)
- Resolution downsampling
- Customizable augmentation parameters

### 📊 Quality Assessment
- Dice score calculation
- Automated evaluation of augmentation effects
- Performance metrics tracking

### 🔧 Utilities
- Orientation correction for misaligned scans
- Modular architecture for easy extension
- Comprehensive logging

## Project Structure

```
├── main.py             # Pipeline entry point
├── augment.py          # Data augmentation module
├── change_orientation.py    # Orientation correction utilities
├── experiment.py       # Experimental analysis scripts
├── segmentation.py     # TotalSegmentator wrapper
├── utils.py           # Helper functions
└── config.yml         # Configuration settings
```

## Running Experiments

The pipeline includes an experimental framework for analyzing segmentation quality:

```bash
python experiment.py
```

This will:
1. Generate augmented datasets with varying parameters
2. Perform segmentation on each variant
3. Calculate and compare Dice scores
4. Generate visualization plots

## Configuration Options

Key settings in `config.yml`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| CT_PATH | Input dataset location | required |
| OUTPUT_DIRECTORY | Results storage path | required |
| TASK | Segmentation task type | "total" |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TotalSegmentator team for their excellent segmentation tool
- Contributors and maintainers of the project

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Contact the maintainers

---
*Note: This project is under active development. Features and APIs may change.*
