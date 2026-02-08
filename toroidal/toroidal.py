import numpy as np
import pandas as pd

def compute_derivatives(df, cols, dt):
    df = df.copy()
    for c in cols:
        df[f"d_{c}"] = df[c].diff() / dt
        df[f"dd_{c}"] = df[f"d_{c}"].diff() / dt
    return df

def toroidal_score(df, cols):
    score = 0
    for c in cols:
        score += df[f"d_{c}"].abs()
        score += df[f"dd_{c}"].abs()
    return score

def detect_toroidal_nodes(
    df,
    cols,
    vel_eps=5e-4,
    acc_eps=5e-5,
    min_amp=1e-6
):
    mask = pd.Series(True, index=df.index)
    for c in cols:
        mask &= df[f"d_{c}"].abs() < vel_eps
        mask &= df[f"dd_{c}"].abs() < acc_eps
        mask &= df[c].abs() > min_amp
    return mask

