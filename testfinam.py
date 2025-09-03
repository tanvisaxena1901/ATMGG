# ==========================================
# 📦 Setup
# ==========================================


import os, json, pandas as pd
import spacy, nltk

nltk.download("punkt")
nltk.download("punkt_tab")  

nlp = spacy.load("en_core_web_sm")
print([token.text for token in nlp("The system shall encrypt PHI using AES-256.") if token.pos_ == "VERB"])

# Master toggle for BigQuery
USE_BIGQUERY = False
PROJECT_ID = "local-project"

# ==========================================
# 🛠️ Local Mocks
# ==========================================
class LocalBigQueryMock:
    def export(self, data, dataset_id, table_id):
        df = pd.DataFrame(data)
        out = f"{dataset_id}_{table_id}.csv"
        df.to_csv(out, index=False, encoding="utf-8")
        print(f"💾 Exported locally → {out}")
        return out

    def query(self, sql, file):
        print(f"⚠️ Skipping query (BigQuery disabled): {sql}")
        return pd.read_csv(file).to_dict(orient="records")

client = LocalBigQueryMock()

class LocalLLM:
    def __init__(self, model_name="mock-llm"):
        self.model_name = model_name
    def predict(self, prompt):
        return f"[MOCK-{self.model_name}] Response to: {prompt[:80]}..."

llm = LocalLLM("gemini-2.5-pro")

def safe_export(data, dataset_id, table_id):
    return client.export(data, dataset_id, table_id)

# ==========================================
# 🔹 Layer 1 – Parse Documents
# ==========================================
class BatchParser:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder

    def parse_batch(self):
        # Mock parsed requirements
        return {
            "doc1.txt": [
                "The system shall encrypt PHI using AES-256.",
                "The system shall log all access events."
            ],
            "doc2.txt": [
                "The application shall support multi-factor authentication."
            ]
        }

    def export_results(self, results, dataset_id, table_id):
        data = [{"filename": f, "chunk": c} for f, chunks in results.items() for c in chunks]
        return safe_export(data, dataset_id, table_id)

parser = BatchParser()
parsed_results = parser.parse_batch()
parser.export_results(parsed_results, "requirements_dataset", "raw_chunks")

# ==========================================
# 🔹 Layer 2 – Requirement Registry
# ==========================================
class RequirementBuilder:
    def __init__(self, model="mock-llm"):
        self.model = model

    def build_registry(self, raw_reqs, batch_size=2):
        structured = []
        for i, r in enumerate(raw_reqs):
            structured.append({
                "requirement_id": f"REQ-{i+1}",
                "title": r.split()[0],
                "statement": r,
                "priority": "Medium",
                "severity": "High"
            })
        return structured

builder = RequirementBuilder()
raw_reqs = [c for chunks in parsed_results.values() for c in chunks]
structured_reqs = builder.build_registry(raw_reqs)
safe_export(structured_reqs, "requirements_dataset", "requirements")

with open("structured_requirements.json", "w") as f:
    json.dump(structured_reqs, f, indent=2)

# ==========================================
# 🔹 Layer 3 – Metadata Enrichment
# ==========================================
class MetadataEnricher:
    def enrich(self, reqs):
        enriched = []
        for r in reqs:
            r["domain"] = "Security" if "encrypt" in r["statement"].lower() else "Access Control"
            r["compliance"] = "HIPAA"
            enriched.append(r)
        return enriched

enricher = MetadataEnricher()
enriched_reqs = enricher.enrich(structured_reqs)
safe_export(enriched_reqs, "requirements_dataset", "enriched_requirements")

with open("enriched_requirements.json", "w") as f:
    json.dump(enriched_reqs, f, indent=2)

# ==========================================
# 🔹 Layer 4 – Categorization & Retrieval
# ==========================================
class CategorizerRetriever:
    def process(self, reqs):
        categorized = []
        for r in reqs:
            r["category"] = "Authentication" if "auth" in r["statement"].lower() else "Security"
            r["embedding"] = [0.1, 0.2, 0.3]  # mock vector
            categorized.append(r)
        return categorized

cr = CategorizerRetriever()
categorized_reqs = cr.process(enriched_reqs)
safe_export(categorized_reqs, "requirements_dataset", "requirements")

# ==========================================
# 🔹 Layer 5 – Test Case Generation
# ==========================================
class TestCaseGenerator:
    def batch_generate(self, reqs):
        test_cases = []
        for r in reqs:
            for t_type in ["Positive", "Negative", "Edge"]:
                test_cases.append({
                    "test_id": f"{r['requirement_id']}_{t_type}",
                    "requirement_id": r["requirement_id"],
                    "title": f"{t_type} test for {r['title']}",
                    "description": f"{t_type} scenario for {r['statement']}",
                    "steps": ["Step 1", "Step 2"],
                    "expected_result": "Expected outcome",
                    "priority": r["priority"],
                    "severity": r["severity"]
                })
        return test_cases

tcg = TestCaseGenerator()
test_cases = tcg.batch_generate(categorized_reqs)
safe_export(test_cases, "requirements_dataset", "test_cases")

with open("test_cases.json", "w") as f:
    json.dump(test_cases, f, indent=2)

# ==========================================
# 🔹 Layer 6 – Coverage Validation
# ==========================================
class CoverageValidator:
    def build_traceability_matrix(self, reqs, test_cases):
        matrix = []
        for r in reqs:
            linked = [t for t in test_cases if t["requirement_id"] == r["requirement_id"]]
            status = "Covered" if len(linked) >= 3 else "Missing"
            matrix.append({
                "requirement_id": r["requirement_id"],
                "coverage_status": status,
                "coverage_percent": 100 if status=="Covered" else 0,
                "coverage_gaps": [] if status=="Covered" else ["Needs more test cases"]
            })
        return matrix

cv = CoverageValidator()
trace_matrix = cv.build_traceability_matrix(categorized_reqs, test_cases)
safe_export(trace_matrix, "requirements_dataset", "traceability_matrix")

pd.DataFrame(trace_matrix)
