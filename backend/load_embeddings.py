import json
from pathlib import Path
from rag.vectorstore import save_data

def main():
    # Get the path to data.json
    data_path = Path(__file__).parent.parent / "data.json"
    
    print(f"Loading and embedding data from {data_path}...")
    save_data(str(data_path))
    print("Data has been successfully embedded and saved to Qdrant!")

if __name__ == "__main__":
    main() 