import os
import re

import dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

dotenv.load_dotenv()

ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")

API_KEY = os.getenv('OPENAI_API_KEY')
API_BASE = os.getenv('OPENAI_API_BASE')

glm4_flash = ChatZhipuAI(model="GLM-4-Flash", temperature=0.2)
glm4_air = ChatZhipuAI(model="GLM-4-Air", temperature=0.2)
glm4 = ChatZhipuAI(model="GLM-4", temperature=0.7, max_tokens=99999999)

gpt4o = ChatOpenAI(api_key=API_KEY, base_url=API_BASE, model="gpt-4o", temperature=0.7)


class MarkdownOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        # 使用正则表达式去掉首尾的 ```markdown 标记
        md_content = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
        md_content = re.sub(r'\s*```$', '', md_content, flags=re.MULTILINE)
        return md_content


str_parser = StrOutputParser()
md_parser = MarkdownOutputParser()
