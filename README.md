Project Overview

  This project is an AI-powered pipeline designed to automate the generation of test cases from healthcare software requirements. It takes a source document
  (in this case, a PDF), extracts requirements, enriches them with metadata, and then uses a Large Language Model (LLM) to generate detailed, traceable test
  cases. The entire process is broken down into several distinct stages, with each Python script representing a step in the pipeline. The project heavily
  utilizes Google Cloud's Vertex AI for its AI capabilities and BigQuery for data storage.

  Data Flow and Pipeline Structure

  The project follows a clear, linear data flow. The JSON files you see are the outputs of each major stage, acting as the inputs for the next.

   1. Input Document (`data/Common_InsuranceReqs_FINAL.pdf`)
       * This is the source document containing the software requirements.

   2. Parsing (`batch_parser.py`) -> `requirements.json`
       * The pipeline starts by parsing the input PDF to extract raw, unstructured requirement statements.

   3. Structuring (`requirement_builder.py`) -> `structured_requirements.json`
       * The raw statements are fed into an LLM to be converted into a structured format with fields like title, priority, severity, actors, etc.

   4. Enrichment (`metadata_enricher.py`) -> `enriched_requirements.json`
       * The structured requirements are then enriched with more specific, domain-relevant metadata. This script uses the regulations.yaml file to identify
         and tag requirements with applicable healthcare regulations (like HIPAA, GDPR, etc.).

   5. Test Case Generation (`test_case_generator.py`) -> `test_cases.json`
       * The enriched requirements are used as prompts for the LLM to generate three types of test cases for each requirement:
           * Positive: "Happy path" scenarios.
           * Negative: Invalid input or failure scenarios.
           * Edge: Boundary or unusual condition scenarios.

   6. Validation (`semantic_validator.py` & `coverage_validator.py`)
       * The generated test cases are validated against the original requirements to ensure they are relevant and provide adequate coverage.

  File-by-File Explanation

  Here’s a breakdown of what each file does:

  Core Python Scripts (The Pipeline)

   * batch_parser.py: This script is the starting point. It reads various document types (.pdf, .docx, etc.) from the data directory, extracts raw text, and
     identifies potential requirement statements. The output is a clean list of these statements in requirements.json.
   * requirement_builder.py: Takes the raw requirements and uses an LLM to transform them into a structured JSON format. This adds critical details like
     priority, severity, and acceptance criteria, making the requirements machine-readable and ready for the next steps.
   * metadata_enricher.py: This script adds a layer of domain-specific intelligence. It analyzes the structured requirements, identifies mentions of
     healthcare regulations listed in regulations.yaml, and normalizes key terms like actors and actions.
   * categorizer_retriever.py: This script serves two purposes. It uses an LLM to classify each requirement into a standard software category (e.g.,
     Functional, Security, Performance). It also generates vector embeddings for each requirement, which are numerical representations used for semantic
     search and retrieval.
   * test_case_generator.py: This is the core of the final output. It takes the enriched requirements and uses them to prompt an LLM to generate detailed,
     structured test cases.
   * semantic_validator.py: After test cases are created, this script uses an LLM to verify that each test case logically and semantically matches the intent
     of its parent requirement.
   * coverage_validator.py: This script provides a high-level view of test coverage. It generates a traceability matrix to identify which requirements are
     covered by test cases and, more importantly, which are not (coverage gaps).
   * retriever_bq.py: A utility script for retrieving requirements from a BigQuery database using semantic (vector-based) search. This is useful for finding
     similar requirements or for querying the requirement database in a more intelligent way.

  Data and Configuration Files

   * requirements.json: The output of the parsing stage. Contains a list of raw, unstructured requirement statements extracted from the source document.
   * structured_requirements.json: The output of the structuring stage. Contains the requirements in a detailed, structured JSON format.
   * enriched_requirements.json: The output of the enrichment stage. This is the most detailed version of the requirements, containing everything from the
     structured step plus the added metadata and regulation info.
   * test_cases.json: The final output of the generation pipeline, containing a list of detailed test cases ready for a QA team or an automated testing
     framework.
   * parsed_data.json: This file is currently empty but was likely intended to store intermediate parsed data.
   * regulations.yaml: A simple configuration file that lists all the healthcare-related regulations and standards the system should be aware of.
   * data/Common_InsuranceReqs_FINAL.pdf: The input document for the entire process.

  Other Files

   * automated_test_case.ipynb: A Jupyter Notebook that was likely used for developing, testing, and running the pipeline interactively.
   * TODO.md: A markdown file to keep track of pending tasks and future improvements for the project.
   * __pycache__/ and .ipynb_checkpoints/: These are auto-generated directories containing cached files and checkpoints to speed up execution and for
     recovery. They are not part of the core application logic.