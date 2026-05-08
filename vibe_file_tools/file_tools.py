#!/usr/bin/env python3
"""
Vibe File Tools - Direct file manipulation utilities for the Vibe agent
"""

import os
from typing import Tuple

def find_exact_section(file_content: str, search_text: str) -> Tuple[int, int]:
    """
    Find the exact start and end positions of search_text in file_content
    
    Args:
        file_content: Full content of the file
        search_text: Exact text to search for
        
    Returns:
        Tuple of (start_pos, end_pos) if found, (-1, -1) if not found
    """
    start_pos = file_content.find(search_text)
    if start_pos == -1:
        return (-1, -1)
    
    end_pos = start_pos + len(search_text)
    return (start_pos, end_pos)

def direct_search_replace(file_path: str, search_text: str, replace_text: str) -> bool:
    """
    Perform a direct search/replace operation on a file
    
    Args:
        file_path: Path to the file to modify
        search_text: Exact text to search for (including whitespace)
        replace_text: Text to replace with
        
    Returns:
        True if successful, False if failed
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If we don't have write permissions
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Read the original file content
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Find the exact section to replace
    start_pos, end_pos = find_exact_section(original_content, search_text)
    
    if start_pos == -1:
        # Provide detailed debugging info
        error_msg = f"Search text not found in {file_path}\n"
        error_msg += f"Search text length: {len(search_text)} characters\n"
        error_msg += f"Search text preview: {repr(search_text[:100])}\n"
        
        # Try to find similar text for debugging
        lines = original_content.split('\n')
        for i, line in enumerate(lines):
            if search_text.strip() in line:
                error_msg += f"Found similar text on line {i+1}: {repr(line)}\n"
        
        raise ValueError(error_msg)
    
    # Perform the replacement
    new_content = original_content[:start_pos] + replace_text + original_content[end_pos:]
    
    # Verify the replacement would actually change something
    if new_content == original_content:
        raise ValueError("Replacement did not change the file content")
    
    # Write the new content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def safe_search_replace(file_path: str, search_text: str, replace_text: str) -> bool:
    """
    Safe version of search_replace with backup and error handling
    
    Args:
        file_path: Path to the file to modify
        search_text: Exact text to search for (including whitespace)
        replace_text: Text to replace with
        
    Returns:
        True if successful, False if failed
    """
    try:
        # Create backup
        backup_path = file_path + ".vibe_backup"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
        
        # Perform the replacement
        result = direct_search_replace(file_path, search_text, replace_text)
        
        # Clean up backup on success
        if result and os.path.exists(backup_path):
            os.unlink(backup_path)
        
        return result
        
    except Exception as e:
        print(f"ERROR in safe_search_replace: {e}")
        
        # Try to restore from backup if it exists
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as src:
                    with open(file_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                os.unlink(backup_path)
                print(f"Restored {file_path} from backup")
            except Exception as restore_error:
                print(f"Failed to restore from backup: {restore_error}")
        
        return False

# Example usage
if __name__ == "__main__":
    # Test the functions
    test_file = "test_file.txt"
    
    # Create test file
    with open(test_file, 'w') as f:
        f.write("Hello World!\nThis is a test.\nMultiple lines here.\n")
    
    try:
        # Test successful replacement
        result = direct_search_replace(
            test_file,
            "Multiple lines here.\n",
            "Replaced content here.\n"
        )
        print(f"Test 1 - Success: {result}")
        
        # Test failed replacement (text not found)
        try:
            result = direct_search_replace(
                test_file,
                "Non-existent text",
                "Should not replace"
            )
            print(f"Test 2 - Should have failed: {result}")
        except ValueError as e:
            print(f"Test 2 - Correctly failed: {str(e)[:50]}...")
            
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.unlink(test_file)