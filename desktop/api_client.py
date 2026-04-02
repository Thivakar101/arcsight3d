import requests
import json
import os

class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:5000/api/v1"):
        self.base_url = base_url
        self.timeout = 30

    def create_project(self, name, description):
        url = f"{self.base_url}/projects"
        payload = {"name": name, "description": description}
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def upload_blueprint(self, project_id, file_path):
        url = f"{self.base_url}/projects/{project_id}/blueprint"
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(url, files=files, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def process_project(self, project_id, config):
        url = f"{self.base_url}/projects/{project_id}/process"
        response = requests.post(url, json=config, timeout=60) # Longer timeout for processing
        response.raise_for_status()
        return response.json()
        
    def generate_model(self, project_id, config):
        url = f"{self.base_url}/projects/{project_id}/generate"
        response = requests.post(url, json=config, timeout=120) # Blender can take time
        response.raise_for_status()
        return response.json()

    def download_model(self, project_id, export_id, save_path):
        url = f"{self.base_url}/projects/{project_id}/exports/{export_id}/download"
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
