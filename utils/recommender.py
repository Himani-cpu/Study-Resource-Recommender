import pandas as pd

class Recommender:
    def __init__(self, resource_csv_path="data/resources.csv"):
        self.df = pd.read_csv(resource_csv_path)
        # Normalize columns for filtering
        self.df['subject'] = self.df['subject'].str.lower()
        self.df['difficulty'] = self.df['difficulty'].str.lower()
        self.df['type'] = self.df['type'].str.lower()
        self.df['title'] = self.df['title'].astype(str)
        self.df['description'] = self.df.get('description', pd.Series([""] * len(self.df))).astype(str)

    def get_subjects(self):
        return sorted(self.df['subject'].str.title().unique())

    def get_difficulties(self):
        return sorted(self.df['difficulty'].str.title().unique())

    def get_resource_types(self):
        return sorted(self.df['type'].str.title().unique())

    def recommend(self, subject, difficulty, resource_type="All", specific_topic=""):
        # Lowercase for comparison
        subject = subject.lower()
        difficulty = difficulty.lower()
        resource_type = resource_type.lower()
        specific_topic = specific_topic.lower().strip()

        filtered = self.df[
            (self.df['subject'] == subject) &
            (self.df['difficulty'] == difficulty)
        ]

        if resource_type != "all":
            filtered = filtered[filtered['type'] == resource_type]

        if specific_topic:
            filtered = filtered[
                filtered['title'].str.lower().str.contains(specific_topic) |
                filtered['description'].str.lower().str.contains(specific_topic)
            ]

        # Convert to dict for easy use in Streamlit
        results = filtered.to_dict(orient='records')
        return results
