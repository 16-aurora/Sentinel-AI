"""
Sentinel AI - Economic Risk Scorer V1

Heuristic economic exposure scoring.
This module does not estimate crisis probabilities.
"""

DEFAULT_WEIGHTS = {
    "growth": 0.40,
    "inflation": 0.30,
    "unemployment": 0.30
}

ADVERSE_THRESHOLD = 1.5
MAXIMUM_Z_SCORE = 3.0


def adverse_score(z_score, direction):
    """Convert an adverse Z-score into a 0-100 component score."""

    if z_score is None:
        return None

    if direction == "LOW":
        is_adverse = z_score <= -ADVERSE_THRESHOLD
        intensity = abs(z_score)

    elif direction == "HIGH":
        is_adverse = z_score >= ADVERSE_THRESHOLD
        intensity = z_score

    else:
        raise ValueError("Direction must be LOW or HIGH.")

    if not is_adverse:
        return 0.0

    return min(100.0, intensity / MAXIMUM_Z_SCORE * 100)


def classify_risk(score):
    """Classify the final heuristic economic risk score."""

    if score is None:
        return "UNAVAILABLE"
    if score >= 75:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MODERATE"
    return "LOW"


def score_economic_profile(indicators, weights=None):
    """
    Score one country-year economic profile.

    Expected indicator keys:
    gdp_growth
    gdp_per_capita_growth
    inflation
    unemployment

    Growth uses the strongest adverse component, not their sum.
    Missing dimensions cause proportional weight renormalization.
    """

    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    if set(weights) != {"growth", "inflation", "unemployment"}:
        raise ValueError("Weights must define the three risk dimensions.")

    if any(value < 0 for value in weights.values()):
        raise ValueError("Weights cannot be negative.")

    if sum(weights.values()) <= 0:
        raise ValueError("At least one weight must be positive.")

    growth_candidates = []

    for indicator in ("gdp_growth", "gdp_per_capita_growth"):
        if indicators.get(indicator) is not None:
            growth_candidates.append(
                adverse_score(indicators[indicator], "LOW")
            )

    growth_score = (
        max(growth_candidates)
        if growth_candidates else None
    )

    inflation_score = adverse_score(
        indicators.get("inflation"), "HIGH"
    )

    unemployment_score = adverse_score(
        indicators.get("unemployment"), "HIGH"
    )

    components = {
        "growth": growth_score,
        "inflation": inflation_score,
        "unemployment": unemployment_score
    }

    available_weight = sum(
        weights[name]
        for name, value in components.items()
        if value is not None
    )

    if available_weight == 0:
        final_score = None
    else:
        final_score = sum(
            weights[name] * value
            for name, value in components.items()
            if value is not None
        ) / available_weight

    return {
        "growth_risk_score": growth_score,
        "inflation_risk_score": inflation_score,
        "unemployment_risk_score": unemployment_score,
        "available_weight": available_weight,
        "economic_risk_score": final_score,
        "economic_risk_category": classify_risk(final_score)
    }
