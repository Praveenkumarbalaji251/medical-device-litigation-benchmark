"""
Base model classes for medical device classification.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
import logging

class BaseClassifier(ABC, nn.Module):
    """
    Abstract base class for medical device classifiers.
    """
    
    def __init__(self, num_classes: int, input_dim: int):
        """
        Initialize base classifier.
        
        Args:
            num_classes: Number of device categories
            input_dim: Input feature dimension
        """
        super().__init__()
        self.num_classes = num_classes
        self.input_dim = input_dim
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model."""
        pass
    
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """
        Make predictions on input data.
        
        Args:
            x: Input tensor
            
        Returns:
            Predicted class probabilities
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
        return probs
    
    def get_model_info(self) -> Dict:
        """Get model information and parameters."""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            'model_name': self.__class__.__name__,
            'num_classes': self.num_classes,
            'input_dim': self.input_dim,
            'total_parameters': total_params,
            'trainable_parameters': trainable_params
        }

class MLPClassifier(BaseClassifier):
    """
    Multi-layer perceptron classifier for medical device features.
    """
    
    def __init__(self, num_classes: int, input_dim: int, 
                 hidden_dims: List[int] = [512, 256, 128],
                 dropout: float = 0.2):
        """
        Initialize MLP classifier.
        
        Args:
            num_classes: Number of device categories
            input_dim: Input feature dimension
            hidden_dims: List of hidden layer dimensions
            dropout: Dropout probability
        """
        super().__init__(num_classes, input_dim)
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_classes))
        self.classifier = nn.Sequential(*layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through MLP."""
        return self.classifier(x)

class CNNClassifier(BaseClassifier):
    """
    Convolutional neural network for medical device image classification.
    """
    
    def __init__(self, num_classes: int, input_channels: int = 3,
                 base_filters: int = 64):
        """
        Initialize CNN classifier.
        
        Args:
            num_classes: Number of device categories
            input_channels: Number of input channels (e.g., 3 for RGB)
            base_filters: Base number of convolutional filters
        """
        super().__init__(num_classes, input_channels)
        
        self.conv_layers = nn.Sequential(
            # First conv block
            nn.Conv2d(input_channels, base_filters, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(base_filters),
            nn.MaxPool2d(2, 2),
            
            # Second conv block
            nn.Conv2d(base_filters, base_filters*2, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(base_filters*2),
            nn.MaxPool2d(2, 2),
            
            # Third conv block
            nn.Conv2d(base_filters*2, base_filters*4, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(base_filters*4),
            nn.MaxPool2d(2, 2),
        )
        
        # Adaptive pooling to handle variable input sizes
        self.adaptive_pool = nn.AdaptiveAvgPool2d((7, 7))
        
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(base_filters*4 * 7 * 7, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through CNN."""
        x = self.conv_layers(x)
        x = self.adaptive_pool(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.classifier(x)
        return x

class TransformerClassifier(BaseClassifier):
    """
    Transformer-based classifier for sequential medical device data.
    """
    
    def __init__(self, num_classes: int, vocab_size: int, 
                 embed_dim: int = 256, num_heads: int = 8, 
                 num_layers: int = 4, max_seq_len: int = 512):
        """
        Initialize Transformer classifier.
        
        Args:
            num_classes: Number of device categories
            vocab_size: Vocabulary size for embeddings
            embed_dim: Embedding dimension
            num_heads: Number of attention heads
            num_layers: Number of transformer layers
            max_seq_len: Maximum sequence length
        """
        super().__init__(num_classes, vocab_size)
        
        self.embed_dim = embed_dim
        self.max_seq_len = max_seq_len
        
        # Embedding layers
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_seq_len, embed_dim)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, 
            dim_feedforward=embed_dim*4, dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(embed_dim, embed_dim//2),
            nn.ReLU(),
            nn.Linear(embed_dim//2, num_classes)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through Transformer."""
        seq_len = x.size(1)
        
        # Create embeddings
        token_emb = self.token_embedding(x)
        pos_emb = self.position_embedding(torch.arange(seq_len, device=x.device))
        x = token_emb + pos_emb.unsqueeze(0)
        
        # Transformer forward (expects seq_len x batch_size x embed_dim)
        x = x.transpose(0, 1)
        x = self.transformer(x)
        
        # Global average pooling
        x = x.mean(dim=0)
        
        # Classification
        return self.classifier(x)