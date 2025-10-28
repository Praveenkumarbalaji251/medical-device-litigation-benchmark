"""
Evaluation metrics and benchmarking tools for medical device classification.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report
)
from typing import Dict, List, Optional, Tuple, Union
import json
import os
import logging
from datetime import datetime

class BenchmarkEvaluator:
    """
    Comprehensive evaluation framework for medical device classification models.
    """
    
    def __init__(self, class_names: Optional[List[str]] = None):
        """
        Initialize evaluator.
        
        Args:
            class_names: List of class names for reporting
        """
        self.class_names = class_names
        self.logger = logging.getLogger(__name__)
        self.results = {}
        
    def evaluate_predictions(self, y_true: np.ndarray, y_pred: np.ndarray, 
                           y_pred_proba: Optional[np.ndarray] = None, 
                           model_name: str = "model") -> Dict:
        """
        Evaluate model predictions with comprehensive metrics.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities (optional)
            model_name: Name of the model being evaluated
            
        Returns:
            Dictionary containing evaluation metrics
        """
        metrics = {}
        
        # Basic classification metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        metrics['precision'] = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        metrics['recall'] = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        metrics['f1_score'] = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Per-class metrics
        precision_per_class = precision_score(y_true, y_pred, average=None, zero_division=0)
        recall_per_class = recall_score(y_true, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_true, y_pred, average=None, zero_division=0)
        
        metrics['per_class_precision'] = precision_per_class.tolist()
        metrics['per_class_recall'] = recall_per_class.tolist()
        metrics['per_class_f1'] = f1_per_class.tolist()
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        # ROC-AUC (if probabilities provided)
        if y_pred_proba is not None:
            try:
                if len(np.unique(y_true)) == 2:  # Binary classification
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
                else:  # Multi-class classification
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba, 
                                                     multi_class='ovr', average='weighted')
            except ValueError as e:
                self.logger.warning(f"Could not calculate ROC-AUC: {e}")
                metrics['roc_auc'] = None
        
        # Classification report
        report = classification_report(y_true, y_pred, target_names=self.class_names, 
                                     output_dict=True, zero_division=0)
        metrics['classification_report'] = report
        
        # Store results
        self.results[model_name] = {
            'metrics': metrics,
            'timestamp': datetime.now().isoformat(),
            'num_samples': len(y_true)
        }
        
        self.logger.info(f"Evaluated {model_name}: Accuracy={metrics['accuracy']:.4f}, "
                        f"F1={metrics['f1_score']:.4f}")
        
        return metrics
    
    def compare_models(self, results_dict: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare multiple models based on their evaluation results.
        
        Args:
            results_dict: Dictionary mapping model names to results
            
        Returns:
            DataFrame with comparison metrics
        """
        comparison_data = []
        
        for model_name, results in results_dict.items():
            metrics = results['metrics']
            row = {
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1-Score': metrics['f1_score'],
                'ROC-AUC': metrics.get('roc_auc', 'N/A'),
                'Samples': results['num_samples']
            }
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        df = df.sort_values('F1-Score', ascending=False)
        
        return df
    
    def calculate_statistical_significance(self, model1_preds: np.ndarray, 
                                         model2_preds: np.ndarray, 
                                         y_true: np.ndarray) -> Dict:
        """
        Calculate statistical significance between two models using McNemar's test.
        
        Args:
            model1_preds: Predictions from model 1
            model2_preds: Predictions from model 2
            y_true: Ground truth labels
            
        Returns:
            Dictionary with statistical test results
        """
        # Create contingency table for McNemar's test
        model1_correct = (model1_preds == y_true)
        model2_correct = (model2_preds == y_true)
        
        # Contingency table: [both_wrong, model1_right_model2_wrong, 
        #                     model1_wrong_model2_right, both_right]
        both_wrong = np.sum(~model1_correct & ~model2_correct)
        model1_only = np.sum(model1_correct & ~model2_correct)
        model2_only = np.sum(~model1_correct & model2_correct)
        both_right = np.sum(model1_correct & model2_correct)
        
        # McNemar's test statistic
        if model1_only + model2_only > 0:
            mcnemar_stat = (abs(model1_only - model2_only) - 1)**2 / (model1_only + model2_only)
        else:
            mcnemar_stat = 0
        
        return {
            'mcnemar_statistic': mcnemar_stat,
            'contingency_table': {
                'both_wrong': both_wrong,
                'model1_only_correct': model1_only,
                'model2_only_correct': model2_only,
                'both_correct': both_right
            },
            'p_value_threshold': 3.841  # Chi-square critical value for p=0.05
        }
    
    def generate_benchmark_report(self, output_path: str, 
                                include_plots: bool = True) -> str:
        """
        Generate comprehensive benchmark report.
        
        Args:
            output_path: Path to save the report
            include_plots: Whether to include visualization plots
            
        Returns:
            Path to generated report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        report_content = self._create_report_content(include_plots)
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"Benchmark report saved to {output_path}")
        return output_path
    
    def save_results(self, output_path: str):
        """
        Save evaluation results to JSON file.
        
        Args:
            output_path: Path to save results
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        self.logger.info(f"Results saved to {output_path}")
    
    def load_results(self, input_path: str):
        """
        Load evaluation results from JSON file.
        
        Args:
            input_path: Path to load results from
        """
        with open(input_path, 'r') as f:
            self.results = json.load(f)
        
        self.logger.info(f"Results loaded from {input_path}")
    
    def _create_report_content(self, include_plots: bool = True) -> str:
        """Create markdown content for benchmark report."""
        content = f"""# Medical Device Classification Benchmark Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

This report presents the evaluation results for medical device classification models.

### Models Evaluated

"""
        
        if self.results:
            comparison_df = self.compare_models(self.results)
            content += comparison_df.to_markdown(index=False)
        else:
            content += "No evaluation results available."
        
        content += """

## Detailed Results

"""
        
        for model_name, results in self.results.items():
            metrics = results['metrics']
            content += f"""
### {model_name}

- **Accuracy**: {metrics['accuracy']:.4f}
- **Precision**: {metrics['precision']:.4f}  
- **Recall**: {metrics['recall']:.4f}
- **F1-Score**: {metrics['f1_score']:.4f}
- **ROC-AUC**: {metrics.get('roc_auc', 'N/A')}
- **Samples**: {results['num_samples']}

"""
        
        return content

def calculate_class_weights(y: np.ndarray) -> np.ndarray:
    """
    Calculate class weights for imbalanced datasets.
    
    Args:
        y: Array of class labels
        
    Returns:
        Array of class weights
    """
    from collections import Counter
    
    class_counts = Counter(y)
    total_samples = len(y)
    num_classes = len(class_counts)
    
    weights = np.zeros(num_classes)
    for class_idx, count in class_counts.items():
        weights[class_idx] = total_samples / (num_classes * count)
    
    return weights