"""Service interface contracts.

Every service in this application is consumed through an abstract interface
defined here (Dependency Inversion Principle). `app.services.implementations`
provides concrete classes; `app.api.v1.dependencies` wires interface ->
implementation via FastAPI's `Depends()`. No route or service should ever
import a class from `implementations` directly.
"""
