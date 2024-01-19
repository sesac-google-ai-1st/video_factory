from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import LLMChain

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class ScriptAssistant:
    def __init__(self, llm_name):
        # 번역하는 프롬프트
        self.translate2ko_prompt = "If the text below is in Korean, do nothing. If not, please translate it into Korean. There is no need to add an explanation. \n text: {text}"

        # main topic 생성하는 프롬프트
        # input: youtube topic
        self.maintopic_prompt = """
        <{youtube_topic}> 과 관련한 주제의 유튜브 채널을 운영 하려한다.
        <{youtube_topic}> 과 관련한 흥미롭고 재미있는 영상 주제를 10개 제안해줘.
        - 주제가 잘 드러나게 길게 작성해줘
        - 추가 설명 없이 주제만 작성해줘
        - "-" 표시 하지마
        - "*" 표시 하지마
        - 앞뒤에 아무말도 하지말고 딱 주제만 나열해줘
        """

        # sub topic 생성하는 프롬프트
        # input: youtube_topic, main_topic
        self.subtopics_prompt = """
        If my requirements below are in a language other than English, please translate it into English, think about it, and answer in English.

        I am planning to run a YouTube channel about <{youtube_topic}>.
        I'm looking to create a chronological content series about <{youtube_topic}>

        Video main topic: I plan to make a YouTube video on the main topic "{main_topic}".

        List up 10 detailed titles (subtitles) for the above topic in order, with only one line break.
        """

        # 스크립트 생성하는 프롬프트
        # inputs: n, main_topic, sub_topic_list

        # GPT ( 버전 : gpt-3.5-turbo-1106 / gpt 4)
        self.gpt_script_prompt = """
        I am planning to create a YouTube video with the main and detailed topics below.
        Write a video script
        First, please write only the script for detailed topic number {n}.

        Video main topic
        : {main_topic}

        video details topic

        {sub_topic_list}

        Writing guide

        1. Don't say hello to the channel
        2. Don’t distinguish between scenes (don’t even write scene distinction phrases)
        3. I also distinguish between intro and body text (don’t even write the text).
        4. Just write the script
        5. Use at least 800 characters.
        """

        # Gemini
        self.gemini_script_prompt = """
        Your mission is to create a script that will be used for video production.
        Describe a story about the main and sub-topics.
        I've marked the technical facts as technical fact sheet.

        main topic: {main_topic}
        sub topics: 
        {sub_topic_list}

        Technical specification:

        1. The difficult terminology is written as follows: \
        - "Aseptic reproduction" => "The ability to create offspring on one's own without any other individual" \
        2. Long and detailed description. \
        3. According to Tone and Manner, a script for knowledge transfer is written mainly by stories. \
        4. Focusing on stories and narratives, the contents are richly written, including historical backgrounds, events, etc. \
        5. Channel introduction and greetings are omitted at the start, and greetings are omitted at the end. \
        6. Exclude narrator and commentator phrases. \
        7. Do not write " and () and - and special characters. \
        8. Do not distinguish between scenes. \
        9. Do not  even write anything that describes the scene. \
        10. Do not separate chapters. \
        11. no : do not ask questions \
        12. Write a paragraph by sub-title. \
        13. Run a line change after each sentence.    \
        14. Even clauses or examples are not presented as a list, but are written in a tightrope.    \

        Just write about subtopic number {n}.
        Use at least 800 characters.

        output format = n. sub_topics \n text
        {human_input}
        """

        # Chat model 선택
        if llm_name == "GPT":
            self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-0301", temperature=1)
            self.script_prompt_ = self.gpt_script_prompt
        elif llm_name == "Gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=1,
                convert_system_message_to_human=True,
                # client=safety_settings,
            )
            self.script_prompt_ = self.gemini_script_prompt
        else:
            raise ValueError(
                "Invalid llm_name. Supported values are 'gpt' and 'gemini'."
            )

        # prompt templates
        self.maintopic_prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "당신은 YouTube 동영상에 대한 흥미로운 주제를 많이 알고 있는 유용한 도우미입니다.",
                ),
                HumanMessagePromptTemplate.from_template(self.maintopic_prompt),
            ]
        )

        self.subtopics_prompt_template = ChatPromptTemplate.from_template(
            self.subtopics_prompt
        )

        self.script_prompt_template = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(self.script_prompt_),
            ]
        )

        self.translate2ko_prompt_template = ChatPromptTemplate.from_template(
            self.translate2ko_prompt
        )

        # memory
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=800,
            memory_key="chat_history",  # 프롬프트의 input variable과 같은 이름
            return_messages=True,
            input_key="human_input",
        )

        # output parser
        self.output_parser = StrOutputParser()

        # chain
        # sub 주제 생성 chain
        self.maintopic_chain = LLMChain(
            llm=self.llm,
            prompt=self.maintopic_prompt_template,
            # verbose=True,
            output_key="text",
        )

        # sub 주제 생성 chain
        self.subtopic_chain = LLMChain(
            llm=self.llm,
            prompt=self.subtopics_prompt_template,
            # verbose=True,
            output_key="text",
        )

        # script 생성 chain - 메모리 O
        self.generate_script_chain = LLMChain(
            llm=self.llm,
            prompt=self.script_prompt_template,
            # verbose=True,
            memory=self.memory,  #
            output_key="text",
        )

        # translate chain
        self.translate_chain = (
            self.translate2ko_prompt_template
            | ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
        )
        # parsing을 위해 return 값 알아두기 : AIMessage(content='blah')

        self.script_chain = (
            self.generate_script_chain | self.translate_chain | self.output_parser
        )  # stream을 위해 output_parser 추가

    def make_maintopic(self, user_input):
        self.main_list = self.maintopic_chain.invoke({"youtube_topic": user_input})
        print(self.main_list)
        self.main_list = [  # 문자열을 줄바꿈으로 분리하고, 주제 이외는 다 제거함
            sen.split(".")[1].strip()
            for sen in self.main_list["text"].split("\n")
            if "." in sen
        ]
        return self.main_list

    def make_subtopics(self, user_input, main_topic):
        """주제를 입력받아, subtopic 리스트를 반환하는 함수입니다.

        subtopic_chain은 subtopic 영어 문자열을 반환합니다. (en_result)
        가끔 subtopic 이외의 말을 덧붙이거나 줄바꿈을 여러번하는 경우가 있기 때문에 리스트로 변환하는 과정에서 후처리를 해줍니다. (en_list)
        이를 translate_chain에 입력으로 넣으면, subtopic 한글 문자열을 반환합니다. (ko_result)
        마지막으로 subtopic 한글 문자열을 한글 리스트로 변환합니다. (ko_list)

        Args:
            user_input (str): 사용자가 input form에 입력한 영상 주제

        Returns:
            list: 한글 subtopic 리스트
        """
        self.en_result = self.subtopic_chain.invoke(
            {"youtube_topic": user_input, "main_topic": main_topic}
        )
        self.en_list = [  # 문자열에서 "n.~" 이외는 다 제거함
            sen.strip()
            for sen in self.en_result["text"].split("\n")
            if any(map(lambda x: x == ".", sen[1:3]))
        ]

        self.ko_result = self.translate_chain.invoke({"text": "\n".join(self.en_list)})

        self.ko_list = list(
            map(lambda x: x.strip(), self.ko_result.content.split("\n"))
        )
        ########번역 chain을 invoke 대신 batch를 사용##########
        # self.en_list_batch = list(map(lambda x: {"text": x}, self.en_list))
        # print(self.en_list_batch)
        # self.ko_list = self.translate_chain.batch(self.en_list_batch)
        #########시간을 측정해보니 더 오래걸림##########

        return self.ko_list

    def select_subtopics(self, selected_idx):
        """index를 받아서, index에 해당하는 subtopic을 반환하는 함수입니다.

        여기서 만든 en_selected_list는 변수로 저장되었다가, make_scripts 함수에 바로 입력됩니다.

        Args:
            selected_idx (list): 사용자가 화면에서 선택한 체크박스의 index 리스트

        Returns:
            list: 선택된 index에 해당하는 영어 subtopic을 담은 리스트
        """
        self.en_selected_list = [self.en_list[i - 1] for i in selected_idx]

        return self.en_selected_list

    def make_scripts(self, user_input, n):
        """주제와 몇번째 subtopic인지를 입력 받아서, 해당 subtopic에 맞는 script를 생성하는 함수입니다.

        위의 select_subtopic 함수에서 만든 en_selected_list의 번호를 다시 매겨준 후, (selected_list_reset_index)
        script chain에 input으로 집어넣습니다. 번호를 1번부터 다시 매겼기 때문에, n 번째 subtopic에 관한 script를 작성할 수 있습니다.
        각 subtopic마다 script를 생성하는 이유는, 풍부한 내용을 얻기 위한 것입니다.
        또한, 이전에 생성한 script 내용과 중복을 피하고, 문체의 일관성을 위해, script_chain에 memory를 사용하였습니다.

        Args:
            user_input (str): 사용자가 input form에 입력한 영상 주제
            n (str): 여러개의 subtopic 중 몇번째 subtopic에 관한 script를 작성할지 지정

        Returns:
            generator: script의 chunk를 담은 generator
        """
        self.selected_list_reset_index = list(
            map(
                lambda x, i: str(i) + "." + x.split(" ", 1)[1],
                self.en_selected_list,
                range(1, len(self.en_selected_list) + 1),
            )
        )

        self.data = {
            "human_input": "",
            "n": n,  # 반복문 돌리며 n번째 subtopic에 해당되는 script 생성
            "main_topic": user_input,
            "sub_topic_list": self.selected_list_reset_index,
        }

        return self.script_chain.stream(self.data)
