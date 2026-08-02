"""AI Growth Opportunities(tm) engine.

The flagship differentiated feature. Turns a resolved `Company` (plus its
AI-derived profile) into a ranked list of `app.models.opportunity.Opportunity`
objects.

Reserved layout (populated starting Phase 5, see docs/ROADMAP.md):

- `opportunity_engine.py`   — orchestrates generation: calls `AIService`
  for candidate ideas, then runs each through the scorers below.
- `scoring/impact_scorer.py`     — estimates business impact (low/medium/high).
- `scoring/complexity_scorer.py` — estimates implementation complexity.
- `scoring/priority_calculator.py` — combines impact + complexity into a
  single `priority_score`.

Exposed to the rest of the backend exclusively through
`app.services.interfaces.opportunity_service.OpportunityService` — no other
module should import from this package directly.
"""
