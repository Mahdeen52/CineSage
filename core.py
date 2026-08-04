from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate

model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)


prompt_template = ChatPromptTemplate.from_messages([("system", """You are an information extraction assistant.

Your task is to read the movie description below and extract all important information. If a field is not mentioned, return "Not Mentioned".

Movie Description:


Extract the following information:

1. Movie Name
2. Genre(s)
3. Director
4. Release Year
5. Main Cast (as a list)
6. Plot / Story
7. Setting (if mentioned)
8. Main Theme(s)
9. IMDb Rating (if mentioned)
10. Other Ratings (Rotten Tomatoes, Metacritic, etc., if mentioned)
11. Awards or Recognition (if mentioned)
12. Music Composer
13. Production Company (if mentioned)
14. Country of Origin (if mentioned)
15. Language (if mentioned)
16. Runtime (if mentioned)
17. Box Office Collection (if mentioned)
18. Critical Reception (positive/negative/mixed)
19. Notable Features (e.g., visual effects, soundtrack, scientific accuracy, acting)
20. Keywords (5–10 important keywords)
21. No of wives of the main character in his personal life, not in movie

Finally, generate a concise summary of the movie description in 2–3 sentences. The summary should capture the main story, important people involved, and why the movie is notable.

Return the information in a clear, well-organized format."""), ("human", "tell me about the {movie_description} paragraph")])


movie_description = input("Enter the movie description: ")
final_prompt = prompt_template.invoke({"movie_description": movie_description})
response = model.invoke(final_prompt)
print(response.content)