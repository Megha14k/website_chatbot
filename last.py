import requests
from bs4 import BeautifulSoup
import subprocess
import sys

# configuration values
URL = "https://botpenguin.com/"
MODEL = "llama2"

# scrape website content
def scrape_website():
    print(f"Scraping website: {URL}")

    # headers to mimic a browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    # fetch website HTML
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("⚠ Website blocked scraping (Cloudflare protection).")
        print(f"Error: {e}")
        sys.exit(1)

    # parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # get website title
    title = soup.title.string.strip() if soup.title else "Unknown Website"

    # remove non-content tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # extract and clean visible text
    text = soup.get_text(separator=" ")
    text = " ".join(text.split())

    return title, text

# split text into chunks
def chunk_text(text, chunk_size=1200):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

# ask Ollama using website chunks
def ask_ollama(question, chunks, website_name, memory):
    for chunk in chunks:
        # prompt with strict answer rules
        prompt = f"""
You are a website chatbot.

STRICT RULES (no exceptions):
- Answer in ONE sentence only
- Maximum 25 words
- Use ONLY the website content
- Do NOT add examples, lists, or extra details
- Do NOT say "the website provides", "this platform offers", or similar phrases
- If the answer is not found, reply exactly: I don't know

Website content:
{chunk}

Question: {question}
Answer:
"""

        # run Ollama locally
        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        answer = result.stdout.strip()

        # return first valid answer
        if answer and answer.lower() != "i don't know":
            memory += f"User: {question}\nBot: {answer}\n"
            return answer, memory

    # fallback if no answer is found
    return "I don't know", memory

# main chatbot loop
def main():
    # load website data
    website_name, website_text = scrape_website()

    print("\nWebsite content fetched successfully!")
    print(f"Website Name: {website_name}\n")
    print("Chatbot is ready! Type 'exit' to quit.\n")

    # prepare chunks and memory
    chunks = list(chunk_text(website_text))
    memory = ""

    while True:
        user_input = input("You: ").strip()

        # exit command
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # deterministic website name response
        if "website name" in user_input.lower():
            print(f"Bot: {website_name}\n")
            continue

        # generate response
        answer, memory = ask_ollama(user_input, chunks, website_name, memory)
        print(f"Bot: {answer}\n")

# program entry point
if __name__ == "__main__":
    main()
