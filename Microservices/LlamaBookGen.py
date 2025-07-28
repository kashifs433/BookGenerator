import os, sys
microservice_dir = os.path.abspath(os.path.dirname(__file__))
if microservice_dir not in sys.path:
    sys.path.append(microservice_dir)

from ConfigReader import ConfigReader
from gpt4all import GPT4All

LlamaModelName = ConfigReader.get_value("LlamaModelConfig", "GPT4All", "ModelName")
LlamaDevice = ConfigReader.get_value("LlamaModelConfig", "GPT4All", "device")
Llama_n_threads = ConfigReader.get_value("LlamaModelConfig", "GPT4All", "n_threads")
Llama_max_token = ConfigReader.get_value("LlamaModelConfig", "GPT4All", "max_tokens")
Llama_Prompt = ConfigReader.get_value("LlamaModelConfig", "GPT4All", "Prompt")
LlamaFolderPath = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "LlamaModels",LlamaModelName))

EmptyStructure = """{
    "BookName": "<Name for the book>",
    "Text_Description_Book_Cover_Image": "<Suggestion for the Book Cover>",
    "Chapters": [{
        "Chapter_Number": "<Number of the Chapter>",
        "Chapter_Title": "<Title of the Chapter>",
        "Chapter_Content": "<Content of the Chapter>"
    },...]
}"""

class GenerativeBookGen:


    @staticmethod
    def BookGen(Book_Type,Book_Description,Book_Chapter_count):
        ReplacedPrompt = str(Llama_Prompt).replace("{Book_Type}", Book_Type).replace("{Book_Description}",Book_Description).replace("{Book_Chapter_count}", Book_Chapter_count)
        Prompt = ReplacedPrompt +"\n"+ EmptyStructure

        model = GPT4All(model_name=LlamaFolderPath, device=LlamaDevice, n_threads=int(str(Llama_n_threads)))
        with model.chat_session() as se:
            Llama_Response = se.generate(Prompt, max_tokens=int(str(Llama_max_token)))
            return Llama_Response

