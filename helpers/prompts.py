import sys
from yachalk import chalk
# sys.path.append("..")

import json
import ollama.client as client


def extractConcepts(prompt: str, metadata={}, model="qwen-turbo"):
    SYS_PROMPT = (
        "Your task is extract the key concepts (and non personal entities) mentioned in the given context. "
        "Extract only the most important and atomistic concepts, if  needed break the concepts down to the simpler concepts."
        "Categorize the concepts in one of the following categories: "
        "[event, concept, place, object, document, organisation, condition, misc]\n"
        "Format your output as a list of json with the following format:\n"
        "[\n"
        "   {\n"
        '       "entity": The Concept,\n'
        '       "importance": The concontextual importance of the concept on a scale of 1 to 5 (5 being the highest),\n'
        '       "category": The Type of Concept,\n'
        "   }, \n"
        "{ }, \n"
        "]\n"
    )
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result


def graphPrompt(input: str, metadata={}, model="zephyr:latest"):
    if model == None:
        model = "zephyr:latest"
    print("3")
    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

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
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        "   }, {...}\n"
        "]"
    )

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result

# print(graphPrompt("3D S CENE GEOMETRY ESTIMATION FROM 360◦IMAGERY :\n\nA S URVEY\n\nThiago L. T. da Silveira, Paulo G. L. Pinto, Jeffri E. M. Llerena, Cláudio R. Jung\n\nInstitute of Informatics, Federal University of Rio Grande do Sul, Brazil\n\n{tltsilveira, paulo.pinto, jeffri.mllerena, crjung}@inf.ufrgs.br\n\nABSTRACT\n\nThis paper provides a comprehensive survey on pioneer and state-of-the-art 3D scene geometry\n\nestimation methodologies based on single, two, or multiple images captured under the omnidirectional\n\noptics. We first revisit the basic concepts of the spherical camera model, and review the most common\n\nacquisition technologies and representation formats suitable for omnidirectional (also called 360◦,\n\nspherical or panoramic) images and videos. We then survey monocular layout and depth inference\n\napproaches, highlighting the recent advances in learning-based solutions suited for spherical data.\n\nThe classical stereo matching is then revised on the spherical domain, where methodologies for\n\ndetecting and describing sparse and dense features become crucial. The stereo matching concepts are\n\nthen extrapolated for multiple view camera setups, categorizing them among light fields, multi-view\n\nstereo, and structure from motion (or visual simultaneous localization and mapping). We also compile\n\nand discuss commonly adopted datasets and figures of merit indicated for each purpose and list recent\n\nresults for completeness. We conclude this paper by pointing out current and future trends."))
