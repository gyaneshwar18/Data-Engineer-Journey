import pandas as pd
from pathlib import Path


class StudentETLPipeline:

    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.df = None

    # -------- EXTRACT --------
    def extract(self):
        print("📥 Extracting data...")
        self.df = pd.read_csv(self.input_path)
        print(self.df.head())

    # -------- TRANSFORM --------
    def transform(self):
        print("🔄 Transforming data...")

        # clean types
        self.df["marks"] = pd.to_numeric(self.df["marks"], errors="coerce")

        # aggregate
        self.df = (
            self.df
            .groupby("name")["marks"]
            .mean()
            .reset_index(name="avg_marks")
        )

        print(self.df)

    # -------- LOAD --------
    def load(self):
        print("💾 Loading output...")
        self.df.to_csv(self.output_path, index=False)
        print(f"✅ Saved to {self.output_path}")

    # -------- RUN PIPELINE --------
    def run(self):
        self.extract()
        self.transform()
        self.load()


# ---------- MAIN ----------
if __name__ == "__main__":
    pipeline = StudentETLPipeline(
        input_path="input.csv",
        output_path="output.csv"
    )

    pipeline.run()
