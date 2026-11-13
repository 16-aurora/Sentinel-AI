"""
Sentinel AI - Risk Assessment Pipeline V2

Integrates:
- Risk Scorer
- Risk Prioritizer
- Risk Alert Engine
- Risk Explainer
"""

from src.risk_engine.risk_scorer import RiskScorer
from src.risk_engine.risk_prioritizer import RiskPrioritizer
from src.risk_engine.risk_alerts import RiskAlertEngine
from src.risk_engine.risk_explainer import RiskExplainer


class RiskAssessmentPipeline:

    def __init__(self):
        self.scorer = RiskScorer()
        self.prioritizer = RiskPrioritizer()
        self.alert_engine = RiskAlertEngine()
        self.explainer = RiskExplainer()

    def run(self, data):

        # 1. Calculate risk scores
        scored = self.scorer.calculate(data.copy())

        # 2. Generate risk alerts
        alerted = self.alert_engine.generate_alerts(scored)

        # 3. Generate explanations
        explained = self.explainer.explain(alerted)

        # 4. Prioritize vulnerabilities
        assessment = self.prioritizer.prioritize(explained)

        return assessment
