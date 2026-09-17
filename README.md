# 🛡️ NetGuard

## Machine Learning-Based Network Intrusion Detection System

```

```
NetGuard is an end-to-end academic machine-learning application for
**Network Intrusion Detection (NIDS)**. The system analyzes labelled
network-flow data and classifies traffic into two categories:

-   `0 → BENIGN`
-   `1 → ATTACK`

The project combines data preprocessing, exploratory analysis,
supervised machine learning, model evaluation, feature analysis,
interactive traffic prediction, and multi-model consensus in a Streamlit
dashboard.

> **Academic disclaimer:** NetGuard is an academic/research prototype.
> Its predictions depend on the supplied training and evaluation data
> and should not be treated as a complete enterprise
> intrusion-prevention system or as a guarantee of real-world attack
> detection.

------------------------------------------------------------------------

## 🌐 Live Demo

Add your deployed Streamlit URL here when available:

``` text
https
```

------------------------------------------------------------------------

# 📌 Problem Statement

Modern networks generate large volumes of traffic that can be difficult
to inspect manually. Traditional intrusion detection approaches can
depend heavily on predefined signatures and rules.

NetGuard demonstrates how **supervised machine learning** can learn
patterns from network-flow features and classify previously observed
traffic patterns as benign or potentially malicious.

The project focuses on the following question:

> **Can machine-learning models learn useful patterns from network-flow
> features to distinguish BENIGN traffic from ATTACK traffic?**

------------------------------------------------------------------------

# 🎯 Objectives

-   Load and analyze network intrusion datasets.
-   Clean and prepare network-flow data for machine learning.
-   Convert multi-class traffic labels into a binary `BENIGN` / `ATTACK`
    classification.
-   Select relevant network-flow features.
-   Train multiple supervised machine-learning models.
-   Compare model performance using multiple evaluation metrics.
-   Analyze ROC and Precision-Recall behavior.
-   Study relationships between network features using correlation
    analysis.
-   Interpret Random Forest feature importance.
-   Provide an interactive traffic-prediction interface.
-   Compare predictions from multiple models using majority voting.
-   Maintain session-level training history and support CSV export.
-   Provide a foundation for future real-time packet capture and
    automated security response.

------------------------------------------------------------------------

# 🧬 Dataset

## CIC-IDS2017

NetGuard supports CSV files from the **CIC-IDS2017** network intrusion
dataset.

The dataset contains network-flow characteristics associated with benign
traffic and different types of attacks.

For the current binary classification task, the original labels are
converted into:

``` text
BENIGN        → 0
Any attack    → 1
```

Therefore, although the source dataset contains multiple attack
categories, the current model answers the higher-level question:

``` text
Is the traffic BENIGN or ATTACK?
```

### Dataset loading behavior

The application:

1.  Searches for CSV files in the `Datasets` directory.
2.  Loads available network-traffic data when CSV files are present.
3.  Uses a simulated network-traffic dataset as a fallback when no CSV
    dataset is found.

> The simulated dataset is intended for demonstration/testing and should
> not be interpreted as representative of all real-world network
> traffic.

------------------------------------------------------------------------

# 🔗 Dataset Source

The project is designed around the **CIC-IDS2017** dataset from the
Canadian Institute for Cybersecurity.

Dataset information:

``` text
CIC-IDS2017
Canadian Institute for Cybersecurity
```

If a specific downloaded copy or mirror was used, the exact
source/reference should be documented in the repository according to the
dataset license and citation requirements.

------------------------------------------------------------------------

# 🔍 Network Features

NetGuard selects relevant network-flow attributes from the available
dataset.

Examples include:

  -----------------------------------------------------------------------
  Feature                             Description
  ----------------------------------- -----------------------------------
  `Flow Duration`                     Duration of the network flow

  `Total Fwd Packets`                 Number of forward-direction packets

  `Total Backward Packets`            Number of backward-direction
                                      packets

  `Total Length of Fwd Packets`       Total data carried by forward
                                      packets

  `Total Length of Bwd Packets`       Total data carried by backward
                                      packets

  `Fwd Packet Length Mean`            Average forward packet size

  `Bwd Packet Length Mean`            Average backward packet size

  `Flow Bytes/s`                      Approximate bytes transferred per
                                      second

  `Flow Packets/s`                    Approximate packets transferred per
                                      second

  `Fwd IAT Mean`                      Average forward inter-arrival time
  -----------------------------------------------------------------------

