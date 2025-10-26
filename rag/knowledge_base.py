import os
import json
import pandas as pd
from typing import List, Dict
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    CSVLoader,
    PyPDFLoader
)
class KnowledgeBase:
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.documents = {}
        
    def load_knowledge_base(self):
        self.documents['building_codes'] = self._load_pdfs(f"{self.knowledge_base_path}/building_codes")
        loaders = {
            'insurance_guidelines': DirectoryLoader(
                f"{self.knowledge_base_path}/insurance_guidelines", 
                glob="**/*.json",
                loader_cls=TextLoader
            ),
            'construction_standards': DirectoryLoader(
                f"{self.knowledge_base_path}/construction_standards",
                glob="**/*.txt",
                loader_cls=TextLoader
            )
        }
        
        try:
            csv_loader = CSVLoader(f"{self.knowledge_base_path}/real_estate_data/neighborhood_comps.csv")
            self.documents['real_estate_data'] = csv_loader.load()
        except Exception as e:
            print(f"Error loading real_estate_data: {e}")
            self.documents['real_estate_data'] = []
        
        for category, loader in loaders.items():
            try:
                self.documents[category] = loader.load()
                print(f"Loaded {len(self.documents[category])} documents from {category}")
            except Exception as e:
                print(f"Error loading {category}: {e}")
                self.documents[category] = []
    
    def _load_pdfs(self, directory: str) -> List[Document]:
        documents = []
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.pdf'):
                    try:
                        loader = PyPDFLoader(os.path.join(directory, filename))
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading PDF {filename}: {e}")
        print(f"Loaded {len(documents)} PDF documents from building_codes")
        return documents
    
    def get_documents_by_category(self, category: str) -> List[Document]:
        return self.documents.get(category, [])
    