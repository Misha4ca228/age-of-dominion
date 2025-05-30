import json
import os

class Json:
    def load(self, relative_path):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, ".."))
        full_path = os.path.join(project_root, relative_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_project_path(self, *parts):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        return os.path.join(project_root, *parts)

json_loader = Json()