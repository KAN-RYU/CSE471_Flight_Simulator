import numpy as np

def vector_lerp(vecStart: np.ndarray, vecEnd: np.ndarray, t: float):
    if vecStart.shape != vecEnd.shape:
        raise Exception("Two vectors' shapes are not same")
    return vecStart*t + vecEnd*(1-t)