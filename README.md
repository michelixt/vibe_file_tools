# Vibe Mistral search_replace alternative for Windows

Due to vibe mistral's builtin search_replace function not working decently on Windows (cr/lf-issue and extra whitespace), this is a simple alternative version which works for me. It makes vibe work again nicely.

# Installation

```bash
pip install vibe_file_tools
```

<https://pypi.org/project/vibe-file-tools/>

# Usage

Run the MCP server:

```bash
python -m vibe_file_tools.mcp_tool
```

This exposes two tools:

- **`search_replace`** - Safe search/replace with backup and automatic restore on error
- **`direct_search_replace_tool`** - Faster search/replace without backup

Both tools accept:
- `file_path` - Path to the file to modify
- `search_text` - Exact text to search for (including whitespace)
- `replace_text` - Text to replace with
