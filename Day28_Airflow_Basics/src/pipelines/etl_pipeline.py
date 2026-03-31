def extract():
    print("Extracting data...")
    data = ["ORDER1", "ORDER2", "ORDER3"]
    return data


def transform(data):
    print("Transforming data...")
    transformed = [d.lower() for d in data]
    return transformed


def load(data):
    print("Loading data...")
    for d in data:
        print(f"Loaded: {d}")


def run_pipeline():
    data = extract()
    transformed = transform(data)
    load(transformed)


# For local testing
if __name__ == "__main__":
    run_pipeline()
