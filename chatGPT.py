from openai import OpenAI
import tiktoken
from rich import print
import os
from dotenv import load_dotenv

load_dotenv()
# API Key here
gpt_key = os.getenv("GPT_KEY")

# function to check tokens used; we don't want to use too much becuase expensive
def num_tokens_from_messages(messages, model="gpt-4o"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens  
    except Exception:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")
    

class GPTManager:
    def __init__(self):
        # token limit for 4o is reeeeeally huge, but we don't want to spend too much money
        # 8000 seems like enough context for now, might add a remembering function later
        # to store important information
        self.token_limit = 8000 
        self.chat_history = []
        # open API
        try:
            self.client = OpenAI(api_key=gpt_key)
        except TypeError:
            print("Error, you probably forgot the API key.")

    def chat(self, prompt=""):
        if(not prompt):
            print("Error! No prompt given!")
            return
        
        # Add prompt to history (formatted how gpt wants it)
        self.chat_history.append({"role": "user", "content": prompt})

        # Make sure message isn't too long, pop oldest messages otherwise
        print(f"[coral]***Current token length in history: {num_tokens_from_messages(self.chat_history)}***")
        while(num_tokens_from_messages(self.chat_history) > self.token_limit):
            self.chat_history.pop(1) # skip the system message
            print(f"Message removed, new length is {num_tokens_from_messages(self.chat_history)}")

        print("[yellow]Prompting GPT...")
        response = self.client.chat.completions.create(model="gpt-4o", messages=self.chat_history)

        # Append response to the chat history
        self.chat_history.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})

        # Display answer to user
        answer = response.choices[0].message.content
        print(f"[green]\n{answer} \n")
        return answer
    
# Quick debugging test
if __name__ == "__main__":
    gptManager = GPTManager()

    sys_prompt = {"role": "system", "content": "You are Spyro from the Spyro the Dragon video game series! You have 77 of the original 80 dragon eggs you are searching for! Answer the user's questions, and ask your own to figure out where the remaining eggs are hiding."}
    #user_prompt = {"role": "user", "content": "Hello Spyro, what are you looking for?"}

    gptManager.chat_history.append(sys_prompt)

    while(True):
        user_prompt = input("Write your chats here: ")
        gptManager.chat(user_prompt)





        