The application selects features from a predefined candidate list and
limits the selected feature set to a maximum of **15 features**.

------------------------------------------------------------------------

# 🧹 Data Preprocessing

The preprocessing pipeline performs the following operations:

### 1. Create a working copy

The input DataFrame is copied before processing.

### 2. Handle infinite values

Positive and negative infinity values are replaced with missing values.

``` text
+∞ / -∞ → NaN
```

### 3. Handle missing values

Missing values are replaced with:

``` text
NaN → 0
```

### 4. Identify the label column

The application checks for the network-traffic label column, including
the possible leading-space variant.

### 5. Convert labels

The original labels are converted into a binary target:

``` text
BENIGN → 0
Other labels → 1
```

### 6. Select relevant features

The application first searches for predefined network-flow features. If
fewer than five are available, it falls back to numerical columns while
excluding the label and generated `Attack` column.

### 7. Limit feature count

A maximum of 15 selected features is used.

### 8. Train-test split

The data is divided using:

``` python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)
```

This produces:

``` text
70% → Training
30% → Testing
```

Stratification helps preserve the class distribution between training
and testing data.

> **Current implementation note:** The code does not apply a separate
> StandardScaler/normalization step or PCA transformation before
> training.

------------------------------------------------------------------------

# 📊 Exploratory Data Analysis

NetGuard provides analytical visualizations directly through the
Streamlit dashboard.

The **Advanced Analytics** section includes:

-   Traffic/class distribution
-   ROC curves
-   Precision-Recall curves
-   Random Forest feature importance
-   Feature correlation heatmap
-   Model comparison
-   Classification metrics
-   Confusion matrices

The correlation heatmap helps identify relationships between network
features.

For example, packet counts and their corresponding total packet lengths
can show strong relationships because they describe related aspects of
the same network flow.

> Correlation analysis describes **feature-to-feature relationships**.
> It is different from Random Forest feature importance, which describes
> how features contribute to tree-based prediction.

------------------------------------------------------------------------

# 🧠 PCA / Dimensionality Reduction

PCA was considered as a dimensionality-reduction technique in the
project architecture.

However:

> **PCA is not implemented in the current code.**

The current implementation instead restricts the model to a maximum of
15 selected original network features.

Keeping the original network-flow features has an interpretability
advantage because features such as packet count, flow duration, and
bytes per second retain their original meanings.

PCA can be evaluated in a future version if the feature space becomes
substantially larger.

------------------------------------------------------------------------

# 🤖 Machine Learning Models

NetGuard currently implements **three supervised classification
algorithms**.

## 1. 🌲 Random Forest

Configuration:

``` text
n_estimators = 100
max_depth = 15
random_state = 42
n_jobs = -1
```

Random Forest combines multiple decision trees.

The current scikit-learn configuration uses **Gini impurity by default**
for tree splitting.

Gini impurity helps the trees select splits that make the resulting
groups more class-pure.

Random Forest feature importance is obtained using:

``` python
rf_model.feature_importances_
```

------------------------------------------------------------------------

## 2. 📈 Gradient Boosting

Configuration:

``` text
n_estimators = 100
random_state = 42
```

Gradient Boosting builds an ensemble sequentially, where later trees
improve the existing model's errors.

------------------------------------------------------------------------

## 3. 🎯 Support Vector Machine

Configuration:

``` text
kernel = RBF
probability = True
random_state = 42
```

The RBF kernel enables non-linear decision boundaries.

Probability estimation is enabled so the application can obtain
probability-related prediction information from the trained SVM.

------------------------------------------------------------------------

# ⚖️ Model Comparison

The application trains the available classifiers on the same
training/testing split and displays their performance for comparison.

The dashboard allows comparison using:

-   Accuracy
-   Precision
-   Recall
-   F1-Score
-   ROC-AUC
-   Confusion Matrix
-   ROC Curve
-   Precision-Recall Curve

> **Current implementation note:** The project does not use a separate
> predefined F1-based automatic "best model" selection rule like the
> AquaGuard example. Instead, the application trains the available
> models, evaluates them, displays their results, and allows multi-model
> comparison.

