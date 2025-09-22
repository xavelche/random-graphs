#!/usr/bin/env python3
"""
Random Graph Visualizer

Interactive terminal program for generating and visualizing random graphs
with both menu-driven and command-line interfaces.
"""

import sys
import argparse
from typing import Optional
from visualization import visualize_erdos_renyi, visualize_galton_watson


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate and visualize random graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py --model er --nodes 100 --prob 0.05
  python main.py --model gw --lambda 1.2 --generations 8
        """
    )
    
    parser.add_argument(
        "--model", 
        choices=["er", "gw"], 
        help="Graph model: 'er' for Erdős–Rényi, 'gw' for Galton–Watson"
    )
    
    # Erdős–Rényi parameters
    parser.add_argument(
        "--nodes", "-n", 
        type=int, 
        help="Number of nodes for Erdős–Rényi model"
    )
    parser.add_argument(
        "--prob", "-p", 
        type=float, 
        help="Edge probability for Erdős–Rényi model (0-1)"
    )
    
    # Galton–Watson parameters
    parser.add_argument(
        "--lambda", "-l", 
        dest="lam",
        type=float, 
        help="Poisson parameter λ for Galton–Watson model"
    )
    parser.add_argument(
        "--generations", "-g", 
        type=int, 
        help="Maximum generations for Galton–Watson model"
    )
    
    return parser


def validate_erdos_renyi_params(n: Optional[int], p: Optional[float]) -> tuple[int, float]:
    """Validate and prompt for Erdős–Rényi parameters."""
    if n is None:
        while True:
            try:
                n = int(input("Enter number of nodes (n, max 500): "))
                if n <= 0:
                    print("Number of nodes must be positive.")
                    continue
                if n > 500:
                    print("Too many nodes! Maximum is 500 for good visualization.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
    
    if p is None:
        while True:
            try:
                p = float(input("Enter edge probability (p, 0-1): "))
                if 0 <= p <= 1:
                    break
                else:
                    print("Probability must be between 0 and 1.")
            except ValueError:
                print("Please enter a valid number.")
    
    # Validate ranges
    if not (1 <= n <= 500):
        raise ValueError(f"Number of nodes must be between 1 and 500, got {n}")
    if not (0 <= p <= 1):
        raise ValueError(f"Edge probability must be between 0 and 1, got {p}")
    
    return n, p


def validate_galton_watson_params(lam: Optional[float], max_gen: Optional[int]) -> tuple[float, int]:
    """Validate and prompt for Galton–Watson parameters."""
    if lam is None:
        while True:
            try:
                lam = float(input("Enter Poisson parameter λ (offspring rate): "))
                if lam > 0:
                    break
                else:
                    print("Lambda must be positive.")
            except ValueError:
                print("Please enter a valid number.")
    
    if max_gen is None:
        while True:
            try:
                max_gen = int(input("Enter maximum generations: "))
                if max_gen > 0:
                    break
                else:
                    print("Maximum generations must be positive.")
            except ValueError:
                print("Please enter a valid integer.")
    
    # Validate ranges
    if lam <= 0:
        raise ValueError(f"Lambda must be positive, got {lam}")
    if max_gen <= 0:
        raise ValueError(f"Maximum generations must be positive, got {max_gen}")
    
    return lam, max_gen


def get_user_input() -> int:
    """Display menu and get user's choice."""
    print("\n" + "="*60)
    print("              RANDOM GRAPH VISUALIZER")
    print("="*60)
    print("Choose a random graph model to explore:")
    print()
    print("1. Erdős–Rényi G(n,p) random graphs")
    print("   • Study phase transitions and degree distributions")
    print("   • Observe giant component emergence")
    print()
    print("2. Galton–Watson branching trees")
    print("   • Explore extinction vs explosion dynamics")
    print("   • Visualize population growth patterns")
    print()
    print("3. Exit")
    print("-"*60)
    
    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")


def erdos_renyi_mode(n: Optional[int] = None, p: Optional[float] = None) -> None:
    """Handle Erdős–Rényi graph generation mode."""
    print("\n--- Erdős–Rényi Random Graphs G(n,p) ---")
    print("Mathematical insight: Watch for phase transition around p ≈ 1/n")
    print()
    
    n, p = validate_erdos_renyi_params(n, p)
    
    # Provide mathematical context
    critical_p = 1.0 / n if n > 0 else 0
    expected_degree = (n - 1) * p
    
    print(f"\nGenerating G({n}, {p:.3f})")
    print(f"• Critical threshold: around p ≈ 1/n = {critical_p:.4f}")
    print(f"• Expected degree: {expected_degree:.2f}")

    if p > 2 * critical_p:
        print("• Connectivity regime: edges are dense enough that large clusters are likely")
    elif p < 0.5 * critical_p:
        print("• Connectivity regime: only small clusters are expected")
    else:
        print("• Connectivity regime: near the critical point (interesting fluctuations)")
    
    print("\nClick anywhere on the figure to generate new graphs...")
    visualize_erdos_renyi(n, p)


def galton_watson_mode(lam: Optional[float] = None, max_gen: Optional[int] = None) -> None:
    """Handle Galton–Watson tree generation mode."""
    print("\n--- Galton–Watson Branching Process ---")
    print("Mathematical insight: Critical parameter λ = 1 separates extinction/explosion")
    print()
    
    lam, max_gen = validate_galton_watson_params(lam, max_gen)
    
    # Provide mathematical context
    if lam < 1:
        extinction_prob = 1.0
        regime = "Subcritical (certain extinction)"
    elif lam == 1:
        extinction_prob = 1.0
        regime = "Critical (certain extinction, slow decay)"
    else:
        # For Poisson(λ), extinction probability is smallest positive root of s = e^{λ(s-1)}
        # Approximation for λ > 1: q ≈ 2(λ-1)/λ² for λ close to 1
        if lam < 2:
            extinction_prob = 2 * (lam - 1) / (lam * lam)
        else:
            extinction_prob = 0.1  # Very rough approximation
        regime = "Supercritical (possible survival)"
    
    print(f"\nGenerating tree with λ = {lam:.2f}, max {max_gen} generations")
    print(f"• Regime: {regime}")
    print(f"• Extinction probability: ~{extinction_prob:.3f}")
    print(f"• Expected growth rate: λᵗ = {lam:.2f}ᵗ")
    
    print("\nClick on the figure to generate new trees...")
    visualize_galton_watson(lam, max_gen)


def main() -> None:
    """Main program entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Command line mode
    if args.model:
        try:
            if args.model == "er":
                erdos_renyi_mode(args.nodes, args.prob)
            elif args.model == "gw":
                galton_watson_mode(args.lam, args.generations)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        return
    
    # Interactive menu mode
    try:
        while True:
            choice = get_user_input()
            
            if choice == 1:
                erdos_renyi_mode()
            elif choice == 2:
                galton_watson_mode()
            elif choice == 3:
                print("\nGoodbye!")
                sys.exit(0)
            
            # Ask if user wants to continue
            print("\n" + "-"*60)
            continue_choice = input("Return to main menu? (y/n): ").lower().strip()
            if continue_choice not in ['y', 'yes', '']:
                print("Goodbye!")
                sys.exit(0)
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()