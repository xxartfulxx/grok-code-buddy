import os
from dotenv import load_dotenv

load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
REQUEST_COUNT = 0
REQUEST_LIMIT = 100

def fetch_grok_response(prompt, session, gui):
    global REQUEST_COUNT
    print(f"Entering fetch_grok_response with prompt: {prompt}")
    if REQUEST_COUNT >= REQUEST_LIMIT:
        print("Hit request limit")
        return "Whoa, we’ve hit the limit! Time to chill—back tomorrow, yeah?"
    REQUEST_COUNT += 1
    gui.increment_request_count()
    print(f"Global request count incremented to: {REQUEST_COUNT}")

    session.append({'role': 'user', 'content': prompt})
    print(f"Session updated: {session}")

    if "code" in prompt.lower() and "test" in prompt.lower():
        answer = "Here’s some text.\n```python\ndef test():\n    print('Hello')\n```\nMore text."
    elif "essay" in prompt.lower() and "xai" in prompt.lower():
        answer = (
            "xAI, founded by Elon Musk in 2016, is a company dedicated to accelerating human scientific discovery through artificial intelligence. Based in San Francisco, "
            "xAI’s mission is to tackle some of the universe’s most profound mysteries—like dark matter, the origins of life, or the nature of consciousness—by leveraging AI "
            "to amplify human intellect. Musk, a serial entrepreneur known for SpaceX and Tesla, envisioned xAI as a tool to fast-track humanity’s understanding of reality, a "
            "theme that echoes across his ventures. Unlike SpaceX’s rockets or Tesla’s electric cars, xAI’s output is less tangible: it’s about crafting AI models that could "
            "one day rival or surpass human reasoning, offering insights no single mind could uncover alone.\n\n"
            "The company’s early projects include Grok, an AI designed to provide helpful and truthful answers, often with a dash of humor and an outside perspective on "
            "humanity. Built from scratch by xAI’s team—stocked with talent from DeepMind, Google, and OpenAI—this AI reflects the company’s ambition to create tools that "
            "don’t just respond but provoke thought. xAI’s culture mirrors Musk’s ‘fail fast, learn faster’ philosophy, emphasizing rapid iteration and bold experimentation. "
            "While much of its work remains under wraps, rumors swirl about projects tackling everything from quantum physics to biological simulations, all driven by AI.\n\n"
            "What sets xAI apart is its focus on curiosity-driven research over immediate commercial gain. Where other AI firms chase chatbots or ad algorithms, xAI aims to "
            "answer questions we haven’t fully asked yet. Imagine an AI that not only solves equations but suggests new ones for scientists to explore—that’s the dream. With "
            "Musk at the helm, xAI inherits his knack for dreaming big, tempered by a track record of turning wild ideas into reality. Its potential impact is staggering: "
            "unlocking secrets of the cosmos, speeding up discoveries in medicine, or even redefining how we see ourselves. At 500 words, this essay only scratches the surface, "
            "but xAI stands as Musk’s bold bet on AI as humanity’s next frontier, blending ambition with a relentless quest for cosmic truth."
        )
    else:
        answer = f"Got your prompt: '{prompt}'. How can I assist you further?"
    session.append({'role': 'assistant', 'content': answer})
    print(f"Returning mock response: {answer[:50]}...")
    return answer