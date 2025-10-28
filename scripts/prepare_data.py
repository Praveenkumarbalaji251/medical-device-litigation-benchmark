#!/usr/bin/env python3
"""
Main script for preparing the medical device classification dataset.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.preprocessing import DataProcessor, get_dataset_statistics
from config import load_config, get_default_config

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/data_preparation.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main function for data preparation."""
    parser = argparse.ArgumentParser(description="Prepare medical device dataset")
    parser.add_argument("--config", type=str, default="config/default_config.yaml",
                       help="Path to configuration file")
    parser.add_argument("--input", type=str, required=True,
                       help="Path to raw data file")
    parser.add_argument("--output", type=str, default="data/processed",
                       help="Output directory for processed data")
    parser.add_argument("--log-level", type=str, default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    os.makedirs("logs", exist_ok=True)
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        if os.path.exists(args.config):
            config = load_config(args.config)
            logger.info(f"Loaded configuration from {args.config}")
        else:
            config = get_default_config()
            logger.warning(f"Configuration file {args.config} not found. Using defaults.")
        
        # Initialize data processor
        data_config = config.get('data', {})
        processor = DataProcessor(data_config)
        
        # Load raw data
        logger.info(f"Loading raw data from {args.input}")
        raw_data = processor.load_raw_data(args.input)
        
        # Calculate and log statistics
        stats = get_dataset_statistics(raw_data)
        logger.info(f"Dataset statistics: {stats}")
        
        # Preprocess data
        logger.info("Preprocessing data...")
        processed_data = processor.preprocess_data(raw_data)
        
        # Create train/val/test splits
        logger.info("Creating data splits...")
        train_data, val_data, test_data = processor.create_splits(
            processed_data,
            test_size=data_config.get('test_split', 0.15),
            val_size=data_config.get('val_split', 0.15),
            random_state=data_config.get('random_seed', 42)
        )
        
        # Save processed data
        logger.info(f"Saving processed data to {args.output}")
        processor.save_processed_data(train_data, val_data, test_data, args.output)
        
        # Save split statistics
        split_stats = {
            'train': get_dataset_statistics(train_data),
            'validation': get_dataset_statistics(val_data),
            'test': get_dataset_statistics(test_data)
        }
        
        logger.info("Data preparation completed successfully!")
        logger.info(f"Split statistics: {split_stats}")
        
    except Exception as e:
        logger.error(f"Error during data preparation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()