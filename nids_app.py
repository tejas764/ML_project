import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os
from datetime import datetime
import io

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#20e3d2", "#ffbf47", "#ff4d6d", "#4da3ff", "#9d7bff"]

st.set_page_config(
    page_title=" Network Intrusion Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

theme_enable = False

# Custom CSS for better UI
st.markdown("""
<style>
    :root {
        --bg: #07111f;
        --panel: #0f1d2d;
        --panel-2: #14263b;
        --text: #edf7ff;
        --muted: #a7bdd1;
        --cyan: #20e3d2;
        --blue: #4da3ff;
        --amber: #ffbf47;
        --danger: #ff4d6d;
        --border: rgba(96, 190, 255, 0.25);
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(32, 227, 210, 0.16), transparent 30%),
            radial-gradient(circle at 85% 0%, rgba(255, 191, 71, 0.12), transparent 28%),
            linear-gradient(135deg, #07111f 0%, #0c1725 48%, #111827 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1380px;
    }

    .main-header {
        font-size: clamp(2.3rem, 5vw, 4.8rem) !important;
        line-height: 1.05;
        font-weight: 900;
        color: #f7fbff;
        text-align: center;
        margin: 0 0 0.5rem 0;
        letter-spacing: 0;
        text-shadow: 0 0 28px rgba(32, 227, 210, 0.35);
    }

    .hero-subtitle {
        text-align: center;
        color: var(--muted);
        font-size: 1.05rem;
        margin: 0 auto 1.6rem auto;
        max-width: 900px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1625 0%, #101d2d 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(20, 38, 59, 0.96), rgba(9, 22, 37, 0.96));
        border: 1px solid var(--border);
        border-left: 4px solid var(--cyan);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.28);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 800;
    }

    div[data-testid="stTabs"] button {
        background: rgba(15, 29, 45, 0.74);
        border-radius: 8px 8px 0 0;
        color: var(--muted);
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #07111f;
        background: linear-gradient(135deg, var(--cyan), var(--amber));
        font-weight: 800;
    }
    .metric-card {
        background: linear-gradient(135deg, var(--panel) 0%, var(--panel-2) 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        border: 1px solid var(--border);
    }
    .stAlert {
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stButton>button,
    .stDownloadButton>button {
        background: linear-gradient(135deg, #20e3d2 0%, #4da3ff 100%);
        color: #06111f;
        border: 0;
        border-radius: 8px;
        font-weight: 800;
        box-shadow: 0 10px 26px rgba(32, 227, 210, 0.22);
    }

    .stButton>button:hover,
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #ffbf47 0%, #20e3d2 100%);
        color: #06111f;
        border: 0;
        transform: translateY(-1px);
    }

    .stDataFrame,
    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(96, 190, 255, 0.18);
    }
</style>
""", unsafe_allow_html=True)

# Title and Description
# st.markdown('<p class="main-header" style="font-size: 60px !important; line-height: 1.2;">🛡️ Advanced AI Network Intrusion Detection System</p>', unsafe_allow_html=True)

st.markdown("""
    <h1 class="main-header">
        Network Intrusion Detection System
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-subtitle">
    <b>Professional Network Security Monitoring with Advanced Machine Learning</b><br>
    Multi-Model Analysis &nbsp;|&nbsp; Real-time Detection &nbsp;|&nbsp; Comprehensive Analytics
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'training_history' not in st.session_state:
    st.session_state['training_history'] = []
if 'prediction_count' not in st.session_state:
    st.session_state['prediction_count'] = {'normal': 0, 'attack': 0}
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'Dark Mode'

st.sidebar.header("⚙️ Advanced Control Panel")
st.sidebar.markdown("---")

# Theme Enable Logic
if theme_enable:
    available_themes = ["Dark Mode", "Light Mode"]

    current_val = st.session_state.get('theme', 'Dark Mode')
    if current_val not in available_themes:
        current_val = 'Dark Mode'
        
    theme = st.sidebar.selectbox("🎨 Theme", available_themes, 
    index=available_themes.index(current_val))
else:
    theme = 'Dark Mode'

# Update theme in session state
if theme != st.session_state['theme']:
    st.session_state['theme'] = theme
    st.rerun()

# Apply theme-specific CSS
if theme == "Dark Mode":
    st.markdown("""
    <style>
        /* Dark mode uses the primary dashboard styling above. */
    </style>
    """, unsafe_allow_html=True)
elif theme == "Light Mode":
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            text-align: center;
            margin-bottom: 1rem;
        }
        .stMetric {
            background: linear-gradient(135deg, #ffffff 0%, #e9ecef 100%);
            padding: 1rem;
            border-radius: 10px;
            border: 2px solid #0066cc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #004499 0%, #0066cc 100%);
            box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

# Function to generate simulated data
def generate_simulation_data(num_samples=1000):
    """Generate realistic network traffic data for training"""
    np.random.seed(42)
    
    # Normal Traffic (70%)
    normal_samples = int(num_samples * 0.7)
    normal_data = {
        'Flow Duration': np.random.normal(2000000, 500000, normal_samples),
        'Total Fwd Packets': np.random.randint(1, 50, normal_samples),
        'Total Backward Packets': np.random.randint(1, 50, normal_samples),
        'Total Length of Fwd Packets': np.random.normal(1000, 300, normal_samples),
        'Total Length of Bwd Packets': np.random.normal(1000, 300, normal_samples),
        'Fwd Packet Length Mean': np.random.normal(500, 150, normal_samples),
        'Flow Bytes/s': np.random.normal(10000, 3000, normal_samples),
        'Flow Packets/s': np.random.normal(50, 15, normal_samples),
        'Fwd IAT Mean': np.random.normal(100000, 30000, normal_samples),
        'Bwd IAT Mean': np.random.normal(100000, 30000, normal_samples),
        'Label': ['BENIGN'] * normal_samples
    }
    
    # Attack Traffic (30%)
    attack_samples = num_samples - normal_samples
    attack_data = {
        'Flow Duration': np.random.normal(500000, 200000, attack_samples),
        'Total Fwd Packets': np.random.randint(50, 500, attack_samples),
        'Total Backward Packets': np.random.randint(0, 10, attack_samples),
        'Total Length of Fwd Packets': np.random.normal(5000, 1000, attack_samples),
        'Total Length of Bwd Packets': np.random.normal(100, 50, attack_samples),
        'Fwd Packet Length Mean': np.random.normal(1500, 500, attack_samples),
        'Flow Bytes/s': np.random.normal(50000, 10000, attack_samples),
        'Flow Packets/s': np.random.normal(200, 50, attack_samples),
        'Fwd IAT Mean': np.random.normal(10000, 5000, attack_samples),
        'Bwd IAT Mean': np.random.normal(10000, 5000, attack_samples),
        'Label': np.random.choice(['DDoS', 'DoS', 'PortScan', 'BruteForce'], attack_samples)
    }
    
    df_normal = pd.DataFrame(normal_data)
    df_attack = pd.DataFrame(attack_data)
    df = pd.concat([df_normal, df_attack], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def load_csv_data(file_path):
    """Load data from CSV file or use simulation"""
    
    if file_path and os.path.exists(file_path):
        try:
            st.info(f"📂 Loading data from: {os.path.basename(file_path)}")
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
            st.success(f"✅ Successfully loaded {len(df)} records from CSV!")
            return df, True
        except Exception as e:
            st.error(f"❌ Error loading CSV: {str(e)}")
            st.info("Using simulated data instead...")
            return generate_simulation_data(2000), False
    else:
        st.warning("⚠️ No CSV file found. Using simulated data instead.")
        st.info("📥 To use real data, download CIC-IDS2017 dataset and place CSV in Datasets folder")
        return generate_simulation_data(2000), False

def preprocess_data(df, is_real_csv=True):
    """Preprocess the dataset for training"""
    
    data = df.copy()
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.fillna(0)
    
    if 'Label' in data.columns:
        label_col = 'Label'
    elif ' Label' in data.columns:
        label_col = ' Label'
    else:
        st.error("❌ Label column not found!")
        return None, None, None
    
    data['Attack'] = data[label_col].apply(lambda x: 0 if 'BENIGN' in str(x).upper() else 1)
    
    feature_columns = []
    possible_features = [
        'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
        'Fwd Packet Length Mean', 'Bwd Packet Length Mean',
        'Flow Bytes/s', 'Flow Packets/s', 'Fwd IAT Mean',
        'Bwd IAT Mean', 'Fwd PSH Flags', 'Bwd PSH Flags',
        'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
        'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
        'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance'
    ]
    
    for feature in possible_features:
        if feature in data.columns:
            feature_columns.append(feature)
        elif f' {feature}' in data.columns:
            feature_columns.append(f' {feature}')
    
    if len(feature_columns) < 5:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        feature_columns = [col for col in numeric_cols if col not in [label_col, 'Attack']]
    
    feature_columns = feature_columns[:15]
    
    if not feature_columns:
        st.error("❌ No valid features found!")
        return None, None, None
    
    X = data[feature_columns]
    y = data['Attack']
    
    return X, y, feature_columns

def train_models(X, y, selected_models):
    """Train multiple ML models"""
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    models = {}
    results = {}
    
    model_configs = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42)
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, model_name in enumerate(selected_models):
        status_text.text(f"🤖 Training {model_name}...")
        
        model = model_configs[model_name]
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)
        
        precision, recall, _ = precision_recall_curve(y_test, y_proba)
        
        models[model_name] = model
        results[model_name] = {
            'accuracy': accuracy,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_proba': y_proba,
            'fpr': fpr,
            'tpr': tpr,
            'roc_auc': roc_auc,
            'precision': precision,
            'recall': recall,
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        progress_bar.progress((idx + 1) / len(selected_models))
    
    status_text.text("✅ All models trained successfully!")
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()
    
    return models, results, X_test, y_test, X_train

# Main Application
def main():
    
    st.sidebar.subheader("📁 Dataset Selection")
    
    if os.path.exists("Datasets"):
        csv_files = [f for f in os.listdir("Datasets") if f.endswith('.csv')]
    else:
        csv_files = []
    
    if csv_files:
        selected_file = st.sidebar.selectbox("Select CSV File:", csv_files)
        selected_file_path = os.path.join("Datasets", selected_file)
    else:
        st.sidebar.warning("No CSV files found")
        st.sidebar.info("Place CSV in Datasets folder")
        selected_file = None
        selected_file_path = None
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 Model Selection")
    
    model_options = ['Random Forest', 'Gradient Boosting', 'SVM']
    selected_models = st.sidebar.multiselect(
        "Select Models to Train:",
        model_options,
        default=['Random Forest', 'Gradient Boosting']
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Training Options")
    
    data_size = st.sidebar.slider("Simulated Data Size:", 1000, 5000, 2000, 500)
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚀 Train Models Now", use_container_width=True):
        if not selected_models:
            st.error("⚠️ Please select at least one model!")
            return
        
        train_file = selected_file_path
        data, is_real = load_csv_data(train_file)

        if not is_real:
            data = generate_simulation_data(data_size)

        result = preprocess_data(data, is_real)

        if result[0] is None:
            st.error("Failed to preprocess data!")
            return

        X, y, feature_cols = result
        models, results, X_test, y_test, X_train = train_models(X, y, selected_models)

        st.session_state['train_file_path'] = selected_file_path
        st.session_state['selected_models'] = selected_models
        st.session_state['data_size'] = data_size
        st.session_state['model_trained'] = True
        st.session_state['data'] = data
        st.session_state['is_real'] = is_real
        st.session_state['models'] = models
        st.session_state['results'] = results
        st.session_state['feature_cols'] = feature_cols
        st.session_state['X_data'] = X

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for model_name, result in results.items():
            st.session_state['training_history'].append({
                'timestamp': timestamp,
                'model': model_name,
                'accuracy': result['accuracy'],
                'samples': len(X)
            })
        st.success("Models trained successfully. You can now use the dashboard without retraining.")
    
    if st.session_state.get('model_trained', False):
        required_state = ['data', 'models', 'results', 'feature_cols', 'X_data']
        if any(key not in st.session_state for key in required_state):
            st.warning("Training data is not available in this session. Please click 'Train Models Now' again.")
            return

        data = st.session_state['data']
        models = st.session_state['models']
        results = st.session_state['results']
        feature_cols = st.session_state['feature_cols']
        X = st.session_state['X_data']
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dataset Overview", 
            "🤖 Model Performance", 
            "📈 Advanced Analytics",
            "🔴 Live Detection",
            "📜 History & Reports"
        ])
        
        with tab1:
            st.subheader("📁 Dataset Information")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("📦 Total Records", len(data))
            with col2:
                st.metric("📊 Features", len(data.columns) - 1)
            with col3:
                if 'Label' in data.columns:
                    benign_count = len(data[data['Label'].str.contains('BENIGN', case=False, na=False)])
                elif ' Label' in data.columns:
                    benign_count = len(data[data[' Label'].str.contains('BENIGN', case=False, na=False)])
                else:
                    benign_count = 0
                st.metric("✅ Normal Traffic", benign_count)
            with col4:
                attack_count = len(data) - benign_count
                st.metric("🚨 Attack Traffic", attack_count)
            with col5:
                attack_ratio = (attack_count / len(data)) * 100 if len(data) > 0 else 0
                st.metric("⚠️ Attack Ratio", f"{attack_ratio:.1f}%")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Sample Data Preview:**")
                st.dataframe(data.head(10), use_container_width=True)
            
            with col2:
                if 'Label' in data.columns or ' Label' in data.columns:
                    label_col = 'Label' if 'Label' in data.columns else ' Label'
                    st.write("**Attack Types Distribution:**")
                    
                    attack_dist = data[label_col].value_counts()
                    
                    fig = px.pie(
                        values=attack_dist.values, 
                        names=attack_dist.index,
                        title="Traffic Distribution",
                        hole=0.4,
                        color_discrete_sequence=["#20e3d2", "#ffbf47", "#ff4d6d", "#4da3ff", "#9d7bff"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("🤖 Model Performance Comparison")
            
            col1, col2, col3, col4 = st.columns(4)
            
            best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
            
            with col1:
                st.metric("🏆 Best Model", best_model[0])
            with col2:
                st.metric("🎯 Best Accuracy", f"{best_model[1]['accuracy']*100:.2f}%")
            with col3:
                avg_accuracy = np.mean([r['accuracy'] for r in results.values()])
                st.metric("📊 Avg Accuracy", f"{avg_accuracy*100:.2f}%")
            with col4:
                st.metric("🔢 Models Trained", len(results))
            
            # Model comparison bar chart
            st.write("**Accuracy Comparison:**")
            model_names = list(results.keys())
            accuracies = [results[m]['accuracy'] * 100 for m in model_names]
            
            fig = go.Figure(data=[
                go.Bar(x=model_names, y=accuracies, 
                       text=[f"{acc:.2f}%" for acc in accuracies],
                       textposition='auto',
                       marker_color=['#20e3d2', '#ffbf47', '#ff4d6d'])
            ])
            fig.update_layout(
                title="Model Accuracy Comparison",
                xaxis_title="Model",
                yaxis_title="Accuracy (%)",
                yaxis_range=[0, 100],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics for each model
            st.write("**Detailed Performance Metrics:**")
            
            for model_name, result in results.items():
                with st.expander(f"📊 {model_name} - Detailed Metrics", expanded=(model_name==best_model[0])):
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    cm = result['confusion_matrix']
                    tn, fp, fn, tp = cm.ravel()
                    
                    accuracy = result['accuracy']
                    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                    
                    with col1:
                        st.metric("🎯 Accuracy", f"{accuracy*100:.2f}%")
                    with col2:
                        st.metric("🔍 Precision", f"{precision*100:.2f}%")
                    with col3:
                        st.metric("📊 Recall", f"{recall*100:.2f}%")
                    with col4:
                        st.metric("⚡ F1-Score", f"{f1*100:.2f}%")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Confusion Matrix
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn', 
                                    xticklabels=['Normal', 'Attack'],
                                    yticklabels=['Normal', 'Attack'],
                                    cbar_kws={'label': 'Count'})
                        plt.ylabel('Actual')
                        plt.xlabel('Predicted')
                        plt.title(f'{model_name} - Confusion Matrix')
                        st.pyplot(fig)
                    
                    with col2:
                        # Metrics bar chart
                        metrics_data = pd.DataFrame({
                            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                            'Score': [accuracy*100, precision*100, recall*100, f1*100]
                        })
                        
                        fig = px.bar(metrics_data, x='Metric', y='Score',
                                    title=f'{model_name} - Performance Metrics',
                                    color='Metric',
                                    text='Score',
                                    color_discrete_sequence=["#20e3d2", "#ffbf47", "#ff4d6d", "#4da3ff"])
                        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
                        fig.update_layout(yaxis_range=[0, 105], showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("📈 Advanced Analytics & Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**ROC Curves Comparison:**")
                
                fig = go.Figure()
                
                for model_name, result in results.items():
                    fig.add_trace(go.Scatter(
                        x=result['fpr'], 
                        y=result['tpr'],
                        name=f"{model_name} (AUC={result['roc_auc']:.3f})",
                        mode='lines',
                        line=dict(width=2)
                    ))
                
                fig.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1],
                    name='Random Classifier',
                    mode='lines',
                    line=dict(dash='dash', color='gray')
                ))
                
                fig.update_layout(
                    title='Receiver Operating Characteristic (ROC) Curves',
                    xaxis_title='False Positive Rate',
                    yaxis_title='True Positive Rate',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Precision-Recall Curves:**")
                
                fig = go.Figure()
                
                for model_name, result in results.items():
                    fig.add_trace(go.Scatter(
                        x=result['recall'], 
                        y=result['precision'],
                        name=model_name,
                        mode='lines',
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title='Precision-Recall Curves',
                    xaxis_title='Recall',
                    yaxis_title='Precision',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.write("**Feature Importance Analysis:**")
            
            # Get feature importance from Random Forest
            if 'Random Forest' in models:
                rf_model = models['Random Forest']
                importance = rf_model.feature_importances_
                
                feat_imp_df = pd.DataFrame({
                    'Feature': feature_cols,
                    'Importance': importance
                }).sort_values('Importance', ascending=False)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(feat_imp_df, x='Importance', y='Feature',
                                orientation='h',
                                title='Feature Importance (Random Forest)',
                                color='Importance',
                                color_continuous_scale='Viridis')
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.write("**Top 5 Features:**")
                    for idx, row in feat_imp_df.head(5).iterrows():
                        st.metric(
                            row['Feature'][:20],
                            f"{row['Importance']:.4f}",
                            delta=None
                        )
            
            st.write("**Feature Correlation Heatmap:**")
            
            corr_matrix = X[feature_cols[:10]].corr()
            
            fig = px.imshow(corr_matrix,
                           labels=dict(color="Correlation"),
                           x=corr_matrix.columns,
                           y=corr_matrix.columns,
                           color_continuous_scale='RdBu_r',
                           aspect="auto")
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("🔴 Live Traffic Detection & Analysis")
            
            # Real-time counters
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("✅ Normal Detected", st.session_state['prediction_count']['normal'])
            with col2:
                st.metric("🚨 Attacks Detected", st.session_state['prediction_count']['attack'])
            with col3:
                total_pred = sum(st.session_state['prediction_count'].values())
                st.metric("📊 Total Predictions", total_pred)
            with col4:
                if total_pred > 0:
                    attack_pct = (st.session_state['prediction_count']['attack'] / total_pred) * 100
                    st.metric("⚠️ Attack Rate", f"{attack_pct:.1f}%")
                else:
                    st.metric("⚠️ Attack Rate", "0%")
            
            st.markdown("---")
            
            # Model selection for prediction
            selected_pred_model = st.selectbox(
                "Select Model for Prediction:",
                list(models.keys()),
                key="pred_model"
            )
            
            st.write("**Adjust Network Parameters:**")
            
            input_data = {}
            X_data = st.session_state['X_data']
            
            cols = st.columns(3)
            for idx, feature in enumerate(feature_cols[:9]):
                with cols[idx % 3]:
                    sample_val = float(X_data[feature].median())
                    min_val = float(X_data[feature].min())
                    max_val = float(X_data[feature].max())
                    
                    input_data[feature] = st.slider(
                        feature.strip()[:30],
                        min_value=min_val,
                        max_value=max_val,
                        value=sample_val,
                        key=f"slider_{feature}"
                    )
            
            for feature in feature_cols[9:]:
                input_data[feature] = float(X_data[feature].median())
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🔍 Analyze Traffic", use_container_width=True):
                    test_df = pd.DataFrame([input_data])
                    
                    model = models[selected_pred_model]
                    prediction = model.predict(test_df)[0]
                    probability = model.predict_proba(test_df)[0]
                    
                    # Update counters
                    if prediction == 0:
                        st.session_state['prediction_count']['normal'] += 1
                    else:
                        st.session_state['prediction_count']['attack'] += 1
                    
                    st.markdown("### 🎯 Detection Result")
                    
                    if prediction == 0:
                        st.success(f"✅ **NORMAL TRAFFIC** - No threat detected")
                        st.info(f"🔒 Confidence: {probability[0]*100:.2f}%")
                        st.write("**Status:** Traffic appears legitimate. Continue monitoring.")
                    else:
                        st.error(f"🚨 **ATTACK DETECTED** - Potential intrusion!")
                        st.warning(f"⚠️ Threat Probability: {probability[1]*100:.2f}%")
                        st.write("**Recommended Actions:**")
                        st.write("- 🛑 Block source IP immediately")
                        st.write("- 📧 Alert security team")
                        st.write("- 📝 Log incident for analysis")
                        st.write("- 🔍 Investigate traffic patterns")
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=probability[1]*100,
                        title={'text': "Attack Probability"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkred" if prediction == 1 else "darkgreen"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 70], 'color': "yellow"},
                                {'range': [70, 100], 'color': "lightcoral"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Multi-Model Consensus:**")
                
                if st.button("🔬 Analyze with All Models", use_container_width=True):
                    test_df = pd.DataFrame([input_data])
                    
                    consensus_results = []
                    
                    for model_name, model in models.items():
                        pred = model.predict(test_df)[0]
                        prob = model.predict_proba(test_df)[0]
                        
                        consensus_results.append({
                            'Model': model_name,
                            'Prediction': 'Attack' if pred == 1 else 'Normal',
                            'Confidence': f"{max(prob)*100:.1f}%",
                            'Attack_Prob': prob[1]
                        })
                    
                    consensus_df = pd.DataFrame(consensus_results)
                    
                    # Visual representation
                    fig = px.bar(consensus_df, x='Model', y='Attack_Prob',
                                color='Prediction',
                                title='Model Predictions Comparison',
                                labels={'Attack_Prob': 'Attack Probability'},
                                color_discrete_map={'Attack': '#ff4d6d', 'Normal': '#20e3d2'})
                    fig.update_layout(yaxis_range=[0, 1], height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(consensus_df[['Model', 'Prediction', 'Confidence']], 
                               use_container_width=True, hide_index=True)
                    
                    # Majority voting
                    attack_count = sum(1 for r in consensus_results if r['Prediction'] == 'Attack')
                    majority = "Attack" if attack_count > len(models)/2 else "Normal"
                    
                    st.info(f"🗳️ **Majority Vote:** {majority} ({attack_count}/{len(models)} models)")
        
        with tab5:
            st.subheader("📜 Training History & Report Generation")
            
            if st.session_state['training_history']:
                st.write("**Recent Training Sessions:**")
                
                history_df = pd.DataFrame(st.session_state['training_history'])
                history_df['accuracy_pct'] = history_df['accuracy'] * 100
                
                st.dataframe(
                    history_df[['timestamp', 'model', 'accuracy_pct', 'samples']].tail(10),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'timestamp': 'Training Time',
                        'model': 'Model',
                        'accuracy_pct': st.column_config.NumberColumn('Accuracy (%)', format="%.2f"),
                        'samples': 'Samples'
                    }
                )
                
                st.write("**Accuracy Trend Over Time:**")
                
                fig = px.line(history_df.tail(20), x='timestamp', y='accuracy_pct', 
                             color='model', markers=True,
                             title='Model Performance Over Time',
                             labels={'accuracy_pct': 'Accuracy (%)', 'timestamp': 'Time'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No training history available yet.")
            
            st.markdown("---")
            st.write("**📊 Generate Comprehensive Report:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Generate PDF Report", use_container_width=True):
                    st.info("PDF report generation feature - blocked by security protocols!")
            
            with col2:
                if st.button("📊 Export Results CSV", use_container_width=True):
                    # Create results dataframe
                    results_data = []
                    for model_name, result in results.items():
                        cm = result['confusion_matrix']
                        tn, fp, fn, tp = cm.ravel()
                        
                        results_data.append({
                            'Model': model_name,
                            'Accuracy': result['accuracy'],
                            'ROC_AUC': result['roc_auc'],
                            'True_Positives': tp,
                            'True_Negatives': tn,
                            'False_Positives': fp,
                            'False_Negatives': fn
                        })
                    
                    results_df = pd.DataFrame(results_data)
                    csv = results_df.to_csv(index=False)
                    
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"nids_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if st.button("🔄 Clear History", use_container_width=True):
                    st.session_state['training_history'] = []
                    st.session_state['prediction_count'] = {'normal': 0, 'attack': 0}
                    st.success("✅ History cleared!")
                    st.rerun()
            
            st.markdown("---")
            st.write("**📊 System Statistics:**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎓 Total Trainings", len(st.session_state['training_history']))
            with col2:
                if st.session_state['training_history']:
                    avg_acc = np.mean([h['accuracy'] for h in st.session_state['training_history']])
                    st.metric("📈 Avg Accuracy", f"{avg_acc*100:.2f}%")
                else:
                    st.metric("📈 Avg Accuracy", "N/A")
            with col3:
                total_predictions = sum(st.session_state['prediction_count'].values())
                st.metric("🔍 Total Predictions", total_predictions)
            with col4:
                st.metric("🗂️ Dataset Size", len(data))
    
    else:
        st.info("👈 **Configure settings in sidebar and click 'Train Models Now' to begin**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🤖 Multi-Model Support
            - Random Forest
            - Gradient Boosting
            - Support Vector Machine
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Advanced Analytics
            - ROC & PR Curves
            - Feature Importance
            - Correlation Analysis
            - Real-time Metrics
            """)
        
        with col3:
            st.markdown("""
            ### 🎯 Professional Features
            - Multi-model Consensus
            - Training History
            - Export Reports
            - Live Detection
            """)
        
        st.markdown("---")
        st.subheader("📖 About the project")
        
        st.markdown("""
# 🛡️ Gaurdian
### Machine Learning-Based Network Intrusion Detection System

---

## 🌐 Domain

**Cybersecurity & Machine Learning**

---

## 🎯 Problem Statement

Modern networks generate large volumes of traffic, making it difficult
to identify suspicious activity manually. GAurdian
 uses machine
learning to analyze network traffic, detect suspicious activity and
classify known network threats.

---

## 1️⃣ Real-World Problem

### Network Intrusion Detection

Detect malicious network traffic and identify attacks such as:

- 🔴 DDoS
- 🔴 DoS
- 🔴 PortScan
- 🔴 Other attacks available in the CIC-IDS2017 dataset

---

## 2️⃣ Objectives & Expected Outcome

### 🎯 Objectives

- Analyze network traffic patterns
- Detect suspicious and malicious traffic
- Train multiple machine learning models
- Compare model performance
- Provide real-time traffic classification
- Generate threat alerts and analytics

### ✅ Expected Outcome

A Streamlit-based NIDS that can analyze network traffic and provide
attack predictions, model performance analysis and real-time threat
detection.

---

## 3️⃣ Dataset & Environment

### 📊 Dataset

**CIC-IDS2017**

The system supports the CIC-IDS2017 dataset containing network traffic
data for different days and attack types.

If the dataset is unavailable, the application can also generate
**simulated network traffic** for testing and demonstration.

### 🛠️ Environment

**Python** • **Pandas** • **NumPy** • **Scikit-learn**
• **Matplotlib** • **Seaborn** • **Plotly** • **Streamlit**

---

## 4️⃣ Data Preprocessing & EDA

The system provides:

### 🧹 Data Processing
- Network traffic data loading
- Data preparation for ML models
- Dataset statistics
- Sample data analysis

### 📈 Exploratory Data Analysis
- Attack distribution
- Feature correlations
- Feature importance
- Network traffic analysis

---

## 5️⃣ Machine Learning Approach

### 🧠 Classification

The project uses **supervised machine learning classification**
to identify and classify network traffic.

### 🤖 Models

1. 🌲 Random Forest
2. 📈 Gradient Boosting
3. 📐 Support Vector Machine (SVM)

---

## 6️⃣ Algorithm Implementation

Multiple ML algorithms are trained and evaluated on the network
traffic data.

The application allows users to select one or more models from
the Streamlit sidebar and train them using the selected dataset.

### 🔄 ML Pipeline

Network Traffic
        ->
Dataset
        ->
Data Processing
        ->
ML Model Training
        ->
Prediction
        ->
Threat Detection



## 8️⃣ Model Evaluation

The system evaluates models using:

📊 Accuracy  
🎯 Precision  
🔍 Recall  
⚖️ F1-Score  
📉 Confusion Matrix  

Additional analytics include:

- ROC Curves
- Precision-Recall Curves
- Feature Importance
- Correlation Analysis

---

## 9️⃣ Model Comparison

The system allows the four ML approaches to be trained and compared:

🌲 Random Forest  
📈 Gradient Boosting  
📐 SVM  
 

Their performance is compared using accuracy, precision, recall,
F1-score and confusion matrices.

---

## 🔟 Suitable Model Selection

The most suitable model will be selected based on its performance
across the evaluation metrics, computational speed and suitability
for real-time network intrusion detection.

The selected model will then be used for live traffic prediction.

---

# 🚀 Complete System Workflow

CIC-IDS2017 / Simulated Data
             ↓
      Data Processing
             ↓
           EDA
             ↓
       Feature Analysis
             ↓
            PCA
             ↓
     ┌───────┴────────┐
     ↓       ↓        ↓
Random   Gradient    SVM    Neural
Forest   Boosting           Network
     └───────┬────────┘
             ↓
      Model Comparison
             ↓
       Model Selection
             ↓
       🔴 Live Detection
             ↓
      Threat Prediction
             ↓
    📊 Analytics & Reports
""")
        st.info("💡 **Tip:** Start with Random Forest and Gradient Boosting for best performance!")

if __name__ == "__main__":
    main()
