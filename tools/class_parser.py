from pydantic import BaseModel


class PDFMetadata(BaseModel):
    """
    Metadata of a scientific paper.
    """
    title: str
    authors: list[str]
    year: int
    publisher: str | None = None
    summary: str | None = None
