import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def label_cme_occurrences(data, cme_times, fast_threshold_hrs=3, slow_window_days=4):
    data['cme'] = 0
    for t in cme_times:
        start_fast = t
        end_fast = t + timedelta(hours=fast_threshold_hrs)

        start_slow = t
        end_slow = t + timedelta(days=slow_window_days)

        # Mark a narrow window around the CME time only
        match = (data['time'] >= start_fast) & (data['time'] <= end_fast)
        data.loc[match, 'cme'] = 1
    return data


def train_cme_model(data):
    X = data.drop(columns=['time', 'cme'])
    y = data['cme']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print("\nModel Report:")
    print(classification_report(y_test, y_pred))
    
    return model, X_test, y_test, y_pred
