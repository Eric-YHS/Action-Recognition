from __future__ import annotations

import numpy as np


class FeatureSmoother:
    def __init__(self, alpha: float = 0.4, jump_threshold: float = 2.5) -> None:
        self.alpha = alpha
        self.jump_threshold = jump_threshold
        self._state: np.ndarray | None = None

    def reset(self) -> None:
        self._state = None

    def update(self, feature: np.ndarray | None) -> np.ndarray | None:
        if feature is None:
            self.reset()
            return None
        if self._state is None:
            self._state = feature.astype(np.float32, copy=True)
        elif float(np.linalg.norm(feature - self._state)) >= self.jump_threshold:
            self._state = feature.astype(np.float32, copy=True)
        else:
            self._state = self.alpha * feature + (1.0 - self.alpha) * self._state
        return self._state.copy()
