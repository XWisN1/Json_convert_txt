import os
import json
import argparse
from datetime import datetime
from tqdm import tqdm

def extract_json_values(json_files, keys, output_dir, max_rows_per_file):
    generated_files = {}
    for key in keys:
        file_index = 1
        row_count = 0
        current_file_path = None
        generated_files[key] = []

        for json_file in tqdm(json_files, desc=f"Extracting {key}", unit="file"):
            with open(json_file, 'r') as jf:
                data_list = json.load(jf)
                print(f"Processed: {json_file} \n")
                for data in data_list:
                    if key in data:
                        value = data[key]
                        # 检查值是否为列表
                        if isinstance(value, list):
                            for item in value:
                                if row_count >= max_rows_per_file:
                                    file_index += 1
                                    row_count = 0
                                    current_file_path = os.path.join(output_dir, f"{key}_{datetime.now().timestamp()}_part{file_index}.txt")
                                    generated_files[key].append(current_file_path)
                                    with open(current_file_path, 'w',encoding='utf-8') as f:
                                        continue
                                if current_file_path is None:
                                    output_file = f"{key}_{datetime.now().timestamp()}.txt"
                                    current_file_path = os.path.join(output_dir, output_file)
                                    generated_files[key].append(current_file_path)
                                    with open(current_file_path, 'w',encoding='utf-8') as f:
                                        f.write(str(item) + '\n')
                                        row_count += 1
                                else:
                                    with open(current_file_path, 'a',encoding='utf-8') as f:
                                        f.write(str(item) + '\n')
                                        row_count += 1
                        else: # 值不是列表
                            if row_count >= max_rows_per_file:
                                file_index += 1
                                row_count = 0
                                current_file_path = os.path.join(output_dir, f"{key}_{datetime.now().timestamp()}_part{file_index}.txt")
                                generated_files[key].append(current_file_path)
                                with open(current_file_path, 'w',encoding='utf-8') as f:
                                    continue
                            if current_file_path is None:
                                output_file = f"{key}_{datetime.now().timestamp()}.txt"
                                current_file_path = os.path.join(output_dir, output_file)
                                generated_files[key].append(current_file_path)
                                with open(current_file_path, 'w',encoding='utf-8') as f:
                                    f.write(str(value) + '\n')
                                    row_count += 1
                            else:
                                with open(current_file_path, 'a',encoding='utf-8') as f:
                                    f.write(str(value) + '\n')
                                    row_count += 1

    return generated_files

def main():
    parser = argparse.ArgumentParser(description="Extract JSON values to TXT files.")
    parser.add_argument('keys', nargs='+', help="Comma-separated list of JSON keys to extract.")
    parser.add_argument('--path', default='.', help="Path to the directory containing JSON files.")
    parser.add_argument('--max_rows_per_file', type=int, default=5000, help="Maximum number of rows per TXT file.")

    args = parser.parse_args()

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create output directory in the script's directory
    output_dir = os.path.join(script_dir, "_txt")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all JSON files in the specified directory
    json_files = [os.path.join(args.path, f) for f in os.listdir(args.path) if f.endswith('.json')]

    if not json_files:
        print(f"No JSON files in {args.path}")
        return

    # Extract values
    generated_files = extract_json_values(json_files, args.keys, output_dir, args.max_rows_per_file)

    # Print generated file paths
    print("Generated files:")
    for key, file_paths in generated_files.items():
        for file_path in file_paths:
            print(file_path)

    print("Extraction complete.")

if __name__ == "__main__":
    main()