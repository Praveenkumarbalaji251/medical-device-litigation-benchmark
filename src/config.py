"""
Configuration management for the medical device classification benchmark.
"""

import yaml
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class DataConfig:
    """Data processing configuration."""
    raw_data_path: str
    processed_data_path: str
    train_split: float = 0.7
    val_split: float = 0.15
    test_split: float = 0.15
    random_seed: int = 42
    image_size: tuple = (224, 224)
    augmentation: bool = True
    
@dataclass
class ModelConfig:
    """Model training configuration."""
    model_type: str  # 'mlp', 'cnn', 'transformer'
    num_classes: int
    learning_rate: float = 0.001
    batch_size: int = 32
    num_epochs: int = 100
    early_stopping_patience: int = 10
    weight_decay: float = 1e-4
    
@dataclass
class BenchmarkConfig:
    """Benchmark evaluation configuration."""
    models_to_evaluate: list
    metrics: list
    output_directory: str
    generate_plots: bool = True
    statistical_tests: bool = True

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def save_config(config: Dict[str, Any], config_path: str):
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration for the benchmark.
    
    Returns:
        Default configuration dictionary
    """
    return {
        'data': {
            'raw_data_path': 'data/raw/',
            'processed_data_path': 'data/processed/',
            'train_split': 0.7,
            'val_split': 0.15,
            'test_split': 0.15,
            'random_seed': 42,
            'image_size': [224, 224],
            'augmentation': True
        },
        'models': {
            'mlp': {
                'hidden_dims': [512, 256, 128],
                'dropout': 0.2,
                'learning_rate': 0.001,
                'batch_size': 64
            },
            'cnn': {
                'base_filters': 64,
                'learning_rate': 0.0001,
                'batch_size': 32
            },
            'transformer': {
                'embed_dim': 256,
                'num_heads': 8,
                'num_layers': 4,
                'learning_rate': 0.0001,
                'batch_size': 16
            }
        },
        'training': {
            'num_epochs': 100,
            'early_stopping_patience': 10,
            'weight_decay': 1e-4,
            'save_best_model': True
        },
        'benchmark': {
            'metrics': ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc'],
            'output_directory': 'benchmarks/',
            'generate_plots': True,
            'statistical_tests': True
        }
    }