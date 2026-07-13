from pathlib import Path
from pypdf import PdfMerger


def merge_pdfs(paths, output_path):
    merger = PdfMerger()
    for path in paths:
        path = Path(path)
        if path.exists() and path.stat().st_size > 0:
            merger.append(str(path))
    merger.write(str(output_path))
    merger.close()
    return output_path
