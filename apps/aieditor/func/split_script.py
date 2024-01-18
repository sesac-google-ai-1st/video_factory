# kiwi 사용 이유:
# kss github에 따르면, 41문장을 분리할 때 Kiwi를 사용하면 36.26msce 소요. 이는 koalanlp OKT 다음으로 빠른 속도임.
# 또한, subtopic별로 script가 생성되는데,
# kiwi는 text인자를 str의 Iterable로 줄 경우, 멀티스레드로 분배하여 처리해줌

# !pip install --upgrade pip
# !pip install kiwipiepy

from kiwipiepy import Kiwi

kiwi = Kiwi()


def split_script2senteces(text_list):
    """생성된 script를 담은 리스트를 전달하면, 문장을 분리하는 함수입니다.
    text_list는 html의 textarea subtopic 요소의 value를 담고 있습니다. (ex. ["scirpt1", "script2"])
    각 script 별로 문장을 분리하고, 이를 하나의 list로 만들어 반환합니다.
    이는 자막 파일 생성과 TTS에 사용됩니다.
    이미지 생성을 위해선 번역 과정이 필요합니다.

    Args:
        text_list (list): 각 script 문자열을 담은 리스트 (ex. ["scirpt1", "script2"])

    Returns:
        list: 문장으로 분리된 전체 script를 담은 리스트 (ex. ["sen1", "sen2", "sen3", ...])
    """
    splited_iterable = kiwi.split_into_sents(text_list)
    flattened_list = [
        sentence.text for sublist in splited_iterable for sentence in sublist
    ]

    return flattened_list
