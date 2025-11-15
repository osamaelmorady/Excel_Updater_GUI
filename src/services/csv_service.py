# task_scheduler/services/csv_service.py
import csv
from typing import List, Tuple


def load_csv_file(
    path: str,
    encoding: str = "utf-8",
    delimiter: str | None = None,
) -> Tuple[List[str], List[List[str]]]:
    """
    Load a CSV file and return (headers, rows).

    - headers: list of column names (first row)
    - rows: list of data rows, each a list of str

    If delimiter is None, try to detect it using csv.Sniffer
    and fall back to comma.
    """
    with open(path, "r", encoding=encoding, newline="") as f:
        # read a small sample for sniffing
        sample = f.read(4096)
        f.seek(0)

        if delimiter is None:
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
                delimiter = dialect.delimiter
            except Exception:
                delimiter = ","  # fallback

        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        return [], []

    headers = rows[0]
    data_rows = rows[1:]
    return headers, data_rows
