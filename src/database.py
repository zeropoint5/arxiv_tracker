import sqlite3

from arxiv import Result


class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT,
            domain TEXT,
            title TEXT,
            authors TEXT,
            published DATE,
            summary TEXT,
            llm_summary TEXT,
            url TEXT,
            primary_category TEXT,
            categories TEXT,
            pdf_url TEXT,
            is_related INTEGER DEFAULT 1,
            PRIMARY KEY (id, domain)
        )
        ''')
        self.conn.commit()

    def article_exists(self, entry_id, domain):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM articles WHERE id = ? AND domain = ?", (entry_id, domain))
        return cursor.fetchone() is not None

    def get_existing_summary(self, entry_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT llm_summary FROM articles WHERE id = ? LIMIT 1", (entry_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def insert_article(self, article: Result, domain, llm_summary, is_related=1):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO articles (id, domain, title, authors, published, summary, llm_summary, url, primary_category, categories, pdf_url, is_related)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article.entry_id,
            domain,
            article.title,
            ', '.join(author.name for author in article.authors),
            article.published.date(),
            article.summary,
            llm_summary,
            article.entry_id,
            article.primary_category,
            ', '.join(article.categories),
            article.pdf_url,
            is_related
        ))
        self.conn.commit()

    def get_articles_by_month(self, domain, year, month):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM articles
        WHERE domain = ? AND strftime('%Y-%m', published) = ? AND is_related = 1
        ORDER BY published DESC
        ''', (domain, f"{year}-{month}"))
        return cursor.fetchall()

    def get_all_domains(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT domain FROM articles")
        return [row[0] for row in cursor.fetchall()]

    def get_all_months(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%Y-%m', published) FROM articles ORDER BY published DESC")
        return [row[0] for row in cursor.fetchall()]
