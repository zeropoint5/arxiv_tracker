import time
from langchain_core.prompts import PromptTemplate
from src.langchain_toolkit import glm4_flash, glm4_air, gpt4o, str_parser


class LLMSummarizer:
    def __init__(self):
        pass

    def summarize(self, text):
        template = """
        请将以下论文摘要翻译成中文，并进行一句话总结，涉及到专业术语请翻译的同时在括号中保留原文：

        论文摘要：
        {text}
        
        请按以下格式返回内容：
        
        #### 中文摘要：
        (todo)
        
        #### 一句话总结：
        (todo)
        """

        prompt = PromptTemplate.from_template(template)

        def try_model(llm_model):
            try:
                chain = prompt | llm_model | str_parser
                start_time = time.time()
                res = chain.invoke({"text": text})
                elapsed_time = time.time() - start_time
                print(f"摘要生成时间：{elapsed_time:.2f} 秒")
                return res
            except Exception as e:
                print(f"{llm_model.__class__.__name__} 调用失败: {str(e)}")
                return None

        models = [glm4_flash, glm4_air, gpt4o]

        for model in models:
            response = try_model(model)
            if response:
                return response

        print("所有模型调用均失败")
        return ""


if __name__ == "__main__":
    summarizer = LLMSummarizer()
    sample_abstract = """
    This paper introduces a novel approach to image classification using deep learning techniques. 
    We propose a new architecture that combines convolutional neural networks with attention mechanisms 
    to improve accuracy on challenging datasets. Our method achieves state-of-the-art results on 
    ImageNet and CIFAR-100, demonstrating its effectiveness across various image classification tasks. 
    We also conduct extensive ablation studies to analyze the contribution of each component in our model.
    """
    summary = summarizer.summarize(sample_abstract)
    print(summary)
