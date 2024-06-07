import autogen

# Api key setup
import os
from dotenv import load_dotenv
load_dotenv('api.env') 
api_key = os.getenv('OPENAI_API_KEY')

# Configuration for LLM
config_list = [
    {
        'model': 'gpt-4o',
        'api_key': api_key,
    }
]

llm_config = {
    # 'request_timeout': 600,
    'seed': 42,
    'config_list': config_list,
    'temperature': 0
}

assistant = autogen.AssistantAgent(
    name='Genie',
    llm_config=llm_config,
    system_message='You are Genie who can assist for the questions in container shipping domains.'
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "agent_work_dir", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = '''
Give me a summary of this article: https://dcsa.org/standards/just-in-time-port-call
'''

user_proxy.initiate_chat(
    assistant,
    message=task
)