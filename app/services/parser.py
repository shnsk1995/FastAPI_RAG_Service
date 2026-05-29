"""Document parsing.

Strategy: pick a parser by content_type. Each parser yields a list of
`TextBlock`s preserving structure (page number, section heading, table flag)
so the chunker can split intelligently.

Parsers to support (lazy import — only load the heavy lib that matches the
file type to keep cold-start lean):
    application/pdf                          -> pypdfium2 / pdfplumber / unstructured
    application/vnd.openxmlformats...docx    -> python-docx / unstructured
    text/html                                -> trafilatura / beautifulsoup4
    text/markdown, text/plain                -> direct decode
    text/csv, application/json               -> pandas / json
    application/vnd.ms-excel, ...xlsx        -> openpyxl

For PDFs with images, optionally route through Textract async (recommended
for scanned docs; expensive). Decision point: settings.OCR_ENABLED.
"""

# class TextBlock(BaseModel):
#     text: str
#     page: int | None = None
#     section: str | None = None
#     kind: Literal["paragraph", "heading", "list", "table", "code"] = "paragraph"
#
# class DocumentParser:
#     def __init__(self, settings): ...
#
#     def parse(
#         self,
#         stream: IO[bytes],
#         content_type: str,
#         filename: str,
#     ) -> list[TextBlock]:
#         """Dispatch table by content_type. Raise IngestionError on unsupported
#         type or corrupt file. Sniff first bytes if content_type is generic
#         (application/octet-stream).
#         """
#         ...
