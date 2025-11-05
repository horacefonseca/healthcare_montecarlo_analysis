"""
Healthcare Monte Carlo Analysis Package

This package provides tools for generating synthetic healthcare data,
running Monte Carlo simulations, and analyzing treatment outcomes.
"""

__version__ = "1.0.0"
__author__ = "Horace Fonseca"

from .data_generator import HealthcareDataGenerator
from .monte_carlo_simulator import MonteCarloHealthcareSimulator, TreatmentParameters
from .analysis import HealthcareAnalyzer

__all__ = [
    'HealthcareDataGenerator',
    'MonteCarloHealthcareSimulator',
    'TreatmentParameters',
    'HealthcareAnalyzer'
]
