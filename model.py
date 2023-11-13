#!/usr/bin/env python3
# Standard Library Imports
import io
import json
from typing import Any

import msgspec
#import os
#from datetime import datetime
import yaml
# Third-Party Imports
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings import OllamaEmbeddings
from langchain.llms.ollama import Ollama
from langchain.memory import (ChatMessageHistory,
                              ConversationSummaryBufferMemory)
from langchain.prompts import PromptTemplate
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.vectorstores.chroma import Chroma

# Constants for config keys
MODEL = 'model'
MAIN_TEMPLATE = 'main_template'
QA_TEMPLATE = 'qa_template'
TEMPERATURE = 'temperature'
TFS_Z = 'tfs_z'
TOP_P = 'top_p'
TOP_K = 'top_k'
VERBOSE = 'verbose'
PERSIST_DIRECTORY = 'directory'

def parse_config(config_file_path):
    with io.open(config_file_path, 'r', encoding='utf-8') as config_file:
        print('Loading config...')
        return yaml.safe_load(config_file)

'''def generation_test():
    def question_answered(query):
        return qa_chain(query)
    # Load config
    config = parse_config('./resources/config.yml')

    # Extract config values
    model = config.get(MODEL)
    main_template = config.get(MAIN_TEMPLATE)
    qa_template = config.get(QA_TEMPLATE)
    temperature = float(config.get(TEMPERATURE))
    tfs_z = float(config.get(TFS_Z))
    top_p = float(config.get(TOP_P))
    top_k = float(config.get(TOP_K))
    verbose = config.get(VERBOSE)
    persist_directory = config.get(PERSIST_DIRECTORY)

    # Large language model initialization
    llm = Ollama(
        model=model,
        temperature=temperature,
        tfs_z=tfs_z,
        top_p=top_p,
        top_k=top_k,
        verbose=verbose,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
    )

    # Create a memory chain
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key='chat_history',
        max_token_limit=200,
        verbose=True,
    )

    # Prompt template
    main_agent_template = PromptTemplate(
        input_variables=["input", "chat_history"],
        template=main_template,
    )
    qa_chain_template = PromptTemplate(
        input_variables=["question", "context"],
        template=qa_template,
    )

    # Load the vectorstore
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=OllamaEmbeddings(model=model)
    )

    # Allowed tools
    tools = [
        Tool(
            name="Search Fate Grand Order Knowledgebase",
            func=question_answered,
            description="""# Guide to Using the "Search Fate Grand Order Knowledgebase" Tool
## When to Use the Tool
1. Gameplay Questions: If you have any questions about the gameplay of Fate Grand Order, such as how to complete a certain level, the tool can be very useful. It can provide tips and strategies that can help you progress in the game.
2. Character Information: The tool can provide detailed information about the various characters in the game. If you want to know more about a character's abilities, backstory, or how to obtain them, this tool can provide that information.
3. Event Details: Fate Grand Order often has special events. If you're unsure about the details of an event, such as its duration, rewards, or specific requirements, the tool can provide this information.
4. Troubleshooting: If you're experiencing issues with the game, the tool might be able to provide a solution or workaround.

## When Not to Use the Tool
1. Non-Game Related Questions: The tool is specifically designed to answer questions related to Fate Grand Order. If you have questions that are not related to the game, it's better to use a general search tool.
2. Opinions or Subjective Questions: The tool is designed to provide factual information. It may not be able to provide satisfactory answers to questions that are based on personal opinions or preferences.
3. Up-to-the-Minute Information: While the tool is regularly updated, it may not have the most current information immediately after a new update or event is released in the game.

## Additional Tips
- Specificity Helps: When using the tool, try to be as specific as possible with your question. This can help the tool provide a more accurate and helpful response.
- Try Different Phrasing: If the tool doesn't provide a satisfactory answer on the first try, consider rephrasing your question. Sometimes, asking the question in a different way can yield better results.

Remember, the tool is there to assist you. Don't hesitate to use it whenever you need help with Fate Grand Order. Happy gaming!
            """,
        ),
    ]

    while True:
        query = input("\nQuery: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue
        # Question-answering retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            memory=memory,
            retriever=vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': 0.75}),
            chain_type_kwargs={"prompt": qa_chain_template},
            return_source_documents=True,
        )
        memory.chat_memory.add_user_message(query)
        
        # Create an agent_exe with initial chat history
        agent_exe = initialize_agent(
            llm=llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            prompt=main_agent_template,
            tools=tools,
            verbose=verbose,
            handle_parsing_errors=True,
        )
        result = agent_exe.run({'input': query, 'chat_history': memory.chat_memory.messages})

        print('ANSWER --->', result, '\n')
        memory.chat_memory.add_ai_message(str(result))

    split_file_name = persist_directory.split('/')
    folder_name = split_file_name[::-1][0]
    conversation_UUID = f'{folder_name}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
    print(conversation_UUID)

    try:
        # Read the data from the conversation file
        print(f'Reading {conversation_UUID} TXT content')
        with io.open(os.path.join('./resources/conversation', conversation_UUID), mode='r') as file:
            existing_data = ''.join(file.readlines()) + '\n'
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty dictionary
        with open(os.path.join('./resources/conversation', conversation_UUID), 'w+') as file:
            file.close()
        existing_data = ''

    # Now save the updated data by writing it into the conversation file
    with io.open(os.path.join('./resources/conversation', conversation_UUID), mode='w') as file:
        print('Now proceeding to dump the data')
        file.write(existing_data + memory.load_memory_variables({})['chat_history'])'''

