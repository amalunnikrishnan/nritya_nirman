import autogen


groq_config_list = autogen.config_list_from_json("GROQ_CONFIG_LIST.json")
openai_config_list  = autogen.config_list_from_json("OAI_CONFIG_LIST.json")

groq_llm_config = {
    "temperature": 0.15,
    "config_list": groq_config_list,
    "max_tokens": 1800,
}

openai_llm_config = {
    "temperature": 0.15,
    "config_list": openai_config_list,
    "max_tokens": 800,
}

user_proxy = autogen.UserProxyAgent(
    name = "Admin",
    system_message = "Human Admin. Interact with the critics and provide suggestion to the composer. The process ends only if the critic approves.",
    human_input_mode = "NEVER",
    code_execution_config={"use_docker": False},
)

composer = autogen.ConversableAgent(
    name = "composer",
    system_message = """
    Composer. You create Kathak compositions and receive feedback from the critic.
    """,
    llm_config = openai_llm_config,
)

with open("Tihai.txt", "r") as tihai:
    tihai = tihai.read()

    
tihai_critic = autogen.ConversableAgent(
    name = "critic",
    llm_config = groq_llm_config,
    system_message = """Tihai critic. You help the composer think about the rules associated with a Kathak Tihai.
    You critic the composition and provide feedback to the composer. Your information should be constructive and help the Composer improve.
    Keep the following examples in mind while criticing the composition:
    {tihai}
    You cannot generate compostions.
    """.format(tihai=tihai)
)

group_chat = autogen.GroupChat(
    agents = [composer, tihai_critic, user_proxy], messages = [], max_round=8, speaker_selection_method='round_robin',
)

manager = autogen.GroupChatManager(
    groupchat = group_chat, llm_config = groq_llm_config
)

user_proxy.initiate_chat(
    manager,
    message = """
    Compose a Tihai.
    """
    )
