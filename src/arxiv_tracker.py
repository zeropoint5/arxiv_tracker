import yaml

import arxiv

from src.database import Database
from src.llm_summarizer import LLMSummarizer
from src.markdown_generator import MarkdownGenerator
from src.prepare_mkdocs import generate_index, update_nav


class ArxivTracker:
    def __init__(self):
        self.config = self.load_config()
        self.db = Database(self.config["DB_PATH"])
        self.summarizer = LLMSummarizer()
        self.md_generator = MarkdownGenerator(self.db)
        self.arxiv_client = arxiv.Client()

    def load_config(self):
        with open('arxiv_conf.yml', 'r') as file:
            return yaml.safe_load(file)

    def run(self):
        for domain, queries in self.config["DOMAINS"].items():
            for query in queries:
                self.process_keyword(domain, query)

        self.md_generator.generate_all_markdowns(self.db)
        generate_index()
        update_nav()

    def process_keyword(self, domain, query):
        search = arxiv.Search(
            query=query,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        results = list(self.arxiv_client.results(search))
        for i, result in enumerate(results):
            if not self.db.article_exists(result.entry_id):
                print(f"Processing {i + 1}/{len(results)}: {result.title}")
                llm_summary = self.summarizer.summarize(result.summary)
                self.db.insert_article(result, domain, llm_summary)
