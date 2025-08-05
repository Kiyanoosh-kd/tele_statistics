from typing import Union
from pathlib import Path
import json
from src.data import DATA_DIR
from collections import Counter
from hazm import word_tokenize, Normalizer
from wordcloud import WordCloud
from loguru import logger
import matplotlib.pyplot as plt

class ChatStatistics:
    """Generates chat statistics from telegram chat json file
    """    
    #loads chat data and normalize them
    def __init__(self, chat_json: Union[str, Path]):
        """
        Args:
            chat_json (Union[str, Path]): Path to telegram export json file
        """        
        logger.info(f"Loading chat data from {chat_json}")
        self._raw_text_content = ''
        self.normalizer = Normalizer()
        with open(chat_json) as f:
            self.chat_data = json.load(f)
        for message in self.chat_data['messages']:
            if isinstance(message['text'], str):
                self._raw_text_content += f" {message['text']}"
        self._raw_text_content = self.normalizer.normalize(self._raw_text_content)
        
        with open(DATA_DIR / 'stopwords.txt') as f:
            stop_words = f.readlines()
        stop_words = [item[:-1] for item in stop_words]
        self.stop_words = list(map(self.normalizer.normalize,stop_words))

    # generates word cloud and save it to output file
    def generate_word_cloud(self, output_dir: Union[str, Path]):
        """Generates wordcloud from telegram chat and store in the output_dir

        Args:
            output_dir (Union[str, Path]): output directory address
        """
        logger.info("Generating wordcloud")
        self._tokenizer()
        self.text_content = (' ').join(self.tokens)
        self.word_cloud = WordCloud(background_color='white',
                          font_path= DATA_DIR / 'BHoma.ttf',max_font_size = 250).generate(self.text_content)
        self.word_cloud.to_file(Path(output_dir) / 'wordcloud.png')

    # tokenize text content
    def _tokenizer(self):
        self.raw_tokens = word_tokenize(self._raw_text_content)
        self.tokens = filter(lambda item: item not in self.stop_words, self.raw_tokens)

    #create a plot 
    def plotter(self):
        plt.imshow(self.word_cloud, interpolation='bilinear')
        plt.axis("off")


if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json = DATA_DIR / 'online.json')
    chat_stats.generate_word_cloud(DATA_DIR)
    print(chat_stats)