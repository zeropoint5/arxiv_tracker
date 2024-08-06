import os


class MarkdownGenerator:
    def __init__(self, db):
        self.db = db

    def generate_all_markdowns(self, db):
        domains = db.get_all_domains()
        months = db.get_all_months()

        for domain in domains:
            for month in months:
                year, month = month.split('-')
                articles = db.get_articles_by_month(domain, year, month)
                if articles:
                    self.generate_markdown(domain, year, month, articles)

    def generate_markdown(self, domain, year, month, articles):
        directory = f"docs/{domain}/{year}"
        os.makedirs(directory, exist_ok=True)

        filename = f"{directory}/{month}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {domain} - {year}年{month}月\n\n")

            for article in articles:
                f.write(f"## [{article[2]}]({article[7]})\n\n")
                f.write(f"发布时间：{article[4]}\n\n")
                f.write(f"作者：{article[3]}\n\n")
                f.write(f"{article[6]}\n\n")
                f.write("---\n\n")
