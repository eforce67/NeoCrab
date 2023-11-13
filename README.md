# NeoCrab: An Advanced Discord AI Chatbot

Welcome to **NeoCrab**, an innovative project developed by @eforce67. NeoCrab is a Discord AI chatbot that leverages the power of the Langchain AI framework. It's implemented using Py-cord, a modern, easy-to-use, feature-rich, and async-ready API wrapper for Discord written in Python.

> **Compatibility:** The scripts included in this project have been tested and confirmed to be compatible with Python 3.10 and above. Please note that compatibility with versions below Python 3.10 has not been verified and therefore is not guaranteed.

## File Descriptions

This project consists of several key scripts:

- [neo.py](./neo.py): This script is the heart of the project. It runs the Discord bot, enabling it to interact with users on the platform.
- [model.py](./model.py): This script is responsible for running the AI model. It's designed to facilitate interactive and engaging conversations with the AI.
- [embed.py](./embed.py): This script is a utility tool that generates embeddings for various file types. These embeddings are supported and can be utilized within the code.

## Key Features

NeoCrab is equipped with a range of exciting features:

- **Lang-chain Agent**: The Lang-chain agent is a powerful tool that comes with a wide array of functionalities. You can add more tools and customize its capabilities by modifying the model.py file.
- **Embedding Script**: The project includes an embedding script, which is based on the script found at this link [click here for embeddings code][./embeds.py].
- **Discord Bot Typing Display**: This feature enhances the user experience by displaying a typing animation for the bot on Discord, making the interaction feel more natural and engaging.
- **Conversation Memory**: One of the standout features of NeoCrab is its ability to remember previous conversations. It does this by summarizing all previous interactions, which allows for more coherent and continuous conversations.

> [!Important Note]
> It's crucial to customize the model.py file according to your requirements. Additionally, you should also modify your document files located in the `source_document` directory and the database where your embeddings are created and stored.
> The script is designed to handle multiple files in the `source_document` directory. You can add as many files as you want, and the script will combine all the data into a single database. This feature allows for a more comprehensive and robust database for your project.
