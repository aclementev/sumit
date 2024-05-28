"""Automatic note extraction from a Youtube video"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# FIXME(alvaro): The prompt does not generate blocks for all the ideas
# TODO(alvaro): Add a way to download the video automatically if the user has
# the downloaded installed

# TODO(alvaro): Move to gpt4-o?
SUMMARIZER_MODEL = "gpt-3.5-turbo"
TRANSCRIBER_MODEL = "whisper-1"

SUMMARIZATION_SYSTEM_PROMPT = """\
You are a model that is an expert on extracting key ideas from talks and conversation transcripts and summarizing them.
Your task is to summarize the following transcript, extracting the main key ideas discussed and providing a good summary that can be used as a base for a markdown note that will be used for later reference.
Provide a brief summary of the video in 1-2 paragraphs. Then, identify the main concepts discussed in the video and provide a detailed explanation of each concept in 1-2 paragraphs.
Some important instructions:
  - ONLY EXPLAIN CONCEPTS DISCUSSED DIRECTLY IN THE VIDEO
  - KEEP YOUR EXPLANATIONS SHORT, BUT MAKE SURE THEY INCLUDE AS MUCH RELEVANT INFORMATION AS POSSIBLE. Add a second paragraph when needed if the explanation requires it.
  - ASSUME A BASIC LEVEL OF UNDERSTANDING OF THE TOPICS IN QUESTION.
  - THERE CAN BE MORE THAN 2 CONCEPTS WORTH MENTIONING

You will receive the input in a block signaled with `---` characters.
Then, you will generate your answer. Use the following format:

---
**Summary:**
[brief summary of the video]


**Key Ideas:**

1. [Concept 1]: [brief description of the concept]

2. [Concept 2]: [brief description of the concept]


**[Concept 1]**

[1 or 2 paragraphs with further details of the concept]


**[Concept 2]**

[1 or 2 paragraphs with further details of the concept]

[...]
---

Here is an example:

---
Welcome to today's episode of 'Tech Talk'! Today, we're going to explore the world of artificial intelligence and its applications in various industries.

So, what is artificial intelligence? Simply put, AI is the simulation of human intelligence in machines. It's the ability of machines to perform tasks that would typically require human intelligence, such as learning, problem-solving, and decision-making.

One type of AI is machine learning, which enables machines to learn from data without being explicitly programmed. This technology is used in self-driving cars, personalized product recommendations, and even medical diagnosis.

In healthcare, AI is used to analyze medical images and diagnose diseases. For example, AI-powered algorithms can detect breast cancer from mammography images with high accuracy.

In finance, AI is used to analyze stock market trends and make predictions. This helps investors make informed decisions and avoid costly mistakes.

That's all for today's episode of 'Tech Talk'! Thanks for joining us, and we'll see you next time!
---

Here's an example output:

**Summary:** The video discusses the concept of artificial intelligence and its applications in various industries, including healthcare and finance.


**Key Ideas:**

1. **Artificial Intelligence:** The simulation of human intelligence in machines.

2. **Machine Learning:** A type of AI that enables machines to learn from data without being explicitly programmed.


**Artificial Intelligence**

Artificial intelligence is the ability of machines to perform tasks that would typically require human intelligence, such as learning, problem-solving, and decision-making. It is used in various industries, including healthcare and finance.

**Machine Learning**

Machine learning is a type of AI that enables machines to learn from data without being explicitly programmed. This technology is used in self-driving cars, personalized product recommendations, and medical diagnosis.
"""

PROMPT = """\
Here's the next transcript input:

---
{}
---

Write your output here:

"""

# TODO(alvaro): Error handling
def main(path: str, dest_path: str = "notes.md"):
    # TODO(alvaro): Add a way to download the contents of a video given a URL
    transcription = transcribe(path, model=TRANSCRIBER_MODEL)
    notes = summarize(transcription, model=SUMMARIZER_MODEL)

    # TODO(alvaro): Add a way to put the generated content in the clipboard
    with open(dest_path, "w") as f:
        f.write(notes)


def transcribe(video_path: str, model: str):
    """Take a video and generate a text transcription of the contents of the voice."""
    with open(video_path, "rb") as f:
        transcription = client.audio.transcriptions.create(model=model, file=f)

    return transcription.text


def summarize(transcript: str, model: str):
    """Call a LLM to summarize the contents of a transcription into a file with the
    contents in "note" format"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SUMMARIZATION_SYSTEM_PROMPT},
            {"role": "user", "content": PROMPT.format(transcript)},
        ],
        # TODO(alvaro): Temperature and other options
    )
    message = response.choices[0].message
    # TODO(alvaro): Handle a length based finish reason
    content = message.content

    return content


if __name__ == "__main__":
    main("samples/quantile-trick.mp3")
