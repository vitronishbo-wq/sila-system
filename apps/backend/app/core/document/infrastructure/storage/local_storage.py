from pathlib import Path


class LocalStorage:
    """Implementação simples de storage local para o SILA."""

    def __init__(self, base_path: str = "storage", **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_file(self, content: bytes, sub_folder: str, file_name: str) -> str:
        """Guarda ficheiro e retorna caminho relativo."""
        folder = self.base_path / sub_folder
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / file_name
        with open(file_path, "wb") as f:
            f.write(content)
        return str(Path(sub_folder) / file_name)

    def delete_file(self, relative_path: str):
        """Remove ficheiro do storage."""
        full_path = self.base_path / relative_path
        if full_path.exists():
            full_path.unlink()

    def get_full_path(self, relative_path: str) -> str:
        return str(self.base_path / relative_path)