------------------------------------------------------------------------

# 📈 Model Evaluation

## Accuracy

Measures the overall proportion of correctly classified samples.

\[ Accuracy = rac{TP + TN}{TP + TN + FP + FN} \]

## Precision

Measures how many samples predicted as attacks were actually attacks.

\[ Precision = rac{TP}{TP + FP} \]

## Recall

Measures how many actual attacks were detected.

\[ Recall = rac{TP}{TP + FN} \]

For intrusion detection, recall is important because a false negative
represents an attack that the system failed to detect.

## F1-Score

The harmonic mean of precision and recall.

\[ F1 = 2 imes rac{Precision imes Recall}{Precision + Recall} \]

## ROC-AUC

The ROC curve plots:

-   False Positive Rate on the X-axis
-   True Positive Rate / Recall on the Y-axis

The AUC summarizes class-separation performance across classification
thresholds.

In the current project evaluation, **Random Forest and Gradient Boosting
can produce AUC = 1.000 on the evaluated test data**.

This means perfect separation on that particular evaluation data. It
does **not** prove perfect real-world intrusion detection.

## Precision-Recall Curve

The Precision-Recall curve shows the trade-off between precision and
recall across classification thresholds.

This is especially relevant to NIDS because:

``` text
False Negative → Attack missed
False Positive → Normal traffic treated as attack
```

Both types of error matter in security monitoring.

------------------------------------------------------------------------

# 🧪 Confusion Matrix

The confusion matrix summarizes classification results using four
categories:

``` text
                    Predicted
                 BENIGN    ATTACK

Actual BENIGN      TN        FP

Actual ATTACK      FN        TP
```

Where:

-   **TN** = correctly identified benign traffic
-   **FP** = benign traffic incorrectly classified as attack
-   **FN** = attack traffic incorrectly classified as benign
-   **TP** = correctly identified attack traffic

The application uses the confusion matrix to calculate and display
precision, recall, and F1-score.

------------------------------------------------------------------------

# ⚡ Interactive Live Detection

The **Live Detection** module provides an interactive prediction
interface.

### Workflow

``` text
Select Trained Model
        ↓
Adjust Network Parameters
        ↓
Create One Traffic Record
        ↓
model.predict()
        ↓
model.predict_proba()
        ↓
BENIGN / ATTACK
```

The user can adjust network-flow characteristics such as:

-   Flow Duration
-   Total Forward Packets
-   Total Backward Packets
-   Total Forward Packet Length
-   Total Backward Packet Length
-   Forward Packet Length Mean
-   Backward Packet Length Mean
-   Flow Bytes/s
-   Flow Packets/s

Features that are not exposed through sliders use median values in the
current implementation.

### Important limitation

The current Live Detection module is **not a packet sniffer**.

It does not currently:

-   Capture packets from a network interface.
-   Automatically extract CIC-IDS2017-style features from live packets.
-   Automatically block an IP address.
-   Automatically modify firewall rules.
-   Send external security alerts.

It is an interactive demonstration of model inference.

------------------------------------------------------------------------

# 🧠 Multi-Model Consensus

NetGuard can send the same traffic record to all three models:

``` text
                    Traffic Record
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    Random Forest    Gradient Boosting    SVM
          ↓               ↓               ↓
       ATTACK          ATTACK           BENIGN
          │               │               │
          └───────────────┼───────────────┘
                          ↓
                    Majority Voting
                          ↓
                       ATTACK
```

For example:

``` text
Random Forest      → ATTACK
Gradient Boosting  → ATTACK
SVM                → BENIGN
```

Two out of three models predict ATTACK, so the majority-vote result is:

``` text
ATTACK
```

The consensus mechanism is an additional decision-support mechanism; it
should not automatically be interpreted as proof that the majority vote
is more accurate.

------------------------------------------------------------------------

# 📊 Feature Importance

Random Forest provides feature-importance values through:

``` python
rf_model.feature_importances_
```

These values indicate how much the selected features contribute to
impurity reduction across the trained decision trees.

This should be distinguished from the correlation matrix:

``` text
Correlation Matrix
    ↓
Relationship between features

Random Forest Feature Importance
    ↓
Contribution of features within the Random Forest
```

