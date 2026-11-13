"""
Positive-Unlabeled Bagging implementation.

Unlabeled observations are temporarily treated as negative
examples during each iteration. They are not confirmed negatives.
"""

import numpy as np

from sklearn.base import clone
from sklearn.utils import check_random_state


class PUBagging:
    """
    Positive-Unlabeled Bagging classifier.

    Parameters
    ----------
    estimator : sklearn-compatible estimator
        Base binary classifier.

    n_estimators : int, default=50
        Number of independent PU training iterations.

    max_samples : int or None, default=None
        Number of unlabeled observations sampled per iteration.
        If None, uses the number of confirmed positives.

    random_state : int or None, default=42
        Random seed for reproducibility.
    """

    def __init__(
        self,
        estimator,
        n_estimators=50,
        max_samples=None,
        random_state=42
    ):
        self.estimator = estimator
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.random_state = random_state

    def fit(self, X, y):
        """Train independent classifiers using PU Bagging."""

        X = np.asarray(X)
        y = np.asarray(y)

        if X.ndim != 2:
            raise ValueError("X must be a two-dimensional array.")

        if len(X) != len(y):
            raise ValueError("X and y must have the same number of rows.")

        if not np.isin(y, [0, 1]).all():
            raise ValueError("y must contain only 0 and 1.")

        positive_indices = np.flatnonzero(y == 1)
        unlabeled_indices = np.flatnonzero(y == 0)

        if len(positive_indices) == 0:
            raise ValueError("At least one positive observation is required.")

        if len(unlabeled_indices) == 0:
            raise ValueError("At least one unlabeled observation is required.")

        if self.n_estimators < 1:
            raise ValueError("n_estimators must be at least 1.")

        sample_size = (
            len(positive_indices)
            if self.max_samples is None
            else self.max_samples
        )

        if not isinstance(sample_size, (int, np.integer)):
            raise ValueError("max_samples must be an integer.")

        if sample_size < 1 or sample_size > len(unlabeled_indices):
            raise ValueError(
                "max_samples must be between 1 and the unlabeled pool size."
            )

        self.random_state_ = check_random_state(self.random_state)
        self.estimators_ = []

        for _ in range(self.n_estimators):

            sampled_unlabeled = self.random_state_.choice(
                unlabeled_indices,
                size=sample_size,
                replace=False
            )

            training_indices = np.concatenate([
                positive_indices,
                sampled_unlabeled
            ])

            X_iteration = X[training_indices]

            y_iteration = np.concatenate([
                np.ones(len(positive_indices), dtype=int),
                np.zeros(len(sampled_unlabeled), dtype=int)
            ])

            estimator = clone(self.estimator)

            estimator.fit(X_iteration, y_iteration)

            self.estimators_.append(estimator)

        self.n_features_in_ = X.shape[1]
        self.classes_ = np.array([0, 1])
        self.n_positive_ = len(positive_indices)
        self.n_unlabeled_ = len(unlabeled_indices)
        self.sample_size_ = sample_size

        return self

    def predict_scores(self, X):
        """
        Aggregate positive-class scores across PU iterations.

        These scores are not calibrated real-world probabilities.
        """

        if not hasattr(self, "estimators_"):
            raise RuntimeError("The model must be fitted before prediction.")

        X = np.asarray(X)

        if X.ndim != 2 or X.shape[1] != self.n_features_in_:
            raise ValueError("X has an incompatible feature shape.")

        scores = []

        for estimator in self.estimators_:
            positive_column = np.flatnonzero(estimator.classes_ == 1)

            if len(positive_column) != 1:
                raise ValueError("Base estimator does not expose class 1.")

            scores.append(
                estimator.predict_proba(X)[:, positive_column[0]]
            )

        return np.mean(scores, axis=0)