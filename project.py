import autogen
import dotenv

config_list = autogen.config_list_from_json("nritya_nirman\GROQ_CONFIG_LIST.json")

llm_config = {
    "temperature": 0.2,
    "config_list": config_list,
    "max_tokens": 1500,
}

user_proxy = autogen.UserProxyAgent(
    name = "Admin",
    system_message = "Admin. You are the admin of the group chat. You can initiate the chat and provide feedback to the agents.",
    code_execution_config = {
        "work_dir": None,
        "use_docker": False
    },
    human_input_mode = "TERMINATE",
)

with open("nritya_nirman\\rules_chakkar.txt", "r") as f:
    rules = f.read()
with open("nritya_nirman\Tukda.txt", "r") as f:
    tukda = f.read()
with open("nritya_nirman\Tihai.txt", "r") as f:
    tihai = f.read()
with open("nritya_nirman\SamSeSam.txt", "r") as f:
    samse = f.read()
with open("nritya_nirman\Chakkardar.txt", "r") as f:
    chakkardar = f.read()

tihai_composer = autogen.AssistantAgent(
    name = "TihaiComp",
    llm_config = llm_config,
    system_message = """Tihai Composer. You compose unique Kathak Tihais. Each beat must be separated by a pipe (|).
    Some examples of Kathak compositions: {tihai}. """.format(tihai=tihai),
)

tukda_composer = autogen.AssistantAgent(
    name = "TukdaComp",
    llm_config = llm_config,
    system_message = """Tukda Composer. You compose regular Kathak Tukdas only and nothing else. Each beat must be separated by a pipe (|).
    Some examples of Kathak compositions: {tukda}
    """.format(tukda=tukda),
)

chakkardar_composer = autogen.AssistantAgent(
    name = "ChakkardarComp",
    llm_config = llm_config,
    system_message = """Chakkardar Composer. You compose Kathak Chakkardar Tukdas only and nothing else. Each beat must be separated by a pipe (|).
    Some examples of Kathak compositions: {chakkardar}
    Take the feedback of the critic and make changes if needed. Respond to the critic.""".format(chakkardar=chakkardar),
)

samsesam_composer = autogen.AssistantAgent(
    name = "SamSeSamComp",
    llm_config = llm_config,
    system_message = """Chakkardar Composer. You compose Kathak SamSeSam Tukdas only and nothing else. Each beat must be separated by a pipe (|).
    Some examples of Kathak compositions: {samse}""".format(samse=samse),
)

critic = autogen.AssistantAgent(
    name = "Critic",
    llm_config = llm_config,
    system_message = """Critic. You check the compositions of the composer and provide feedback immediately. You cannot generate compositions.
    Some rules to be followed are {rules}""".format(rules=rules),
)

group_chat = autogen.GroupChat(
    agents = [user_proxy, tihai_composer, critic], messages = [], max_round=5, speaker_selection_method="round_robin"
)

manager = autogen.GroupChatManager(
    groupchat = group_chat, llm_config = llm_config
    )

user_proxy.initiate_chat(
    manager,
    message = """Generate a Tihai."""
    )

