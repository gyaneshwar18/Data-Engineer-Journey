def extract():
    print("Extracting data...")
    data = ["ORDER1", "ORDER2", "ORDER3"]
    return data


def transform(ti):
    data = ti.xcom_pull(task_ids='extract_task')
    print("Transforming data...")
    transformed = [d.lower() for d in data]
    return transformed


def load(ti):
    data = ti.xcom_pull(task_ids='transform_task')
    print("Loading data...")
    for d in data:
        print(f"Loaded: {d}")
