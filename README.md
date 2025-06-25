# PolicyBot
A LLM powered chatbot app which answers question pertaining to the uploaded policy documents as context.

---

# App setup steps
---
1. This app to run on local machine, ollama is to be installed using link: [[Ollama](https://ollama.com/)]
2. Once ollama is installed pull and run the mistral:lates using command `ollama run mistral` in terminal.
3. Create virtual environement `python -m venv venv`
4. Installed the requirement using `pip install -r requirements.txt`.
5. Run the application 'streamlit run app.py'
6. Checkout the screenshot images attached namely: policy_bot_1.png, policy_bot_2.png to understand how with manual input the intent is setup first due to the nature of our data and similarity overlap.

# EDA Details
---

## Exploratory Data Analysis of given text data for Retrieval-Augmented Generation (RAG) on Policy Documents
---
#### In this notebook following analysis are carried out to understand the content of given policies documents:
- Basic statistics and numbers extrcation: To get the length of the document's content.
- Word cloud analysis: To know the dominant keywords of each document and how each document is similar or different from the other ones.
- Named Entity Extraction using Spacy: To deep dive into data and topic grouping analysis, this provided the insight on whether apart from title of each policy documents is there further segregation is possible between the policy document and thereby ensuring better query response by the RAG assistant application.
- TF-IDF based topic modelling: To find if a unsupervised analysis of the given text corpus when done how many topics does the machine algorithms in text analysis space able to find.
- Sematics Analysis: To find the similarity between the policy documents and sections of policy documents.

#### Finding of the above analysis:

##### - Word Cloud Analysis:
- Dominant words found are data, AI, model, policy, ethics, governance. These are few with high weights.
- It is found that there is high degree of overlap between on the bsis of high weight keywords and after segregating each policy document on the basis of the title of each document further segreagation or effort to find the disimilarity between each document is less likely, this can be concluded based on the keyword analysis as part of this section.

##### - Named Entity Extraction:
- This analysis is done by extracting the standard entity from the text corpus using Spacy library.
- Although the tagging of the extracted entity by the spacy model is incorrect but one key thing is it is consistent.
- I each policy document just like work cloud analysis simialr keyword and phrases are found to be tagged with same entity type. This further confirms the above finding that each of these document are more similar than dissimilar.
- In future scope if the more policy documents are added in RAG assistant appication then the overlap can increase further.

##### - TF-IDF Topic modelling:
- This analysis yield result by applying unsupervised learning analysis.
- In this topic recognition is tried on the text corpus of available policy data to find how much segregation a machine learning algorithm can find.
- Although there are 3 policy document when processed under this analysis yield only 2 topic, this further confirms the high overlap and similarity in the content of the policy documents.

##### - Sematics similarity Analysis:
- In this analysis the similarity between the policy document and the section of the policy documents is generated.
- Its is found that the similarity between different chuncks of policy document have a good similarity score with text chucks from another policy docuemnt:
     
    - ('Policy_2.txt', 1) <-> ('Policy_3.txt', 6) (Score: 0.8027)
    - ('Policy_2.txt', 1) <-> ('Policy_3.txt', 2) (Score: 0.7421)
    - ('Policy_2.txt', 7) <-> ('Policy_3.txt', 6) (Score: 0.7375)
    - ('Policy_2.txt', 2) <-> ('Policy_3.txt', 3) (Score: 0.7327)
    - ('Policy_1.txt', 7) <-> ('Policy_3.txt', 21) (Score: 0.6198)

- This further confirms at sentence level there is high overlap within the text data available for this RAG application.

#### Conclusion & Design desicions:
1. Considering future scope to serve multiple policy document as knwledge base/context for this RAG application assistent the chances of inter policy document content similarity will be high.
2. Such high similarity can reduce the result accuracy of the response gven by the RAG application for a given query.
3. Considering this in this RAG applicatio design it is better to have a intent classifier (text classification) of the incoming question/query by the end user.
4. Alternate to intent classifier can be setting up the context in real-time by asking end user upfront that what are they looking for.
5. ##### Application considerations:
   - The details can be found in the README file of the application.
   - In summary, rather that loading the policy document in the bucket storage, documents are loaded as the markdown file and hosted as github pages.
   - This make the input to the RAG model (mistral, llama etc) consistent. As it is found that in shared policy documents the markdow format is not consistent for heading and subheading. In large corpus it will be heavy processing to clean up the markdown special characters. Also this way ensure even if the plicy document is not markdown adn simple text file then that also can be hosted as github pages and loaded into RAG application by passing it as URL.
   - Few screenshots are attached to explain the POC application functioning. (policy_bot_1.png, policy_bot_2.png)

