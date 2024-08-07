import re
import yaml
from pathlib import Path
from collections import defaultdict


def count_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(re.findall(r'^##\s', content, re.MULTILINE))


def generate_index():
    docs_dir = Path("docs")
    index_path = docs_dir / "index.md"

    with open(index_path, "w", encoding='utf-8') as f:
        f.write("# ArXiv Tracker\n\n")
        f.write("欢迎来到 ArXiv Tracker. 这里跟踪了一些领域的最新研究进展:\n\n")

        for domain in sorted(docs_dir.iterdir()):
            if domain.is_dir():
                domain_name = domain.name
                all_files = list(domain.rglob("*.md"))

                def sort_key(file_path):
                    parts = file_path.relative_to(domain).parts
                    y = int(parts[0])
                    m = int(re.search(r'\d+', parts[1])[0])
                    return -y, -m

                sorted_files = sorted(all_files, key=sort_key)[:5]

                if sorted_files:
                    latest_file = sorted_files[0]
                    latest_rel_path = latest_file.relative_to(docs_dir)
                    f.write(f"## [{domain_name}]({latest_rel_path.as_posix()})\n\n")
                else:
                    f.write(f"## {domain_name}\n\n")

                f.write("Latest updates:\n\n")

                for file in sorted_files:
                    rel_path = file.relative_to(docs_dir)
                    year, month = rel_path.parts[1], rel_path.stem
                    display = f"{year}/{month}"
                    f.write(f"- [{display}]({rel_path.as_posix()})\n")
                f.write("\n")


def update_nav():
    docs_dir = Path("docs")
    nav = [{"Home": "index.md"}]

    for domain in sorted(docs_dir.iterdir()):
        if domain.is_dir():
            domain_name = domain.name
            domain_nav = {domain_name: []}

            article_counts = defaultdict(int)
            for file in domain.rglob("*.md"):
                year_month = f"{file.parent.name}-{file.stem}"
                article_counts[year_month] += count_articles(file)

            sorted_items = sorted(article_counts.items(), key=lambda x: x[0], reverse=True)

            for year_month, count in sorted_items:
                year, month = year_month.split('-')
                rel_path = f"{domain_name}/{year}/{month}.md"
                display = f"{year}-{month}({count})"
                domain_nav[domain_name].append({display: rel_path})

            nav.append(domain_nav)

    with open("mkdocs.yml", "r") as f:
        mkdocs_config = yaml.safe_load(f)

    mkdocs_config["nav"] = nav

    with open("mkdocs.yml", "w") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False)


if __name__ == "__main__":
    generate_index()
    update_nav()
