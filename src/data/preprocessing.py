"""
Data processing utilities for medical device classification datasets.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.model_selection import train_test_split
import logging

class DataProcessor:
    """
    Handles data loading, preprocessing, and splitting for medical device datasets.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize DataProcessor with configuration.
        
        Args:
            config: Configuration dictionary containing data parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def load_raw_data(self, data_path: str) -> pd.DataFrame:
        """
        Load raw medical device data from specified path.
        
        Args:
            data_path: Path to raw data file
            
        Returns:
            DataFrame containing raw data
        """
        try:
            if data_path.endswith('.csv'):
                data = pd.read_csv(data_path)
            elif data_path.endswith('.json'):
                data = pd.read_json(data_path)
            else:
                raise ValueError(f"Unsupported file format: {data_path}")
                
            self.logger.info(f"Loaded {len(data)} samples from {data_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply preprocessing steps to the data.
        
        Args:
            data: Raw data DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        processed_data = data.copy()
        
        # Handle missing values
        processed_data = processed_data.dropna()
        
        # Normalize text fields
        if 'device_name' in processed_data.columns:
            processed_data['device_name'] = processed_data['device_name'].str.lower().str.strip()
        
        # Encode categorical variables
        if 'category' in processed_data.columns:
            processed_data['category_encoded'] = pd.Categorical(processed_data['category']).codes
            
        self.logger.info(f"Preprocessed data shape: {processed_data.shape}")
        return processed_data
    
    def create_splits(self, data: pd.DataFrame, test_size: float = 0.2, 
                     val_size: float = 0.1, random_state: int = 42) -> Tuple[pd.DataFrame, ...]:
        """
        Create train/validation/test splits.
        
        Args:
            data: Preprocessed data
            test_size: Proportion of test set
            val_size: Proportion of validation set
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        # First split: train+val vs test
        train_val, test = train_test_split(
            data, test_size=test_size, random_state=random_state, 
            stratify=data.get('category_encoded')
        )
        
        # Second split: train vs val
        val_proportion = val_size / (1 - test_size)
        train, val = train_test_split(
            train_val, test_size=val_proportion, random_state=random_state,
            stratify=train_val.get('category_encoded')
        )
        
        self.logger.info(f"Split sizes - Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
        return train, val, test
    
    def save_processed_data(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
                           test_df: pd.DataFrame, output_dir: str):
        """
        Save processed data splits to files.
        
        Args:
            train_df: Training data
            val_df: Validation data  
            test_df: Test data
            output_dir: Output directory path
        """
        os.makedirs(output_dir, exist_ok=True)
        
        train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
        val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)
        test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)
        
        self.logger.info(f"Saved processed data to {output_dir}")

def get_dataset_statistics(data: pd.DataFrame) -> Dict:
    """
    Calculate basic statistics for the dataset.
    
    Args:
        data: Dataset DataFrame
        
    Returns:
        Dictionary containing statistics
    """
    stats = {
        'total_samples': len(data),
        'num_features': len(data.columns),
        'missing_values': data.isnull().sum().sum(),
    }
    
    if 'category' in data.columns:
        stats['num_classes'] = data['category'].nunique()
        stats['class_distribution'] = data['category'].value_counts().to_dict()
    
    return stats