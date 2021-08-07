import csv
import tensorflow as tf

from sklearn.model_selection import train_test_split

# model = Perceptron()
# model = svm.SVC()
# model = KNeighborsClassifier(n_neighbors=1)
model = GaussianNB()

# Read data from csv file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    # Retrieve a list of data, with 4 first values are input and last value is output 
    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row [:4]],
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })

# Split the input and output from the dataset
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]

# Seperate data into training and testing groups
# X_training: training input, Y_training: training output
# X_testing: testing input, Y_testing: testing output
X_training, X_testing, Y_training, Y_testing = train_test_split (
    evidence, labels, test_size = 0.4
)

# Create a neural network
model = tf.keras.models.Sequential()

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape = (4,), activation = "relu"))

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation = "sigmoid"))

# Train neural network
model.compile(
    optimizer = "adam",
    loss = "binary_crossentropy",
    metrics = ["accuracy"]
)

model.fit(X_training, Y_training, epochs = 20)

# Evaluate how well model performs
model.evaluate(X_testing, Y_testing, verbose = 2)