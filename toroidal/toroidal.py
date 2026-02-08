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


def detect_toroidal_nodes(df, cols, window=3):
    mask = pd.Series(False, index=df.index)

    for c in cols:
        d = df[f"d_{c}"].abs()
        dd = df[f"dd_{c}"].abs()

        local_min = (
            (d < d.rolling(window, center=True).mean()) &
            (dd < dd.rolling(window, center=True).mean())
        )

        mask |= local_min

    return mask.fillna(False)
