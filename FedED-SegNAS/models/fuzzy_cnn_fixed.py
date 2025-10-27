"""
FIXED Fuzzy CNN Architecture for Epistasis Detection
====================================================

This is an improved version that fixes the vanishing gradient problem
causing 50% accuracy.

Key improvements:
1. Replaced sigmoid with ReLU in conv layers (prevents gradient saturation)
2. Added batch normalization (stabilizes training)
3. Removed defuzzification (preserves information)
4. Improved weight initialization
5. Added gradient clipping in optimizer
6. Better dropout scheduling

Author: FedED-SegNAS Project - FIXED VERSION
Date: October 2024
"""

import tensorflow as tf
from tensorflow.keras import layers, Model
import numpy as np


class FuzzificationLayer(layers.Layer):
    """
    Converts discrete SNP data to fuzzy membership values using Gaussian membership functions.
    IMPROVED: Better initialization for means to match SNP values (0, 1, 2)
    """
    
    def __init__(self, num_fuzzy_sets=3, **kwargs):
        super(FuzzificationLayer, self).__init__(**kwargs)
        self.num_fuzzy_sets = num_fuzzy_sets
    
    def build(self, input_shape):
        # FIXED: Initialize means to match SNP genotypes (0, 1, 2)
        # This gives better starting point for learning
        initial_means = tf.constant([0.0, 1.0, 2.0], dtype=tf.float32)
        self.means = self.add_weight(
            name='means',
            shape=(self.num_fuzzy_sets,),
            initializer=tf.keras.initializers.Constant(initial_means),
            trainable=True
        )
        
        # FIXED: Start with narrower standard deviations for better discrimination
        self.stds = self.add_weight(
            name='stds',
            shape=(self.num_fuzzy_sets,),
            initializer=tf.keras.initializers.Constant(0.5),
            trainable=True
        )
        
        super(FuzzificationLayer, self).build(input_shape)
    
    def call(self, inputs):
        """
        Compute fuzzy membership values using Gaussian membership functions.
        """
        inputs_expanded = tf.expand_dims(inputs, axis=-1)
        means_expanded = tf.reshape(self.means, (1, 1, -1))
        stds_expanded = tf.reshape(self.stds, (1, 1, -1))
        
        # Prevent division by zero with larger epsilon
        stds_expanded = tf.maximum(stds_expanded, 0.1)
        
        # Gaussian membership function
        membership = tf.exp(
            -tf.square(inputs_expanded - means_expanded) / 
            (2 * tf.square(stds_expanded))
        )
        
        return membership


class ImprovedFuzzyConvLayer(layers.Layer):
    """
    FIXED: Convolutional layer with ReLU instead of sigmoid to prevent vanishing gradients.
    Added batch normalization for stability.
    """
    
    def __init__(self, filters, kernel_size, use_batch_norm=True, **kwargs):
        super(ImprovedFuzzyConvLayer, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.use_batch_norm = use_batch_norm
        
        # Batch normalization layer
        if self.use_batch_norm:
            self.batch_norm = layers.BatchNormalization()
    
    def build(self, input_shape):
        # FIXED: Better weight initialization (He initialization for ReLU)
        self.conv_weights = self.add_weight(
            name='conv_weights',
            shape=(self.kernel_size, input_shape[-1], self.filters),
            initializer=tf.keras.initializers.HeNormal(),
            trainable=True
        )
        
        self.bias = self.add_weight(
            name='bias',
            shape=(self.filters,),
            initializer='zeros',
            trainable=True
        )
        
        super(ImprovedFuzzyConvLayer, self).build(input_shape)
    
    def call(self, inputs, training=False):
        """
        FIXED: Use ReLU activation instead of sigmoid to prevent gradient saturation.
        """
        output = tf.nn.conv1d(
            inputs, 
            filters=self.conv_weights, 
            stride=1, 
            padding='SAME'
        )
        
        output = tf.nn.bias_add(output, self.bias)
        
        # Apply batch normalization before activation
        if self.use_batch_norm:
            output = self.batch_norm(output, training=training)
        
        # FIXED: ReLU instead of sigmoid - prevents vanishing gradients
        return tf.nn.relu(output)


class ImprovedFuzzyCNN(Model):
    """
    FIXED Fuzzy CNN Architecture for Epistasis Detection.
    
    Key Improvements:
    - ReLU activations instead of sigmoid (prevents vanishing gradients)
    - Batch normalization (stabilizes training)
    - Removed defuzzification layer (preserves information)
    - Better dropout scheduling
    - Improved architecture design
    """
    
    def __init__(self, num_snps, num_classes=2, **kwargs):
        super(ImprovedFuzzyCNN, self).__init__(**kwargs)
        
        self.num_snps = num_snps
        self.num_classes = num_classes
        
        # Fuzzification with improved initialization
        self.fuzzification = FuzzificationLayer(num_fuzzy_sets=3)
        
        # FIXED: Convolutional blocks with ReLU and BatchNorm
        self.conv1 = ImprovedFuzzyConvLayer(filters=32, kernel_size=3, name='fuzzy_conv1')
        self.pool1 = layers.MaxPooling1D(pool_size=2, name='pool1')
        self.dropout1 = layers.Dropout(0.2, name='dropout1')
        
        self.conv2 = ImprovedFuzzyConvLayer(filters=64, kernel_size=3, name='fuzzy_conv2')
        self.pool2 = layers.MaxPooling1D(pool_size=2, name='pool2')
        self.dropout2 = layers.Dropout(0.3, name='dropout2')
        
        self.conv3 = ImprovedFuzzyConvLayer(filters=128, kernel_size=3, name='fuzzy_conv3')
        self.pool3 = layers.GlobalAveragePooling1D(name='global_pool')  # FIXED: Use global pooling instead of regular pool
        
        # REMOVED: Defuzzification layer - it was losing too much information
        
        # Dense layers with batch normalization
        self.dense1 = layers.Dense(256, name='dense1')
        self.bn1 = layers.BatchNormalization(name='bn1')
        self.act1 = layers.Activation('relu', name='relu1')
        self.dropout3 = layers.Dropout(0.4, name='dropout3')
        
        self.dense2 = layers.Dense(128, name='dense2')
        self.bn2 = layers.BatchNormalization(name='bn2')
        self.act2 = layers.Activation('relu', name='relu2')
        self.dropout4 = layers.Dropout(0.4, name='dropout4')
        
        self.output_layer = layers.Dense(num_classes, activation='softmax', name='output')
    
    def call(self, inputs, training=False):
        """
        Forward pass through the improved Fuzzy CNN.
        """
        # Fuzzification: (batch, snps) -> (batch, snps, 3)
        x = self.fuzzification(inputs)
        
        # Conv Block 1
        x = self.conv1(x, training=training)
        x = self.pool1(x)
        x = self.dropout1(x, training=training)
        
        # Conv Block 2
        x = self.conv2(x, training=training)
        x = self.pool2(x)
        x = self.dropout2(x, training=training)
        
        # Conv Block 3 with global pooling
        x = self.conv3(x, training=training)
        x = self.pool3(x)  # Global average pooling - no flatten needed
        
        # Dense Block 1
        x = self.dense1(x)
        x = self.bn1(x, training=training)
        x = self.act1(x)
        x = self.dropout3(x, training=training)
        
        # Dense Block 2
        x = self.dense2(x)
        x = self.bn2(x, training=training)
        x = self.act2(x)
        x = self.dropout4(x, training=training)
        
        # Output
        return self.output_layer(x)


def build_improved_fuzzy_cnn(num_snps, num_classes=2, learning_rate=0.001):
    """
    Factory function to build and compile the improved Fuzzy CNN model.
    
    FIXED:
    - Added gradient clipping to prevent exploding gradients
    - Better learning rate
    - More metrics for monitoring
    """
    # Create model
    model = ImprovedFuzzyCNN(num_snps=num_snps, num_classes=num_classes)
    
    # Dummy forward pass to build all layers
    dummy_input = tf.random.normal((1, num_snps))
    _ = model(dummy_input, training=False)
    
    # FIXED: Use Adam with gradient clipping
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=learning_rate,
        clipnorm=1.0  # Gradient clipping prevents exploding gradients
    )
    
    # Compile model with more metrics
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall'),
            tf.keras.metrics.AUC(name='auc')
        ]
    )
    
    return model