def generation(question, memory_db, authorID):
    def question_answered(query):
        return qa_chain(query)
    # Load config
    config = parse_config('./resources/config.yml')

    # Extract config values
    model = config.get(MODEL)
    main_template = config.get(MAIN_TEMPLATE)
    qa_template = config.get(QA_TEMPLATE)
    temperature = float(config.get(TEMPERATURE))
    tfs_z = float(config.get(TFS_Z))
    top_p = float(config.get(TOP_P))
    top_k = float(config.get(TOP_K))
    verbose = config.get(VERBOSE)
    persist_directory = config.get(PERSIST_DIRECTORY)
    CONVERSATION_PATH = config.get('conv_folder', './resources/conversation/')

    # Large language model initialization
    llm = Ollama(
        model=model,
        temperature=temperature,
        tfs_z=tfs_z,
        top_p=top_p,
        top_k=top_k,
        verbose=verbose,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
    )

    # Prompt template
    main_agent_template = PromptTemplate(
        input_variables=["input", "chat_history"],
        template=main_template,
    )
    qa_chain_template = PromptTemplate(
        input_variables=["question", "context"],
        template=qa_template,
    )
    #retrieve_from_db = json.loads(json.dumps(memory_db))
    def decode(msg, type=Any):
        return msgspec.convert(json.loads(json.dumps(msgspec.to_builtins(msg))), type=type)
    
    retrieve_from_db = decode(memory_db)
    retrieved_messages = messages_from_dict(retrieve_from_db)
    retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
    
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        chat_memory=retrieved_chat_history,
        memory_key='chat_history',
        max_token_limit=200,
        verbose=True,
        )
        
    # Load the vectorstore
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=OllamaEmbeddings(model=model)
    )

    # Allowed tools
    tools = [
        Tool(
            name="Search Fate Grand Order Knowledgebase",
            func=question_answered,
            description="""# Guide to Using the "Search Fate Grand Order Knowledgebase" Tool
## When to Use the Tool
1. Gameplay Questions: If you have any questions about the gameplay of Fate Grand Order, such as how to complete a certain level, the tool can be very useful. It can provide tips and strategies that can help you progress in the game.
2. Character Information: The tool can provide detailed information about the various characters in the game. If you want to know more about a character's abilities, backstory, or how to obtain them, this tool can provide that information.
3. Event Details: Fate Grand Order often has special events. If you're unsure about the details of an event, such as its duration, rewards, or specific requirements, the tool can provide this information.
4. Troubleshooting: If you're experiencing issues with the game, the tool might be able to provide a solution or workaround.

## When Not to Use the Tool
1. Non-Game Related Questions: The tool is specifically designed to answer questions related to Fate Grand Order. If you have questions that are not related to the game, it's better to use a general search tool.
2. Opinions or Subjective Questions: The tool is designed to provide factual information. It may not be able to provide satisfactory answers to questions that are based on personal opinions or preferences.
3. Up-to-the-Minute Information: While the tool is regularly updated, it may not have the most current information immediately after a new update or event is released in the game.

## Additional Tips
- Specificity Helps: When using the tool, try to be as specific as possible with your question. This can help the tool provide a more accurate and helpful response.
- Try Different Phrasing: If the tool doesn't provide a satisfactory answer on the first try, consider rephrasing your question. Sometimes, asking the question in a different way can yield better results.

Remember, the tool is there to assist you. Don't hesitate to use it whenever you need help with Fate Grand Order. Happy gaming!
            """,
        ),
    ]
    # Question-answering retrieval chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.80}),
        chain_type_kwargs={"prompt": qa_chain_template},
        return_source_documents=True,
    )
    memory.chat_memory.add_user_message(question)
    
    # Create an agent_exe with initial chat history
    agent_exe = initialize_agent(
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        prompt=main_agent_template,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
    )
    result = agent_exe.run({'input': question, 'chat_history': memory.chat_memory.messages})
    memory.chat_memory.add_ai_message(str(result))
    
    with open(f"{CONVERSATION_PATH}{authorID}.json", 'wb') as file:
        file.write(msgspec.json.encode(messages_to_dict(memory.chat_memory.messages)))

    return result

if __name__ == "__main__":
    #generation_test()
    pass
