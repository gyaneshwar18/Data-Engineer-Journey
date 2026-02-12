import pandas as pd
import json
import logging
from pathlib import Path


class StudentETLPipeline:

    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            cfg = json.load(f)

        self.input_path = Path(cfg["input_path"])
        self.output_path = Path(cfg["output_path"])
        log_file = Path(cfg["log_file"])

        log_file.parent.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )

        self.df = None

    # -------- EXTRACT --------
    def extract(self):
        logging.info("Extract stage started")
        self.df = pd.read_csv(self.input_path)
        logging.info(f"Loaded {len(self.df)} rows")

    # -------- TRANSFORM --------
    def transform(self):
        logging.info("Transform stage started")

        self.df["marks"] = pd.to_numeric(
            self.df["marks"],
            errors="coerce"
        )

        self.df = (
            self.df
            .groupby("name")["marks"]
            .mean()
            .reset_index(name="avg_marks")
        )

        logging.info("Aggregation complete")

    # -------- LOAD --------
    def load(self):
        logging.info("Load stage started")
        self.df.to_csv(self.output_path, index=False)
        logging.info(f"Saved output to {self.output_path}")

    # -------- RUN --------
    def run(self):
        logging.info("Pipeline started")

        try:
            self.extract()
            self.transform()
            self.load()
            logging.info("Pipeline completed successfully")

        except Exception as e:
            logging.exception(f"Pipeline failed: {e}")
            raise


if __name__ == "__main__":
    pipeline = StudentETLPipeline()
    pipeline.run()
