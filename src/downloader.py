
from pathlib import Path

import requests


class SECDownloader:
    """Download SEC Form 13F quarterly ZIP datasets."""

    def __init__(
        self,
        download_dir: str | Path = "data/raw",
        user_agent: str = "13f-research contact@example.com",
    ) -> None:
        self.download_dir = Path(download_dir)
        self.user_agent = user_agent

    def download(
        self,
        url: str,
        filename: str | None = None,
        overwrite: bool = False,
    ) -> Path:
        """Download one ZIP file and return its local path."""

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if filename is None:
            filename = url.rsplit("/", maxsplit=1)[-1]

        output_path = self.download_dir / filename

        if output_path.exists() and not overwrite:
            return output_path

        headers = {
            "User-Agent": self.user_agent,
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()

        output_path.write_bytes(response.content)

        return output_path

    def download_latest(
        self,
        overwrite: bool = False,
    ) -> Path:
        """Download the latest dataset configured for this project."""

        url = (
            "https://www.sec.gov/files/structureddata/data/"
            "form-13f-data-sets/"
            "01dec2025-28feb2026_form13f.zip"
        )

        return self.download(
            url=url,
            overwrite=overwrite,
        )
