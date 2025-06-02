"""
Split a PDF file into multiple single-page files.

Example:
    pdfly split --output ./split/ input.pdf
        Split all pages of input.pdf into separate files in the ./split/ directory.

"""

from pathlib import Path
from typing import Iterable

from pypdf import (
    PageObject,
    PdfReader,
    PdfWriter,
)
from rich.console import Console


def main(
    filename: Path,
    output: Path,
) -> None:
    page_number_format = "02"
    try:

        # Set up the streams
        reader = PdfReader(filename)
        # num_pages = reader.get_num_pages()
        writers = yield_writers(pages=reader.pages)
        output.mkdir()
        for i, writer in enumerate(writers, start=1):
            out_path = output / f"{i:{page_number_format}}.pdf"
            # out_path.touch()
            with out_path.open("wb") as output_fh_:
                writer.write(output_fh_)

    except Exception as error:
        console = Console()
        console.print(f"Error while splitting {filename}")
        raise error


def yield_writers(pages: Iterable[PageObject]) -> Iterable[PdfWriter]:
    for page in pages:
        writer = PdfWriter()
        writer.add_page(page)
        yield writer