# Test script
if __name__ == '__main__':
    print("=" * 70)
    print("IMPROVED FUZZY CNN ARCHITECTURE TEST")
    print("=" * 70)
    
    # Test with 50 SNPs
    num_snps = 50
    batch_size = 32
    
    print(f"\nBuilding Improved Fuzzy CNN with {num_snps} SNPs...")
    model = build_improved_fuzzy_cnn(num_snps=num_snps)
    
    print("\n" + "=" * 70)
    print("MODEL SUMMARY")
    print("=" * 70)
    model.summary()
    
    # Test forward pass
    print("\n" + "=" * 70)
    print("TESTING FORWARD PASS")
    print("=" * 70)
    
    # Generate dummy SNP data
    dummy_input = tf.random.uniform((batch_size, num_snps), minval=0, maxval=3, dtype=tf.float32)
    dummy_input = tf.floor(dummy_input)
    
    print(f"Input shape: {dummy_input.shape}")
    print(f"Input range: [{tf.reduce_min(dummy_input).numpy()}, {tf.reduce_max(dummy_input).numpy()}]")
    
    # Forward pass
    output = model(dummy_input, training=False)
    
    print(f"\nOutput shape: {output.shape}")
    print(f"Output range: [{tf.reduce_min(output).numpy():.4f}, {tf.reduce_max(output).numpy():.4f}]")
    print(f"Sum of probabilities (should be ~1.0): {tf.reduce_sum(output[0]).numpy():.4f}")
    
    # Test gradient flow
    print("\n" + "=" * 70)
    print("TESTING GRADIENT FLOW")
    print("=" * 70)
    
    dummy_labels = tf.random.uniform((batch_size,), minval=0, maxval=2, dtype=tf.int32)
    
    with tf.GradientTape() as tape:
        predictions = model(dummy_input, training=True)
        loss = tf.keras.losses.sparse_categorical_crossentropy(dummy_labels, predictions)
        total_loss = tf.reduce_mean(loss)
    
    gradients = tape.gradient(total_loss, model.trainable_variables)
    
    print(f"Loss: {total_loss.numpy():.4f}")
    print("\nGradient statistics (first 5 layers):")
    for i, (var, grad) in enumerate(zip(model.trainable_variables[:5], gradients[:5])):
        if grad is not None:
            print(f"  {var.name:40s}: mean={np.abs(grad.numpy()).mean():.8f}, "
                  f"max={np.abs(grad.numpy()).max():.8f}")
    
    total_params = model.count_params()
    print(f"\n✅ Total parameters: {total_params:,}")
    
    print("\n" + "=" * 70)
    print("✅ IMPROVED FUZZY CNN TEST COMPLETE")
    print("=" * 70)
