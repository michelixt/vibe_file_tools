#!/usr/bin/env python3
"""
MCP Server for Vibe File Tools using FastMCP
"""

import os
import sys

from fastmcp import FastMCP
from vibe_file_tools.file_tools import safe_search_replace, direct_search_replace

# Create the MCP server
mcp = FastMCP(name="vibe_file_tools")


@mcp.tool(description="Safe search/replace text in a file with backup and error handling")
def search_replace(file_path: str, search_text: str, replace_text: str) -> str:
    """
    Perform a safe search/replace operation on a file.
    Creates a backup before modifying and restores on error.
    
    Args:
        file_path: Path to the file to modify
        search_text: Exact text to search for (including whitespace)
        replace_text: Text to replace with
        
    Returns:
        Success message or error description
    """
    try:
        result = safe_search_replace(file_path, search_text, replace_text)
        if result:
            return f"Successfully replaced text in {file_path}"
        else:
            return f"Failed to replace text in {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(description="Direct search/replace of text in a file without backup (faster but less safe)")
def direct_search_replace_tool(file_path: str, search_text: str, replace_text: str) -> str:
    """
    Perform a direct search/replace operation on a file without creating a backup.
    
    Args:
        file_path: Path to the file to modify
        search_text: Exact text to search for (including whitespace)
        replace_text: Text to replace with
        
    Returns:
        Success message or error description
    """
    try:
        result = direct_search_replace(file_path, search_text, replace_text)
        if result:
            return f"Successfully replaced text in {file_path}"
        else:
            return f"Failed to replace text in {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """
    Main function to run the MCP server.
    """
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
