# scripts/generate_ground_truth.py
import argparse
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    for fname in os.listdir(args.input):
        if not fname.endswith('.pdf'):
            continue
        pdf_path = os.path.join(args.input, fname)
        with open(pdf_path, 'rb') as f:
            response = requests.post(
                'http://localhost:8000/convert',
                files={'file': (fname, f, 'application/pdf')}
            )
        markdown = response.json().get('markdown', '')
        out_path = os.path.join(args.output, fname.replace('.pdf', '.md'))
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"[DONE] {fname}")

if __name__ == '__main__':
    main()