------------------------------------------------------------------------

# 🗂️ Application Modules

NetGuard is organized into five main dashboard tabs:

  Tab                      Purpose
  ------------------------ ----------------------------------------------
  **Dataset Overview**     Dataset inspection and traffic analysis
  **Model Performance**    Model metrics and classification performance
  **Advanced Analytics**   ROC, PR, feature importance, correlation
  **Live Detection**       Interactive traffic prediction
  **History & Reports**    Training history and CSV export

------------------------------------------------------------------------

# 📜 History & Reports

The application maintains session-level training information including:

-   Training timestamp
-   Model name
-   Accuracy
-   Number of samples

The project also provides CSV export functionality.

The current implementation does not generate a full PDF report; the PDF
report action is intentionally blocked by the application's security
protocol.

------------------------------------------------------------------------

# 📁 Repository Structure

A recommended GitHub structure is:

``` text
NetGuard/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── Datasets/
│   └── CIC-IDS2017 CSV files
│
└── screenshots/
    ├── dashboard.png
    ├── dataset-overview.png
    ├── model-performance.png
    ├── analytics.png
    ├── live-detection.png
    └── consensus.png
```

If your actual Python file has another name, replace `app.py`
accordingly.

------------------------------------------------------------------------

# 📸 Screenshots

Recommended screenshots for the GitHub repository:

### Dashboard

``` markdown
![NetGuard Dashboard](screenshots/dashboard.png)
```

### Model Performance

``` markdown
![Model Performance](screenshots/modelperformance.png)
```

### Advanced Analytics

``` markdown
![Advanced Analytics](screenshots/Advanceanalytics.png)
```

### Live Detection

``` markdown
![Live Detection](screenshots/liveDetection.png)
```

### Multi-Model Consensus

``` markdown
![Multi-Model Consensus](screenshots/consensus.png)
```

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the repository

``` bash
git clone https://github.com/tejas764/ML_project.git
cd NetGuard
```

## 2. Create a virtual environment

### Windows

``` bash
python -m venv venv
venv\Scriptsctivate
```

### Linux / macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

Core dependencies include:

``` text
streamlit
pandas
numpy
scikit-learn
matplotlib
seaborn
plotly
```

## 4. Add the dataset

Place the CIC-IDS2017 CSV files inside:

``` text
Datasets/
```

If no CSV file is found, the application can use its simulated-traffic
fallback.

## 5. Run the application

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

# 🔄 End-to-End Workflow

``` text
             CIC-IDS2017 / Simulated Traffic
                         │
                         ▼
                  Data Preprocessing
                         │
            ┌────────────┼────────────┐
            │            │            │
       Inf/NaN       Label Mapping   Feature
       Handling      BENIGN/ATTACK   Selection
            │            │            │
            └────────────┼────────────┘
                         ▼
                  Train/Test Split
                       70/30
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Random Forest  Gradient Boosting   SVM
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Model Evaluation
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      Metrics        ROC / PR       Feature Analysis
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  Streamlit Dashboard
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   Live Detection              Multi-Model Consensus
```

------------------------------------------------------------------------

# 🔐 Security & Responsible Use

NetGuard is intended for:

-   Educational use
-   Academic demonstrations
-   Research
-   Authorized security testing
-   Network-security experimentation

Do not use the system to monitor or interfere with networks without
appropriate authorization.

The displayed response suggestions, such as blocking a source IP or
alerting a security team, are recommendations only in the current
implementation.

------------------------------------------------------------------------

# ⚠️ Limitations

1.  Live Detection currently uses manually entered feature values rather
    than direct packet capture.
2.  Automatic network-flow feature extraction is not implemented.
3.  Automated firewall blocking is not implemented.
4.  External security alerting is not implemented.
5.  PCA is proposed but not implemented in the current code.
6.  Neural Network classification is not implemented in the current
    version.
7.  The system currently performs binary BENIGN/ATTACK classification
    rather than multi-class attack identification.
8.  Model performance depends strongly on the dataset used for training
    and testing.
9.  Simulated traffic is intended only as a demonstration fallback.
10. An AUC of 1.000 on the current evaluation data does not guarantee
    equivalent performance on unseen real-world network traffic.
