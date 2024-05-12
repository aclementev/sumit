# Sumit


Sumit is a command-line tool for automatically generating notes from a video in markdown format. 
It uses AI models to extract the relevant information from the transcript of a video, and summarizes it in a format 
that is good for a markdown note taking app.


## Installation


To install Sumit, you can use pip:

```bash
pip install sumit
```


## Usage

Sumit can be used by running the following command in your terminal:
You will need an OpenAI API key, which you can pass through the `OPENAI_API_KEY` environment variable.

```bash
sumit <video_path>
```

Replace `<video_path>` with the path to the video file you want to generate notes from.
This will generate a markdown file named `<filename>.md` containing the summarized notes from the input file.


## Example

Here's an example of how to use Sumit:

```bash
sumit my_video.mp4
```

This will generate a markdown file named `my_video_notes.md` containing the summarized notes from the `my_video.mp4` file.
