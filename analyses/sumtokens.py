import os
import json

def get_total_tokens(data):
    """
    Attempt to retrieve the total_tokens value from the JSON data.
    First, check for a top-level key. If not found, look under response->usage.
    """
    # Check top-level first
    if "total_tokens" in data and isinstance(data["total_tokens"], int):
        return data["total_tokens"]
    
    # Check nested location: response->usage->total_tokens
    if ("response" in data and isinstance(data["response"], dict) and
        "usage" in data["response"] and isinstance(data["response"]["usage"], dict) and
        "total_tokens" in data["response"]["usage"] and
        isinstance(data["response"]["usage"]["total_tokens"], int)):
        return data["response"]["usage"]["total_tokens"]
    
    # Not found
    return None

def sum_tokens_in_json_files(directory):
    total_tokens = 0
    files_processed = 0

    if not os.path.isdir(directory):
        print(f"❌ Invalid directory: {directory}")
        return
    
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("success_") and filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Debug: Print keys to help inspect the JSON structure
                    print(f"📂 Processing {filename} - Keys: {list(data.keys())}")
                    
                    tokens = get_total_tokens(data)
                    if tokens is not None:
                        total_tokens += tokens
                        files_processed += 1
                    else:
                        print(f"⚠️ Warning: 'total_tokens' not found in {filename}!")
            
            except json.JSONDecodeError as e:
                print(f"❌ Error: Could not parse {filename} (Invalid JSON) - {e}")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
    
    print(f"\n✅ Total tokens: {total_tokens} (Processed {files_processed} files)")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    sum_tokens_in_json_files(folder_path)
