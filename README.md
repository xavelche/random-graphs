# Random Graphs Visualizer

An interactive exploration of **Erdős–Rényi random graphs** and **Galton–Watson branching processes**.

---

## Overview

This project provides a clean, interactive exploration of classical random graph models, designed for clarity and educational purposes.

### Features
- **Erdős–Rényi G(n,p) model**: Random graphs with independent edge probabilities.
- **Galton–Watson trees**: Branching processes for population dynamics.
- **Interactive visualization**: Generate new realizations with a single click.

---

## Quick Start

### Installation
```bash
git clone https://github.com/yourusername/random-graphs-visualizer.git
cd random-graphs-visualizer
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Visualizer
```bash
python main.py
```

---

## Usage

### Command Line Interface
```bash
# Erdős–Rényi graphs
python main.py --model er --nodes 50 --prob 0.1

# Galton–Watson trees
python main.py --model gw --lambda 1.2 --generations 8
```

### Python API
```python
from visualization import visualize_erdos_renyi, visualize_galton_watson

# Interactive Erdős–Rényi visualization
visualize_erdos_renyi(n=100, p=0.05)

# Interactive Galton–Watson tree
visualize_galton_watson(lam=0.8, max_gen=10)
```

---

## Project Structure

```
random-graphs-visualizer/
├── README.md
├── requirements.txt
├── main.py              # CLI interface
├── graphs.py            # Graph generation algorithms
├── visualization.py     # Visualization classes
├── demo.ipynb           # Some examples
└── examples/            # Sample outputs
```