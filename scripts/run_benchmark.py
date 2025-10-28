#!/usr/bin/env python3
"""
Script for running benchmark evaluation on trained models.
"""

import argparse
import logging
import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from evaluation.metrics import BenchmarkEvaluator
from config import load_config, get_default_config

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/benchmark.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_predictions(predictions_path: str):
    """Load model predictions from file."""
    if predictions_path.endswith('.json'):
        with open(predictions_path, 'r') as f:
            data = json.load(f)
    elif predictions_path.endswith('.csv'):
        data = pd.read_csv(predictions_path).to_dict('records')
    else:
        raise ValueError(f"Unsupported file format: {predictions_path}")
    
    return data

def main():
    """Main function for benchmark evaluation."""
    parser = argparse.ArgumentParser(description="Run medical device classification benchmark")
    parser.add_argument("--config", type=str, default="config/default_config.yaml",
                       help="Path to configuration file")
    parser.add_argument("--predictions-dir", type=str, required=True,
                       help="Directory containing model predictions")
    parser.add_argument("--ground-truth", type=str, required=True,
                       help="Path to ground truth labels file")
    parser.add_argument("--output-dir", type=str, default="benchmarks",
                       help="Output directory for benchmark results")
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
        
        # Load ground truth
        logger.info(f"Loading ground truth from {args.ground_truth}")
        if args.ground_truth.endswith('.csv'):
            gt_df = pd.read_csv(args.ground_truth)
            y_true = gt_df['label'].values if 'label' in gt_df.columns else gt_df.iloc[:, -1].values
        else:
            raise ValueError(f"Unsupported ground truth format: {args.ground_truth}")
        
        # Get class names if available
        class_names = config.get('device_categories', None)
        
        # Initialize evaluator
        evaluator = BenchmarkEvaluator(class_names=class_names)
        
        # Find all prediction files
        predictions_dir = Path(args.predictions_dir)
        prediction_files = list(predictions_dir.glob("*.json")) + list(predictions_dir.glob("*.csv"))
        
        if not prediction_files:
            raise ValueError(f"No prediction files found in {args.predictions_dir}")
        
        logger.info(f"Found {len(prediction_files)} prediction files")
        
        # Evaluate each model
        all_results = {}
        for pred_file in prediction_files:
            model_name = pred_file.stem
            logger.info(f"Evaluating model: {model_name}")
            
            # Load predictions
            pred_data = load_predictions(str(pred_file))
            
            # Extract predictions and probabilities
            if isinstance(pred_data, list) and len(pred_data) > 0:
                if 'predictions' in pred_data[0]:
                    y_pred = np.array([item['predictions'] for item in pred_data])
                    y_pred_proba = np.array([item.get('probabilities', None) for item in pred_data])
                    y_pred_proba = y_pred_proba if y_pred_proba[0] is not None else None
                else:
                    y_pred = np.array(pred_data)
                    y_pred_proba = None
            else:
                logger.error(f"Invalid prediction format in {pred_file}")
                continue
            
            # Evaluate model
            metrics = evaluator.evaluate_predictions(
                y_true=y_true,
                y_pred=y_pred, 
                y_pred_proba=y_pred_proba,
                model_name=model_name
            )
            
            all_results[model_name] = {
                'metrics': metrics,
                'num_samples': len(y_true)
            }
        
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Generate comparison report
        logger.info("Generating benchmark comparison...")
        comparison_df = evaluator.compare_models(evaluator.results)
        print("\\nBenchmark Results:")
        print(comparison_df.to_string(index=False))
        
        # Save results
        results_path = os.path.join(args.output_dir, "benchmark_results.json")
        evaluator.save_results(results_path)
        
        # Save comparison table
        comparison_path = os.path.join(args.output_dir, "model_comparison.csv")
        comparison_df.to_csv(comparison_path, index=False)
        
        # Generate detailed report
        report_path = os.path.join(args.output_dir, "benchmark_report.md")
        evaluator.generate_benchmark_report(report_path, include_plots=True)
        
        logger.info(f"Benchmark evaluation completed! Results saved to {args.output_dir}")
        
    except Exception as e:
        logger.error(f"Error during benchmark evaluation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()