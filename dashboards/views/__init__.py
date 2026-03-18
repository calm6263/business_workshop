# dashboards/views/__init__.py
from .dashboard import DashboardView
from . import (
    crud_views,
    crud_applicants,
    crud_consultations,
    crud_contacts,
    crud_departments,
    crud_events,
    crud_fta_journal,
    crud_news,
    crud_partners,
    crud_contact_form,
    crud_patents,
)

__all__ = ['DashboardView']