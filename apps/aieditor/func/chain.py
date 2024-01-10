from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import LLMChain

from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import MessagesPlaceholder

import os
from dotenv import find_dotenv, load_dotenv
import openai
import google.generativeai as genai


# _ = load_dotenv(find_dotenv())  # read local .env file
# openai.api_key = os.environ["OPENAI_API_KEY"]


class ScriptAssistant:
    def __init__(self, llm_name):
        # 번역하는 프롬프트 템플릿
        self.translate2ko_prompt = (
            "Please translate text below into Korean. \n text: {text}"
        )
        self.translate2en_prompt = (
            "Please translate text below into English. \n text: {text}"
        )

        # sub topic 생성하는 프롬프트 템플릿
        # input: main topic
        self.subtopics_prompt = """
        I am planning to run a YouTube channel about {main topic}.
        I'm looking to create a chronological content series about {main topic}.

        Video main topic: I plan to make a YouTube video on the topic '{main topic}'

        Request: Please just write 10 detailed titles (sub-titles) for the above topic. Line break only once.
        output format = n. sub titles
        """

        # 스크립트 생성하는 프롬프트 템플릿
        # inputs: n, main topic, sub topic list

        # GPT ( 버전 : gpt-3.5-turbo-1106 / gpt 4)
        self.gpt_script_prompt = """
        I am planning to create a YouTube video with the main and detailed topics below.
        Write a video script
        First, please write only the script for detailed topic number {n}.

        Video main topic
        : {main topic}

        video details topic

        {sub topic list}

        Writing guide

        1. Don't say hello to the channel
        2. Don’t distinguish between scenes (don’t even write scene distinction phrases)
        3. I also distinguish between intro and body text (don’t even write the text).
        4. Just write the script
        5. Please write as long as possible
        """

        # Gemini
        self.gemini_script_prompt = """

        Your mission is to create a script that will be used for video production.
        Describe a story about the main and sub-topics.
        I've marked the technical facts as technical fact sheet.

        main topic: {main topic}
        sub topics: 
        {sub topic list}

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
        9. I don't even write anything that describes the scene. \
        10. Do not separate chapters. \
        11. no : do not ask questions \
        12. Write a paragraph by sub-title. \
        13. Run a line change after each sentence.    \
        14. Even clauses or examples are not presented as a list, but are written in a tightrope.    \

        Just write about subtopic number {n}.
        Write a lot of length with a string.

        output format = n. sub_topics \n text
        {human_input}
        """

        # Chat model 선택
        if llm_name == "gpt":
            self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-0301", temperature=1)
            self.subtopics_prompt_ = self.subtopics_prompt
            self.script_prompt_ = self.gpt_script_prompt
        elif llm_name == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=1,
                convert_system_message_to_human=True,
                # client=safety_settings,
            )
            self.subtopics_prompt_ = self.subtopics_prompt
            self.script_prompt_ = self.gemini_script_prompt
        else:
            raise ValueError(
                "Invalid llm_name. Supported values are 'gpt' and 'gemini'."
            )

        self.subtopics_prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful helper who knows a lot of interesting topics for YouTube videos.",
                ),  # simple
                ("user", self.subtopics_prompt_),
            ]
        )

        self.script_prompt_template = ChatPromptTemplate.from_messages(
            [
                # ("system", "You are a helpful assistant in writing YouTube scripts."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", self.script_prompt_),
            ]
        )

        self.translate2ko_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("user", self.translate2ko_prompt),
            ]
        )
        self.translate2en_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("user", self.translate2en_prompt),
            ]
        )

        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=800,
            memory_key="chat_history",  # 프롬프트의 input variable과 같은 이름
            return_messages=True,
            input_key="human_input",
        )

        # sub 주제 생성 chain - 메모리 X
        self.generate_subtopics_chain = LLMChain(
            llm=self.llm,
            prompt=self.subtopics_prompt_template,
            # verbose=True,
            # memory=memory   ###
        )

        # script 생성 chain - 메모리 O
        self.generate_script_chain = LLMChain(
            llm=self.llm,
            prompt=self.script_prompt_template,
            # verbose=True,
            memory=self.memory,  ###
        )

        # translate chain - 메모리 X
        self.translate_chain = LLMChain(
            llm=ChatGoogleGenerativeAI(  ########
                model="gemini-pro", temperature=0, convert_system_message_to_human=True
            ),
            prompt=self.translate2ko_prompt_template,
        )

        self.ko2en_generate_subtopics_chain = (
            self.translate2en_prompt_template | self.generate_subtopics_chain
        )

        self.script_chain = self.generate_script_chain | self.translate_chain

    def make_subtopics(self, user_input):
        self.en_result = self.ko2en_generate_subtopics_chain.invoke(
            {"text": user_input}
        )
        self.en_list = list(
            map(lambda x: x.strip(), self.en_result["text"].split("\n"))
        )

        self.ko_result = self.translate_chain.invoke({"text": self.en_result["text"]})
        self.ko_list = list(
            map(lambda x: x.strip(), self.ko_result["text"].split("\n"))
        )

        return self.ko_list

    def select_subtopics(self, selected_idx):
        self.en_selected_list = [self.en_list[i - 1] for i in selected_idx]
        return self.en_selected_list

    def make_scripts(self, user_input, selected_list, n):
        self.selected_list_reset_index = list(
            map(
                lambda x, i: str(i) + "." + x.split(" ", 1)[1],
                self.en_selected_list,
                range(1, len(self.en_selected_list) + 1),
            )
        )

        self.data = {
            "human_input": "",
            "n": n,  ### 반복문 돌릴 거임
            "main topic": user_input,
            "sub topic list": self.selected_list_reset_index,
        }
        self.ko_script = self.script_chain.invoke(self.data)
        return self.ko_script["text"]
