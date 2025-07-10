"""Document manipulation tools for the authoring team."""

import os
import uuid
from pathlib import Path
from typing import Annotated, Dict, List, Optional
from langchain_core.tools import tool
from langchain_community.vectorstores import Qdrant


def create_working_directory(base_path: str = './content/data') -> Path:
    """Create a random subdirectory for working files."""
    os.makedirs(base_path, exist_ok=True)
    random_id = str(uuid.uuid4())[:8]
    subdirectory_path = os.path.join(base_path, random_id)
    os.makedirs(subdirectory_path, exist_ok=True)
    return Path(subdirectory_path)


def create_document_tools(working_directory: Path, complaint_retriever=None):
    """Create document manipulation tools.
    
    Args:
        working_directory: Path to store documents
        complaint_retriever: Optional retriever for previous responses
        
    Returns:
        Dictionary of tool functions
    """
    
    @tool
    def create_outline(
        points: Annotated[List[str], "List of main points or sections."],
        file_name: Annotated[str, "File path to save the outline."],
    ) -> Annotated[str, "Path of the saved outline file."]:
        """Create and save an outline."""
        with (working_directory / file_name).open("w") as file:
            for i, point in enumerate(points):
                file.write(f"{i + 1}. {point}\n")
        return f"Outline saved to {file_name}"

    @tool
    def read_document(
        file_name: Annotated[str, "File path to save the document."],
        start: Annotated[Optional[int], "The start line. Default is 0"] = None,
        end: Annotated[Optional[int], "The end line. Default is None"] = None,
    ) -> str:
        """Read the specified document."""
        with (working_directory / file_name).open("r") as file:
            lines = file.readlines()
        if start is not None:
            start = 0
        return "\n".join(lines[start:end])

    @tool
    def write_document(
        content: Annotated[str, "Text content to be written into the document."],
        file_name: Annotated[str, "File path to save the document."],
    ) -> Annotated[str, "Path of the saved document file."]:
        """Create and save a text document."""
        with (working_directory / file_name).open("w") as file:
            file.write(content)
        return f"Document saved to {file_name}"

    @tool
    def edit_document(
        file_name: Annotated[str, "Path of the document to be edited."],
        inserts: Annotated[
            Dict[int, str],
            "Dictionary where key is the line number (1-indexed) and value is the text to be inserted at that line.",
        ] = {},
    ) -> Annotated[str, "Path of the edited document file."]:
        """Edit a document by inserting text at specific line numbers."""
        with (working_directory / file_name).open("r") as file:
            lines = file.readlines()

        sorted_inserts = sorted(inserts.items())

        for line_number, text in sorted_inserts:
            if 1 <= line_number <= len(lines) + 1:
                lines.insert(line_number - 1, text + "\n")
            else:
                return f"Error: Line number {line_number} is out of range."

        with (working_directory / file_name).open("w") as file:
            file.writelines(lines)

        return f"Document edited and saved to {file_name}"

    @tool 
    def reference_previous_responses(
        query: Annotated[str, "The query to search for in the previous responses."],
    ) -> Annotated[str, "The previous responses that match the query."]:
        """Search for previous responses that match the query."""
        if complaint_retriever is None:
            return "No complaint retriever available"
        return complaint_retriever.invoke(query)

    return {
        "create_outline": create_outline,
        "read_document": read_document,
        "write_document": write_document,
        "edit_document": edit_document,
        "reference_previous_responses": reference_previous_responses
    }