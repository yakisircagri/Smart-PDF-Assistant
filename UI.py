import streamlit as st
import requests



API_URL = "http://127.0.0.1:8000"



st.set_page_config(
    
    page_title = "Smart PDF Assistant",
    page_icon = "🔲",
    layout = "wide",

)

with st.sidebar:

    st.title("📄Smart PDF Assistant")

    uploaded_file = st.file_uploader(
        "Upload your PDF File",
        type = "pdf",
    )

    if uploaded_file is not None:

        if st.button("Upload"):

            files = {
                "file" : (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf",
                )
            }


            response = requests.post(f"{API_URL}/upload", files = files)

            if response.ok :
                st.success("PDF uploaded successfully!")



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]) :

        st.markdown(message["content"])

        if message["role"] == "assistant" :

            chunks = message.get("chunks", [])

            if message.get("tool")=="citation" and chunks:

                with st.expander("Chunks"):

                    for chunk in chunks :

                        st.markdown(
                            f"**Page:** {chunk['page']}"
                        )

                        st.write(chunk["text"])

                        st.divider()



question = st.chat_input(
    "Ask a question about your PDF ...",
)
    
if question :

    st.session_state.messages.append(
        {
            "role" : "user",
            "content" : question,
        }
    )

    with st.chat_message("user") :

        st.markdown(question)


    with st.spinner("Thinking..."):

        response = requests.post(f"{API_URL}/search", json = {"query" : question})

        data = response.json()



    answer = data["answer"]

    chunks = data["chunks"]

    tool = data["tool"]

    with st.chat_message("assistant") :

        st.markdown(answer)

        if tool == "citation" :

            with st.expander("Retrieved Chunks") :

                for chunk in chunks :

                    st.markdown(f"**Page:** {chunk['page']}")

                    st.write(chunk["text"])

                    st.divider()


    st.session_state.messages.append(
        {
            "role" : "assistant",
            "content" : answer,
            "chunks" : chunks,
            "tool" : tool
        }
    )