11. The current implementation does not include a dedicated persistent
    model file such as `best_model.pkl`; models are trained within the
    application workflow.
12. The application should therefore be considered a prototype rather
    than a production NIDS/IPS.

------------------------------------------------------------------------

# 🚀 Future Scope

### 🌐 Real-Time Packet Capture

Integrate authorized packet-capture tools and network interfaces.

### 🧬 Automatic Feature Extraction

Convert captured packets into the network-flow features expected by the
trained models.

### 🧠 Neural Network Classification

Evaluate neural-network architectures alongside the existing classical
ML models.

### 📉 PCA Evaluation

Experiment with PCA when working with larger feature spaces and compare
performance with the original feature representation.

### 🛡️ Automated Response

Integrate the detection engine with authorized:

-   Firewalls
-   SIEM platforms
-   Alerting systems
-   Incident-response workflows

### 📡 Streaming Detection

Support continuous traffic streams using event-processing systems such
as Kafka or similar technologies.

### 📊 Model Monitoring

Add:

-   Data-drift detection
-   Concept-drift detection
-   False-positive monitoring
-   False-negative monitoring
-   Model performance tracking
-   Prediction latency monitoring

### 🔬 Stronger Validation

Evaluate the models using:

-   Independent datasets
-   Cross-dataset testing
-   Cross-validation
-   Hyperparameter optimization
-   Feature-ablation studies
-   Real-world authorized traffic
-   Class-imbalance analysis

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Category               Technology
  ---------------------- ----------------------------------------------------
  Programming Language   Python
  Web Application        Streamlit
  Data Processing        Pandas, NumPy
  Machine Learning       Scikit-learn
  Classification         Random Forest, Gradient Boosting, SVM
  Visualization          Matplotlib, Seaborn, Plotly
  Dataset                CIC-IDS2017
  Evaluation             Accuracy, Precision, Recall, F1, ROC-AUC, PR Curve
  Analytics              Correlation Matrix, Feature Importance

------------------------------------------------------------------------

# 📚 Concepts Demonstrated

-   Network Intrusion Detection
-   Cybersecurity
-   Machine Learning
-   Supervised Learning
-   Binary Classification
-   Random Forest
-   Gini Impurity
-   Gradient Boosting
-   Support Vector Machines
-   RBF Kernel
-   Feature Selection
-   Exploratory Data Analysis
-   Correlation Analysis
-   Feature Importance
-   Confusion Matrix
-   ROC Curve
-   ROC-AUC
-   Precision-Recall Curve
-   Majority Voting
-   Interactive Model Inference
-   Streamlit Dashboard Development

------------------------------------------------------------------------

# 👨‍💻 Author

## Tejas Bhandarkar

**NetGuard --- Machine Learning-Based Network Intrusion Detection
System**

An academic project exploring the application of machine learning
techniques to network security and intrusion detection.

------------------------------------------------------------------------

# 📜 Academic Disclaimer

NetGuard is an academic/research prototype. Predictions are generated
from patterns learned from the supplied dataset and should not be
treated as a substitute for enterprise-grade security monitoring,
incident response, firewall enforcement, or comprehensive security
assessment.

Before production deployment, the system would require independent
validation, real-time traffic integration, secure infrastructure,
monitoring, model governance, and appropriate security controls.

------------------------------------------------------------------------

# ⭐ NetGuard at a Glance

``` text
       🛡️ NETWORK TRAFFIC
                │
                ▼
       🧹 PREPROCESSING
                │
                ▼
        🔍 FEATURE ANALYSIS
                │
                ▼
       🤖 MACHINE LEARNING
       ┌────────┼────────┐
       ▼        ▼        ▼
       RF       GB       SVM
       └────────┼────────┘
                ▼
       📊 MODEL EVALUATION
                │
        ┌───────┴────────┐
        ▼                ▼
   ⚡ LIVE          🧠 CONSENSUS
   DETECTION        VOTING
        │                │
        └───────┬────────┘
                ▼
        🚨 SECURITY INSIGHT
```

```{=html}
<p align="center">
```
`<b>`{=html}🛡️ NetGuard --- Detect • Analyze • Understand`</b>`{=html}
```{=html}
</p>
```
