import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy.engine import LegacyCursorResult
from sqlalchemy.orm import Session

from database.base import get_session
from database.models import DocumentModel
from project.core import repos, Repository


# @repos
class DocumentRepos(Repository[DocumentModel, str]):
    ...
#     def __init__(self, session: Session = Depends(get_session)):
#         super().__init__(session)
#         self.session = session
#
#     def get_by_los_id(self, los_id) -> DocumentModel:
#         return self.session.get(DocumentModel, los_id)
#
#     def update(self, **kwargs) -> DocumentModel:
#         print(kwargs)
#         stmt = sa.update(DocumentModel).where(DocumentModel.los_id == kwargs.get("los_id")).values(**kwargs)
#         self.session.execute(stmt)
#         return None
