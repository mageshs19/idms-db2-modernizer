import pdfplumber

from idms_modernizer.domain.document_models import (
    DocumentLine,
    DocumentModel,
    DocumentPage,
)


class TextExtractor:

    def extract_document(
        self,
        pdf_path: str
    ) -> DocumentModel:

        pages = []

        with pdfplumber.open(
            pdf_path
        ) as pdf:

            for page_index, page in enumerate(pdf.pages):

                text = (
                    page.extract_text()
                    or ""
                )

                lines = []

                for line_index, line in enumerate(
                    text.splitlines()
                ):

                    lines.append(
                        DocumentLine(
                            line_number=line_index,
                            text=line.strip()
                        )
                    )

                pages.append(
                    DocumentPage(
                        page_number=page_index,
                        lines=lines
                    )
                )

        return DocumentModel(
            pages=pages
        )