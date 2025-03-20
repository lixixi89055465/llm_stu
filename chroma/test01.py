# !pip install --upgrade openai
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def extract_text_from_pdf(filename,  #
                          page_numbers=None,  #
                          min_line_length=1):
    '''
    从pdf文件中（按指定页码）提取文字
    '''
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    ¬

    pass


paramgraphs = extract_text_from_pdf(
    "llama2.pdf",
    page_numbers=[2, 3],
    min_line_length=10
)
