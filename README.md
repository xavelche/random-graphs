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

## Mathematical Background

### Erdős–Rényi Random Graphs (G(n,p))
- **Definition**: A random graph with $ n $ vertices, where each edge appears independently with probability $ p $.
- **Phase Transition**:
  - **Critical threshold**: $ p \approx \frac{1}{n} $.
    - For $ p \ll \frac{1}{n} $: Small disconnected components.
    - For $ p \gg \frac{1}{n} $: Emergence of a giant connected component.
- **Degree Distribution**: For large $ n $, degrees follow a Poisson distribution with mean $ np $.
- **Connectivity**: Sharp threshold at $ p \approx \frac{\log n}{n} $. Above this, the graph is almost surely connected.

#### Suggested Experiments
- Fix $ n=200 $, vary $ p $ between $ 0.001 $ and $ 0.02 $ to observe the phase transition.
- Compare empirical degree distributions with the Poisson($ np $) law.
- Measure the size of the largest component for different values of $ p $.

---

### Galton–Watson Branching Process
- **Definition**: A stochastic process modeling population growth, where each individual produces offspring according to a Poisson($ \lambda $) distribution.
- **Extinction Probability**:
  - $ q = 1 $ if $ \lambda \leq 1 $.
  - $ q < 1 $ if $ \lambda > 1 $.
- **Critical Parameter**: $ \lambda = 1 $ separates subcritical from supercritical regimes.
- **Generation Growth**: Expected population size after $ t $ generations is $ \lambda^t $.

#### Suggested Experiments
- Compare extinction frequencies for $ \lambda = 0.8, 1.0, 1.2 $.
- Observe exponential growth in the supercritical case ($ \lambda > 1 $).
- Estimate extinction probabilities empirically and compare with theory.

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