import os

class DoctrineLoader:
    def __init__(self, doctrine_dir):
        self.doctrine_dir = doctrine_dir
        self.doctrines = {}

    def load_all(self):
        try:
            for filename in os.listdir(self.doctrine_dir):
                path = os.path.join(self.doctrine_dir, filename)
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8') as file:
                        self.doctrines[filename] = file.read()
            print(f"Loaded {len(self.doctrines)} doctrine files.")
        except Exception as e:
            print(f"Error loading doctrine files: {e}")

    def summarize(self):
        summaries = {}
        for name, content in self.doctrines.items():
            first_lines = "\n".join(content.strip().splitlines()[:10])
            summaries[name] = first_lines
        return summaries

    def get(self, filename):
        return self.doctrines.get(filename, f"[{filename}] not found in doctrine set.")
