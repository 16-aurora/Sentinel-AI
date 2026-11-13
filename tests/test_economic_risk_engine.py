import unittest

from economic_risk_scorer import (
    adverse_score,
    classify_risk,
    score_economic_profile
)


class TestEconomicRiskEngine(unittest.TestCase):

    def test_non_adverse_indicators_score_zero(self):
        result = score_economic_profile({
            "gdp_growth": 0.5,
            "gdp_per_capita_growth": 0.4,
            "inflation": 0.5,
            "unemployment": 0.8
        })
        self.assertEqual(result["economic_risk_score"], 0.0)
        self.assertEqual(result["economic_risk_category"], "LOW")

    def test_extreme_growth_decline(self):
        result = score_economic_profile({
            "gdp_growth": -3.0,
            "gdp_per_capita_growth": -2.0,
            "inflation": 0.0,
            "unemployment": 0.0
        })
        self.assertAlmostEqual(result["growth_risk_score"], 100.0)
        self.assertAlmostEqual(result["economic_risk_score"], 40.0)

    def test_correlated_growth_indicators_are_not_added(self):
        result = score_economic_profile({
            "gdp_growth": -3.0,
            "gdp_per_capita_growth": -3.0,
            "inflation": 0.0,
            "unemployment": 0.0
        })
        self.assertAlmostEqual(result["growth_risk_score"], 100.0)
        self.assertAlmostEqual(result["economic_risk_score"], 40.0)

    def test_missing_growth_dimension_renormalizes_weights(self):
        result = score_economic_profile({
            "inflation": 3.0,
            "unemployment": 0.0
        })
        self.assertAlmostEqual(result["available_weight"], 0.60)
        self.assertAlmostEqual(result["economic_risk_score"], 50.0)

    def test_missing_all_indicators_returns_unavailable(self):
        result = score_economic_profile({})
        self.assertIsNone(result["economic_risk_score"])
        self.assertEqual(result["economic_risk_category"], "UNAVAILABLE")

    def test_risk_classification_boundaries(self):
        self.assertEqual(classify_risk(0), "LOW")
        self.assertEqual(classify_risk(25), "MODERATE")
        self.assertEqual(classify_risk(50), "HIGH")
        self.assertEqual(classify_risk(75), "CRITICAL")

    def test_invalid_direction_is_rejected(self):
        with self.assertRaises(ValueError):
            adverse_score(2.0, "UNKNOWN")

    def test_invalid_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            score_economic_profile(
                {"inflation": 2.0},
                {"growth": -0.1, "inflation": 0.5, "unemployment": 0.6}
            )


if __name__ == "__main__":
    unittest.main()
