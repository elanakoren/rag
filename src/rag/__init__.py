from datasets import load_dataset

def main() -> None:
    ds = load_dataset("emozilla/pg19", split="train[:50]")
    print(ds)