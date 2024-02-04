# Urocure - Urology Chatbot

Urocure is a specialized chatbot designed for the field of urology. This Python project utilizes a Streamlit web app, allowing users to interact with the AI and ask questions related to urology. The chatbot is powered by RAG (Retrieval-Augmented Generation) and has been trained on a Chinese dataset containing over 2000 entries. The dataset is stored in MongoDB Atlas as a vector database.

## Features

- **Streamlit Web App:** User-friendly interface for interacting with the urology chatbot.
- **RAG Model:** Utilizes Retrieval-Augmented Generation for improved responses.
- **Chinese Dataset:** Trained on a diverse dataset of 2000+ entries in Chinese. Dataset link: [RJUA QADatasets](http://openkg.cn/dataset/rjua-qadatasets).
- **MongoDB Atlas:** Stores the dataset as a vector database for efficient retrieval.
- **Cloudflare Translation API:** Translates English requests to Chinese and vice versa.
- **CloudFlare Text Generation API:** Generates Text.
## How It Works

1. **User Prompt:** Users send their queries in English through the web app.
2. **Translation:** Cloudflare Translation API is used to translate the English request into Chinese.
3. **RAG Embeddings:** The translated request is passed through the RAG model to generate embeddings.
4. **Embedding Conversion:** Chinese embeddings are converted back to English based on prompt engineering.
5. **MongoDB Atlas Integration:** Utilizes MongoDB Atlas as a vector database for storing and retrieving the Chinese dataset.
6. **Streamlit Interface:** The user interacts with the chatbot through a user-friendly Streamlit web app.

## Setup

1. Clone the repository:


2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up MongoDB Atlas:

   - Create an account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a new cluster and obtain the connection string.
   - Update the connection string in `config.py`.

4. Set up Cloudflare Translation API:

   - Obtain an API key for Cloudflare Translation API.
   - Set the `CLOUDFLARE_API_KEY` environment variable.

5. Run the Streamlit web app:

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) to interact with Urocure.

## Configuration

- **ATLAS_CONNECTION_STRING:** Set the MongoDB Atlas connection string in `config.py`.
- **OPENAI_API_KEY:** Set the OpenAI API key in `.env` file.
- **CLOUDFLARE_API_KEY:** Set the Cloudflare API key in `.env` file.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to contribute and enhance the capabilities of Urocure!
