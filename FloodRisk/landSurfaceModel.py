import numpy as np
import tensorflow as tf
from tensorflow import keras
layers = tf.keras.layers

# Generate synthetic data for training PINN
np.random.seed(42)
num_pinn_points = 100
x_pinn_data = np.sort(5 * np.random.rand(num_pinn_points)).reshape(-1, 1)
y_pinn_data = np.sin(x_pinn_data) + 0.1 * np.random.randn(num_pinn_points, 1)

# Land surface modeling parameters
initial_soil_moisture = 0.5
rainfall_rate = 0.02
evaporation_rate = 0.01

# Land surface model simulation
def land_surface_model(time_steps):
    soil_moisture = [initial_soil_moisture]
    for _ in range(1, time_steps):
        # Update soil moisture based on precipitation and evaporation
        precipitation = rainfall_rate + 0.005 * np.random.randn()  # Simulated rainfall
        evaporation = evaporation_rate
        delta_soil_moisture = precipitation - evaporation
        soil_moisture.append(soil_moisture[-1] + delta_soil_moisture)
    return np.array(soil_moisture)

# Generate synthetic data for training land surface model
num_lsm_points = 50
x_lsm_data = np.sort(5 * np.random.rand(num_lsm_points)).reshape(-1, 1)
y_lsm_data = land_surface_model(num_lsm_points).reshape(-1, 1)

# PINN model with modified activation function and normalization
class PINNModel(tf.keras.Model):
    def __init__(self):
        super(PINNModel, self).__init__()
        self.dense1 = layers.Dense(50, activation='relu', input_shape=(1,))
        self.dense2 = layers.Dense(50, activation='relu')
        self.dense3 = layers.Dense(1, activation=None)

    def call(self, x):
        # Normalize input
        x_normalized = (x - tf.reduce_mean(x)) / tf.math.reduce_std(x)
        
        # Concatenate normalized input
        inputs = tf.concat([x_normalized], axis=1)
        
        # Define model architecture
        dense1_out = self.dense1(inputs)
        dense2_out = self.dense2(dense1_out)
        outputs = self.dense3(dense2_out)
        return outputs

# Define the loss function for the PINN
def physics_loss(model, x):
    with tf.GradientTape(persistent=True) as tape:
        tape.watch(x)
        predictions = model(x)
    u_x = tape.gradient(predictions, x)
    u_xx = tape.gradient(u_x, x)

    # Example: Enforce a simple physics equation (1D diffusion equation)
    f = -u_xx if u_xx is not None else 0.0  # Check if u_xx is not None before using it

    # PINN loss: enforce the physics equation at random points in the domain
    pinn_loss = tf.reduce_mean(tf.square(f))

    return pinn_loss

# Create instances of the modified PINN model and optimizer
pinn_model = PINNModel()
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, clipvalue=1.0)


# Training loop for the PINN
num_pinn_epochs = 10000

for epoch in range(num_pinn_epochs):
    with tf.GradientTape() as tape:
        # Compute the physics-informed loss
        pinn_loss = physics_loss(pinn_model, tf.convert_to_tensor(x_pinn_data, dtype=tf.float32))

    # Update the PINN model
    grads = tape.gradient(pinn_loss, pinn_model.trainable_variables)
    optimizer.apply_gradients(zip(grads, pinn_model.trainable_variables))

    # Print the PINN loss every 100 epochs
    if epoch % 100 == 0:
        print(f"PINN Epoch {epoch}, Loss: {pinn_loss.numpy()}")

# Training loop for the Land Surface Model (LSM)
# (In a real-world scenario, you might have observed data to compare against)
num_lsm_epochs = 5000

for epoch in range(num_lsm_epochs):
    # Simulate the land surface model
    y_lsm_model = land_surface_model(num_lsm_points).reshape(-1, 1)

    # Update the LSM parameters based on the model output (for simplicity, in this example)
    rainfall_rate = 0.02 + 0.005 * np.random.randn()
    evaporation_rate = 0.01

    # Print the LSM loss every 100 epochs
    if epoch % 100 == 0:
        lsm_loss = np.mean(np.square(y_lsm_data - y_lsm_model))
        print(f"LSM Epoch {epoch}, Loss: {lsm_loss}")

# Use the trained PINN model for predictions
x_test = np.linspace(0, 5, 100).reshape(-1, 1)
predictions = pinn_model(tf.convert_to_tensor(x_test, dtype=tf.float32)).numpy()

# Plot the results
import matplotlib.pyplot as plt

plt.scatter(x_pinn_data, y_pinn_data, label='PINN Training Data')
plt.plot(x_test, predictions, label='PINN Predictions', color='r')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('Physics-Informed Neural Network (PINN) Predictions')
plt.show()

# Plot the LSM results
plt.scatter(x_lsm_data, y_lsm_data, label='LSM Training Data')
plt.plot(x_lsm_data, y_lsm_model, label='LSM Model Output', color='g')
plt.xlabel('X')
plt.ylabel('Soil Moisture')
plt.legend()
plt.title('Land Surface Model (LSM) Simulation')
plt.show()
