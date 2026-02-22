#!/usr/bin/env python3
"""
SILA System - Document Header Standardization Script
Adds standardized YAML front matter with metadata to existing documents.
Integrates with the document traceability system.
"""

import json
import sys
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DocumentHeaderManager:
    """Manages document headers and metadata standardization."""

    def __init__(self, project_root: str = None):
        """Initialize the header manager."""
        self.project_root = (
            Path(project_root) if project_root else Path(__file__).parent.parent
        )
        self.docs_dir = self.project_root / "docs"
        self.traceability_file = self.docs_dir / "RASTREABILIDADE_DOCUMENTACAO.json"

    def load_traceability_data(self) -> Dict:
        """Load traceability data to get document information."""
        if not self.traceability_file.exists():
            print(
                "⚠️  Warning: Traceability data not found. Run 'python scripts/map_docs.py' first."
            )
            return {}

        try:
            with open(self.traceability_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error loading traceability data: {e}")
            return {}

    def get_document_info(self, doc_path: str) -> Dict:
        """Get document information from traceability data."""
        data = self.load_traceability_data()

        for doc in data.get("documents", []):
            if doc["document_path"] == doc_path:
                return doc

        return {}

    def generate_header_metadata(self, doc_path: str, doc_info: Dict = None) -> Dict:
        """Generate standardized metadata header for a document."""
        if doc_info is None:
            doc_info = self.get_document_info(doc_path)

        # Base metadata
        metadata = {
            "generated_by": doc_info.get("generated_by", "manual"),
            "generated_on": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "system_version": os.getenv("SYSTEM_VERSION", "v20251010.150000"),
            "status": doc_info.get("status", "manual"),
        }

        # Add document-specific metadata
        metadata.update(
            {
                "document_type": doc_info.get("document_type", "unknown"),
                "last_modified": doc_info.get("last_modified", "unknown"),
                "size_bytes": doc_info.get("size_bytes", 0),
            }
        )

        return metadata

    def read_existing_header(self, file_path: Path) -> tuple[Dict, str]:
        """Read existing YAML header and content from a markdown file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if file has YAML front matter
            if content.startswith("---"):
                lines = content.split("\n")
                yaml_lines = []
                content_start = 1  # Skip the first ---

                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == "---" and i > 1:
                        content_start = i + 1
                        break
                    yaml_lines.append(line)

                if yaml_lines:
                    try:
                        existing_metadata = yaml.safe_load("\n".join(yaml_lines)) or {}
                        remaining_content = (
                            "\n".join(lines[content_start:])
                            if content_start < len(lines)
                            else ""
                        )
                        return existing_metadata, remaining_content
                    except yaml.YAMLError:
                        pass  # Invalid YAML, treat as no header

            return {}, content

        except Exception as e:
            print(f"⚠️  Warning reading {file_path}: {e}")
            return {}, ""

    def write_document_with_header(
        self, file_path: Path, metadata: Dict, content: str
    ) -> bool:
        """Write document with standardized YAML header."""
        try:
            # Generate YAML header
            yaml_header = yaml.dump(
                metadata, default_flow_style=False, allow_unicode=True, sort_keys=False
            )
            yaml_header = yaml_header.strip()

            # Create full content with header
            full_content = f"---\n{yaml_header}\n---\n\n{content}"

            # Write back to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_content)

            return True

        except Exception as e:
            print(f"❌ Error writing header to {file_path}: {e}")
            return False

    def standardize_document(self, doc_path: str, force: bool = False) -> bool:
        """Standardize a single document with proper header."""
        file_path = self.docs_dir / doc_path

        if not file_path.exists():
            print(f"❌ Document not found: {doc_path}")
            return False

        # Skip non-markdown files for now (could be extended later)
        if file_path.suffix.lower() not in [".md", ".txt"]:
            print(f"⏭️  Skipping non-markdown file: {doc_path}")
            return False

        print(f"📝 Processing: {doc_path}")

        # Read existing header and content
        existing_metadata, content = self.read_existing_header(file_path)

        # Generate new metadata
        doc_info = self.get_document_info(doc_path)
        new_metadata = self.generate_header_metadata(doc_path, doc_info)

        # Merge with existing metadata (preserve existing if not force)
        if existing_metadata and not force:
            # Preserve existing metadata, only add missing fields
            for key, value in new_metadata.items():
                if key not in existing_metadata or not existing_metadata[key]:
                    existing_metadata[key] = value
            final_metadata = existing_metadata
        else:
            final_metadata = new_metadata

        # Write back with new header
        return self.write_document_with_header(
            file_path, final_metadata, content.strip()
        )

    def standardize_all_documents(
        self, force: bool = False, dry_run: bool = False
    ) -> Dict[str, int]:
        """Standardize all documents in the project."""
        results = {"processed": 0, "skipped": 0, "failed": 0}

        if not self.docs_dir.exists():
            print(f"❌ Docs directory not found: {self.docs_dir}")
            return results

        # Get list of documents from traceability data
        data = self.load_traceability_data()

        for doc_info in data.get("documents", []):
            doc_path = doc_info["document_path"]

            if dry_run:
                print(f"🔍 Would process: {doc_path}")
                results["processed"] += 1
                continue

            if self.standardize_document(doc_path, force):
                results["processed"] += 1
            else:
                results["failed"] += 1

        return results

    def create_template_headers(self) -> None:
        """Create template header files for different document types."""
        templates_dir = self.docs_dir / "templates"
        templates_dir.mkdir(exist_ok=True)

        templates = {
            "documento_gerado.md": {
                "generated_by": "script_name.py",
                "generated_on": "2025-10-10T15:00:00Z",
                "system_version": "v20251010.150000",
                "status": "current",
                "document_type": "markdown",
                "description": "Template for auto-generated documents",
            },
            "documento_manual.md": {
                "generated_by": "manual",
                "generated_on": "2025-10-10T15:00:00Z",
                "system_version": "v20251010.150000",
                "status": "manual",
                "document_type": "markdown",
                "description": "Template for manually created documents",
            },
        }

        for filename, metadata in templates.items():
            template_file = templates_dir / filename

            content = f"""# {metadata['description'].title()}

Este é um template para {'documentos gerados automaticamente' if metadata['generated_by'] != 'manual' else 'documentos criados manualmente'}.

## Uso

1. Copie este template para seu novo documento
2. Atualize os metadados conforme necessário
3. Adicione seu conteúdo

## Metadados

Os metadados no cabeçalho YAML são utilizados pelo sistema de rastreabilidade documental.
"""

            # Remove description from metadata before writing
            header_metadata = metadata.copy()
            del header_metadata["description"]

            self.write_document_with_header(template_file, header_metadata, content)


def main():
    """Main function for document header standardization."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Standardize document headers with metadata"
    )
    parser.add_argument("--file", "-f", help="Specific document to process")
    parser.add_argument(
        "--force", "-F", action="store_true", help="Force overwrite existing headers"
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--create-templates", action="store_true", help="Create template header files"
    )

    args = parser.parse_args()

    manager = DocumentHeaderManager()

    if args.create_templates:
        print("📋 Creating template headers...")
        manager.create_template_headers()
        print("✅ Templates created!")
        return

    if args.file:
        if args.dry_run:
            print(f"🔍 Would process: {args.file}")
        else:
            success = manager.standardize_document(args.file, args.force)
            if success:
                print(f"✅ Successfully processed: {args.file}")
            else:
                print(f"❌ Failed to process: {args.file}")
                sys.exit(1)
    else:
        print(
            "📋 Standardizing all documents..."
            if not args.dry_run
            else "🔍 Analyzing all documents..."
        )
        results = manager.standardize_all_documents(args.force, args.dry_run)

        print("\n📊 Results:")
        print(f"✅ Processed: {results['processed']}")
        print(f"❌ Failed: {results['failed']}")

        if args.dry_run:
            print("🔍 This was a dry run - no files were modified")
        elif results["failed"] == 0:
            print("✅ All documents standardized successfully!")
        else:
            print(f"⚠️  {results['failed']} documents failed to process")
            sys.exit(1)


if __name__ == "__main__":
    main()
