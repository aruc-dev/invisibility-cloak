
from .base import RemovalConnector
from ..llm_engine import smart_llm
from datetime import datetime
from pathlib import Path

EMAIL_TEMPLATE_PROMPT = """You are drafting a concise data-broker opt-out email.
Subject: Data removal request
Given:
- Broker Name: {broker}
- Domain: {domain}
- PII Summary: {pii}

Write a short email under 160 words requesting removal under CCPA/CPRA. Include a polite confirmation request.
Return plain text body only.
"""

class EmailGeneric(RemovalConnector):
    def submit(self):
        broker = self.broker
        pii = self.pii
        prompt = EMAIL_TEMPLATE_PROMPT.format(broker=broker.get("name"), domain=broker.get("domain"), pii=str({k:pii.get(k) for k in ['names','emails','phones','addresses']}))
        body = smart_llm(prompt)
        drafts = Path(__file__).resolve().parents[2] / "storage" / "drafts"
        drafts.mkdir(parents=True, exist_ok=True)
        fname = drafts / f"optout_{broker.get('domain','broker')}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.txt"
        fname.write_text(body)
        return {"status":"drafted","transcript":"Draft email created","evidence_path": str(fname)}
