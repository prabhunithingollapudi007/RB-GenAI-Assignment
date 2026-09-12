# RB GenAI Data Science Evaluation

This repository evaluates paired human and AI answers to personal-care interview questions. It contains a reproducible preprocessing pipeline, semantic and lexical similarity scoring, exploratory notebooks, generated figures, and quantitative and qualitative reports.

## Quick Start

From the repository root:

```powershell
& ".venv\Scripts\python.exe" -m pip install -e "."
& ".venv\Scripts\python.exe" "scripts\run_analysis.py"
& ".venv\Scripts\python.exe" "scripts\run_semantic_analysis.py"
& ".venv\Scripts\python.exe" "reports\generate_report_figures.py"
& ".venv\Scripts\python.exe" -m unittest discover -s tests -v
```

The semantic stage downloads model weights on first run. The default embedding model is `sentence-transformers/all-mpnet-base-v2`.

## Project Structure

```text
data/
	raw/          Source workbook and assignment PDF
	processed/    Generated clean tables and analysis reports
src/
	rb_genai_analysis/  Reusable analysis package
scripts/              Runnable project scripts
notebooks/            Evaluation and visualization notebooks
reports/              Figures and submission reports
tests/                Automated smoke and schema tests
```

## Source Data

- Workbook: `data/raw/RB_GenAI_Datatest.xlsx`
- Sheet: `answer_pairs`
- Rows: 30
- Columns: `id`, `question_category`, `question`, `person_id`, `human_answers`, `ai_answers`

The analysis pairs each row into the following clean table:

`Person ID | Question Category | Question Text | Human Answer | AI Answer`

Whitespace is normalized in the clean table. Original workbook values are preserved in the source workbook.

## Deliverables

- [Quantitative analysis report](reports/quantitative_analysis_report.md): preprocessing and automatic evaluation findings with tables and figures.
- [Qualitative evaluation report](reports/Qualitative_Evaluation_Report.md): fact consistency, lifestyle congruence, style, holistic judgments, failure modes, and recommendations.
- [Two-page technical report source](reports/Technical_Report_2page.tex): business context, evaluation framework, headline results, implications, and recommendations in LaTeX format.
- [Evaluation report PDF](evaluation%20of%20human%20simulated%20responses.pdf): formatted report deliverable for review or submission.
- [Presentation slide deck](A-rigorous-method-to-know-when-our-generative-agents-can-be-trusted.pptx): presentation of the evaluation approach, findings, and recommendations.
- [Preprocessing notebook](notebooks/preprocessed_pipeline_analysis.ipynb): data quality and text-feature exploration.
- [Semantic notebook](notebooks/semantic_similarity_analysis.ipynb): cosine, BERTScore, ROUGE-L, distributions, correlations, and outliers.
- `data/processed/`: reproducible clean tables, row-level features, semantic scores, summaries, metadata, and artifact flags.

## Reproduce the Preprocessing Analysis

From the project directory, run:

```powershell
& ".venv\Scripts\python.exe" "scripts\run_analysis.py"
```

The runner imports the reusable pipeline from `src/rb_genai_analysis` and writes reports to `data/processed`.

The package can also be installed in editable mode with `python -m pip install -e .`.

## Semantic Similarity Analysis

Run the required semantic comparison:

```powershell
& ".venv\Scripts\python.exe" "scripts\run_semantic_analysis.py"
```

The script computes all three required metric families for each human/AI pair:

- Sentence-embedding cosine similarity using `sentence-transformers/all-mpnet-base-v2`.
- BERTScore precision, recall, and F1 using the package's default English model.
- ROUGE-L precision, recall, and F1 using stemmed token overlap.

Outputs are written to `data/processed`:

- `semantic_similarity_scores.csv`: All metric scores per paired response, with question metadata.
- `semantic_similarity_summary.csv`: Overall and question-category descriptive statistics for every metric.
- `semantic_similarity_metadata.json`: Model and metric provenance.

Scores measure semantic relatedness between paired answers. They should not be interpreted as factual correctness, answer quality, or agreement without additional evaluation criteria.


## Generated Files

All outputs are in `data/processed`:

- `paired_answers_clean.csv`: Clean paired table with the five requested fields.
- `response_level_metrics.csv`: Word, character, unique-word, lexical-diversity, language, and lifestyle metrics for every human and AI response.
- `response_statistics.csv`: Descriptive statistics and quantiles for response length, vocabulary, lexical diversity, and concrete/abstract term counts.
- `language_presence_statistics.csv`: Counts and percentages for concrete language, abstract language, and lifestyle-topic mentions.
- `missingness_report.csv`: Missing-value counts, percentages, and unique-value counts for each clean-table field.
- `quality_artifacts_report.csv`: Potential non-ASCII characters, repeated whitespace, and unusually long responses.
- `analysis_metadata.json`: Workbook structure, output dimensions, and analysis notes.

## Key Findings

- 30 human and 30 AI responses were analyzed.
- No missing values were found in the five clean-table fields.
- Human responses averaged 31.2 words; AI responses averaged 54.5 words.
- Concrete language was detected in 76.7% of human responses and 86.7% of AI responses.
- Abstract language was detected in 26.7% of human responses and 70.0% of AI responses.
- The quality report contains 21 flags, including non-ASCII characters and unusually long responses.

## Metric Definitions

- **Word count**: Number of regex-tokenized words.
- **Character count**: Number of characters after whitespace normalization.
- **Unique word count**: Number of distinct lowercased word tokens.
- **Lexical diversity**: `unique word count / word count`.
- **Concrete language**: Presence or count of terms from a small domain-specific lexicon covering products, brands, ingredients, stores, prices, packaging, and similar tangible references.
- **Abstract language**: Presence or count of terms from a small lexicon covering concepts such as convenience, quality, reliability, value, trust, and performance.
- **Lifestyle constraints**: Case-insensitive detection of travel, time, stress, and professional-image terms.

Concrete and abstract language results are heuristic lexicon-based indicators, not a full linguistic or semantic classification. Quality flags identify candidates for review; they do not automatically prove that a response is invalid.

## Methodology and Caveats

Use `data/processed/response_level_metrics.csv` for evaluation and visualization work. It is in long format, with one row per response and a `response_type` field distinguishing human from AI answers. Reusable functions are in `src/rb_genai_analysis/`.

The notebooks in `notebooks/` are ready to run with the project `.venv` kernel:

- `preprocessed_pipeline_analysis.ipynb`: preprocessing checks, missingness, response distributions, language indicators, artifacts, and category summaries.
- `semantic_similarity_analysis.ipynb`: cosine similarity, BERTScore, ROUGE-L, metric distributions, category comparisons, correlations, and pair outliers.

Concrete and abstract language indicators are transparent lexicon-based heuristics. Similarity metrics measure relatedness, contextual alignment, and ordered word overlap; they do not establish factual correctness, persona fidelity, or answer quality on their own. The dataset is small and category counts are uneven, so findings are descriptive rather than statistically powered.
