import datetime

class AlertAgent:
    def __init__(self):
        # Keeps track of alerts sent today
        self.sent_alerts = {}

    def should_alert(self, sku: str, risk_level: str) -> bool:
        """
        Returns True if an alert should be sent.
        Rule:
        - Only when risk is HIGH
        - Only once per SKU per day
        """
        if risk_level != "HIGH":
            return False

        today = datetime.date.today().isoformat()
        key = f"{sku}_{today}"

        if key in self.sent_alerts:
            return False  # already alerted today

        self.sent_alerts[key] = True
        return True
