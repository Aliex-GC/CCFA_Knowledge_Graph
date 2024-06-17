from langchain_community.llms import Tongyi
from langchain_community.llms import OpenAI

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    PromptTemplate,
)
import os
import sys
from yachalk import chalk
sys.path.append("..")
import json



OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


os.environ['OPENAI_API_BASE'] = 'https://gtapi.xiaoerchaoren.com:8932/v1'


# os.environ["DASHSCOPE_API_KEY"] = "sk-a75f6dd4715c40c0a2b3c909e67016d1"
llm = chat_model = ChatOpenAI(openai_api_key = OPENAI_API_KEY, openai_api_base = os.environ['OPENAI_API_BASE'], max_tokens=4096)


def TYgraphPrompt(prompt: str, metadata={}, model="gpt-4"):
    SYS_PROMPT = (
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        "Format your output as a list of json. Each element of the list contains a pair of terms"
        "and the relation between them, like the follwing: \n"
        "[\n"
        "   {{\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        "   }}, {{...}}\n"
        "]"
        "context: ```{input}``` \n\n output: "
    )

    A_prompt = PromptTemplate(
        template=SYS_PROMPT,
        input_variables=["input"],
    )

    chain = LLMChain(llm=llm, prompt=A_prompt)

    # response = chain.invoke(prompt).get("text", "")
    response = chain.invoke(prompt).get("text", "").replace('```json', '').replace('```', '').strip()

    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result

#print(TYgraphPrompt("3D S CENE GEOMETRY ESTIMATION FROM 360◦IMAGERY :\n\nA S URVEY\n\nThiago L. T. da Silveira, Paulo G. L. Pinto, Jeffri E. M. Llerena, Cláudio R. Jung\n\nInstitute of Informatics, Federal University of Rio Grande do Sul, Brazil\n\n{tltsilveira, paulo.pinto, jeffri.mllerena, crjung}@inf.ufrgs.br\n\nABSTRACT\n\nThis paper provides a comprehensive survey on pioneer and state-of-the-art 3D scene geometry\n\nestimation methodologies based on single, two, or multiple images captured under the omnidirectional\n\noptics. We first revisit the basic concepts of the spherical camera model, and review the most common\n\nacquisition technologies and representation formats suitable for omnidirectional (also called 360◦,\n\nspherical or panoramic) images and videos. We then survey monocular layout and depth inference\n\napproaches, highlighting the recent advances in learning-based solutions suited for spherical data.\n\nThe classical stereo matching is then revised on the spherical domain, where methodologies for\n\ndetecting and describing sparse and dense features become crucial. The stereo matching concepts are\n\nthen extrapolated for multiple view camera setups, categorizing them among light fields, multi-view\n\nstereo, and structure from motion (or visual simultaneous localization and mapping). We also compile\n\nand discuss commonly adopted datasets and figures of merit indicated for each purpose and list recent\n\nresults for completeness. We conclude this paper by pointing out current and future trends."))
