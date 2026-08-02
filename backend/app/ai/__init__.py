"""AI boundary.

`openrouter_client.py` is the only module that knows OpenRouter's request
shape. `schemas.py` defines the Pydantic model the single structured
research response is validated against. `AIService` (see
`app.services.interfaces.ai_service`, backed by
`app.services.implementations.openrouter_ai_service`) is the public
contract other layers depend on. The `opportunities/` subpackage remains
reserved for a future dedicated scoring engine — for now,
`ai_opportunity_service.py` derives opportunities from the same single AI
call as everything else.
"""
