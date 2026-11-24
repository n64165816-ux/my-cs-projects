# Traffic Sign Recognition & Autopilot Simulation

A Convolutional Neural Network (CNN) built with **TensorFlow/Keras** and **OpenCV** to classify 43 categories of German traffic signs (GTSRB dataset), extended with a real-time **2D Autopilot Simulation** built in **Pygame** to demonstrate model deployment and decision-making.

---

## Model Architecture & Experimentation

To achieve high classification accuracy while preventing overfitting, the following CNN architecture was designed and tested:

1. **Convolutional Block 1:** `Conv2D` with **32 filters** `(3x3)` and `ReLU` activation to extract low-level visual features (edges, colors, and basic contours), followed by `MaxPooling2D` `(2x2)` for spatial downsampling.
2. **Convolutional Block 2:** `Conv2D` with **64 filters** `(3x3)` and `ReLU` activation to capture complex geometric shapes (triangles, circles, octagons) and internal symbols, followed by `MaxPooling2D` `(2x2)`.
3. **Flattening & Classification:** A `Flatten` layer feeding into a fully connected `Dense` layer of **128 units** (`ReLU`), regularized with a **0.4 Dropout** rate to prevent overfitting on the training set.
4. **Output Layer:** A `Dense` layer of **43 units** (`NUM_CATEGORIES`) with `softmax` activation to output a probability distribution across all traffic sign classes.

### Training Results
* **Optimizer:** `adam` | **Loss Function:** `categorical_crossentropy` | **Epochs:** `10`
* **Training Accuracy:** `95.08%` (Loss: `0.1612`)
* **Test Set Accuracy:** **`98.38%`** (Loss: `0.0745`)

---

## Project Structure & Usage

* `traffic.py`: Loads the dataset, builds and trains the CNN model, evaluates accuracy on the test split, and saves the trained model (`autopilot_model.keras`).
* `autopilot_sim.py`: A real-time Pygame simulation that loads the saved `.keras` model and uses `model.predict()` to read road signs and dynamically control vehicle speed, braking, and stops.

### Running the Project

1. **Install dependencies:**
   ```bash
   pip install opencv-python scikit-learn tensorflow pygame-ce
   ```

2. **Train and save the model:**
   ```bash
   python traffic.py gtsrb autopilot_model.keras
   ```

3. **Run the Autopilot Simulation:**
   ```bash
   python autopilot_sim.py
   ```

---

## Real-World Applications of This Pipeline

Beyond traffic sign recognition, the end-to-end computer vision pipeline developed in this project (**Data Preprocessing $\rightarrow$ CNN Training $\rightarrow$ Real-Time Inference**) can be directly adapted to solve high-impact real-world problems by retraining the model on domain-specific image datasets:

* **Precision Agriculture (AgriTech):** Detecting early-stage plant diseases, nutrient deficiencies, or pest damage by analyzing leaf images via mobile cameras before outbreaks spread across crops.
* **Smart Recycling & Waste Management:** Automating material sorting on conveyor belts in recycling facilities by classifying plastics, glass, metals, and cardboard in real time.
* **Industrial Safety & Traffic Monitoring:** Monitoring workplace compliance (such as detecting whether workers are wearing safety helmets and protective gear) or automating license plate recognition (ANPR) and road safety monitoring.
* **Medical Imaging Diagnostics:** Assisting healthcare professionals by pre-screening X-rays, MRI scans, or dermatological images to flag anomalies quickly and accurately.
