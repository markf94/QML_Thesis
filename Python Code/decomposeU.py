"""
Quantum Gate Decomposition Algorithm

This module implements the decomposition of 2x2 unitary matrices into elementary quantum gates
using the ZYZ (or Euler) decomposition method. The decomposition expresses any 2x2 unitary
matrix in terms of rotation angles (alpha, beta, gamma, delta).

The implementation uses numerical optimization to find the angles that reproduce the target
unitary matrix within specified precision.
"""

from typing import Tuple, Optional, List, Callable
import numpy as np
import cmath
from dataclasses import dataclass
from mpmath import findroot
from functools import partial

@dataclass
class UnitaryMatrix:
    """Represents a 2x2 unitary matrix with its elements."""
    u00: complex
    u01: complex
    u10: complex
    u11: complex

    def validate(self) -> bool:
        """
        Validates if the matrix is approximately unitary within numerical precision.
        Returns True if valid, False otherwise.
        """
        # Create numpy matrix for easier computation
        matrix = np.array([[self.u00, self.u01], 
                          [self.u10, self.u11]], dtype=complex)
        # Check if U†U ≈ I
        product = matrix.conj().T @ matrix
        identity = np.eye(2, dtype=complex)
        return np.allclose(product, identity, atol=1e-6)

@dataclass
class DecompositionAngles:
    """Stores the angles from the ZYZ decomposition."""
    alpha: float
    beta: float
    gamma: float
    delta: float

class GateDecomposer:
    def __init__(self, matrix: UnitaryMatrix, precision: float = 1e-6):
        """
        Initialize decomposer with target unitary matrix and desired precision.
        
        Args:
            matrix: Target unitary matrix to decompose
            precision: Numerical precision for optimization
        """
        if not matrix.validate():
            raise ValueError("Input matrix must be unitary")
        self.matrix = matrix
        self.precision = precision
        self.search_points = np.linspace(-2*np.pi, 2*np.pi, 20)

    def _create_beta_delta_equations(self) -> Tuple[Callable, Callable]:
        """Creates the equations for finding beta and delta angles."""
        def eq1(beta: float, delta: float) -> complex:
            return cmath.exp(1j*(beta+delta)) - self.matrix.u11/self.matrix.u00

        def eq2(beta: float, delta: float) -> complex:
            return cmath.exp(1j*(beta-delta)) + self.matrix.u10/self.matrix.u01

        return eq1, eq2

    def _create_alpha_gamma_equations(self, beta: float, delta: float) -> Tuple[Callable, Callable]:
        """Creates the equations for finding alpha and gamma angles."""
        def eq3(alpha: float, gamma: float) -> complex:
            return (self.matrix.u11 * cmath.exp(-1j*alpha) * 
                   cmath.exp(1j*(-beta/2-delta/2)) - cmath.cos(gamma/2))

        def eq4(alpha: float, gamma: float) -> complex:
            return (self.matrix.u10 * cmath.exp(-1j*alpha) * 
                   cmath.exp(1j*(-beta/2+delta/2)) - cmath.sin(gamma/2))

        return eq3, eq4

    def _find_minimum_magnitude_solution(self, 
                                      equations: Tuple[Callable, Callable],
                                      current_best: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        """
        Finds the solution with minimum magnitude angles using multiple starting points.
        """
        best_solution = current_best
        min_magnitude = sum(abs(x) for x in current_best)

        for x, y in np.ndindex(len(self.search_points), len(self.search_points)):
            try:
                start_point = (self.search_points[x], self.search_points[y])
                solution = findroot(equations, start_point)
                solution_real = (float(solution[0].real), float(solution[1].real))
                
                magnitude = sum(abs(x) for x in solution_real)
                if magnitude < min_magnitude:
                    min_magnitude = magnitude
                    best_solution = solution_real
                    
            except (ZeroDivisionError, OverflowError, ValueError):
                continue

        return best_solution if min_magnitude < sum(abs(x) for x in current_best) else None

    def decompose(self) -> Optional[DecompositionAngles]:
        """
        Performs the ZYZ decomposition of the unitary matrix.
        
        Returns:
            DecompositionAngles object containing the decomposition angles,
            or None if decomposition fails
        """
        # Handle special case where matrix has zero elements
        if abs(self.matrix.u10) < self.precision or abs(self.matrix.u01) < self.precision:
            return self._handle_special_case()

        # Find beta and delta
        beta_delta_eqs = self._create_beta_delta_equations()
        initial_angles = (10.0, 10.0)  # Large initial values
        beta_delta = self._find_minimum_magnitude_solution(beta_delta_eqs, initial_angles)
        
        if not beta_delta:
            return None
            
        beta, delta = beta_delta

        # Find alpha and gamma
        alpha_gamma_eqs = self._create_alpha_gamma_equations(beta, delta)
        alpha_gamma = self._find_minimum_magnitude_solution(alpha_gamma_eqs, initial_angles)
        
        if not alpha_gamma:
            return None
            
        alpha, gamma = alpha_gamma

        return DecompositionAngles(alpha=alpha, beta=beta, gamma=gamma, delta=delta)

    def verify_decomposition(self, angles: DecompositionAngles) -> bool:
        """
        Verifies if the decomposition accurately reproduces the original matrix.
        """
        reconstructed = self.reconstruct_matrix(angles)
        original = np.array([[self.matrix.u00, self.matrix.u01],
                           [self.matrix.u10, self.matrix.u11]])
        return np.allclose(reconstructed, original, atol=self.precision)

    @staticmethod
    def reconstruct_matrix(angles: DecompositionAngles) -> np.ndarray:
        """
        Reconstructs the unitary matrix from decomposition angles.
        """
        alpha, beta, gamma, delta = angles.alpha, angles.beta, angles.gamma, angles.delta
        
        nu00 = cmath.exp(1j*(alpha-beta/2-delta/2)) * cmath.cos(gamma/2)
        nu01 = -cmath.exp(1j*(alpha-beta/2+delta/2)) * cmath.sin(gamma/2)
        nu10 = cmath.exp(1j*(alpha+beta/2-delta/2)) * cmath.sin(gamma/2)
        nu11 = cmath.exp(1j*(alpha+beta/2+delta/2)) * cmath.cos(gamma/2)
        
        return np.array([[nu00, nu01], [nu10, nu11]])

def main():
    # Example usage with Hadamard-like matrix
    hadamard = UnitaryMatrix(
        u00=0.19509,
        u01=-0.98079,
        u10=0.98079,
        u11=0.19509
    )
    
    decomposer = GateDecomposer(hadamard)
    angles = decomposer.decompose()
    
    if angles:
        print(f"Decomposition angles found:")
        print(f"α = {angles.alpha:.6f}")
        print(f"β = {angles.beta:.6f}")
        print(f"γ = {angles.gamma:.6f}")
        print(f"δ = {angles.delta:.6f}")
        
        if decomposer.verify_decomposition(angles):
            print("\nDecomposition verified successfully!")
        else:
            print("\nWarning: Decomposition verification failed")
    else:
        print("Failed to find valid decomposition")

if __name__ == "__main__":
    main()
