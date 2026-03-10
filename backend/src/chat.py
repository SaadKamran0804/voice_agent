# def get_transcript(event, room_id, logger):
#     """
#     Parses conversation events and logs them to the console and structured logger.
#     """
#     # A user message (either spoken into the mic OR typed in the chat)
#     if event.item.role == "user":
#         print(f"\n[USER INPUT] Room: {room_id} | User: '{event.item.text_content}'")
#         print(f"\nUser: \n\n'{event}'\n\n")
#         logger.info(
#             "User input captured",
#             extra={"room_id": room_id, "text": event.item.text_content},
#         )

#     # The agent's generated response
#     elif event.item.role == "assistant":
#         print(f"[AGENT REPLY] Room: {room_id} | Agent: '{event.item.text_content}'\n")
#         print(f"\nAgent: \n\n'{event}'\n\n")
#         logger.debug(f"Agent replied in room {room_id}")

#     # Note: Later, you can easily add Neon DB saving logic right here!


# ============================================


import os
import textwrap

from google import genai
from google.genai import types


# def get_transcript_item(event, room_id, logger):
#     """
#     Extracts a single event into your exact dictionary schema.
#     Returns the dictionary so you can append it to your list in agent.py.
#     """
#     if event.item.role not in ["user", "assistant"]:
#         return None

#     # Safely extract text
#     content = event.item.content if hasattr(event.item, "content") else str(event.item)
#     if isinstance(content, list):
#         text = " ".join([c.text for c in content if hasattr(c, "text")])
#     else:
#         text = str(content)

#     # Build the exact schema
#     message_data = {
#         "id": getattr(event.item, "id", "no_id_found"),
#         "role": event.item.role,
#         "content": text,
#     }
    
#     # Keep structured logging for backend tracking
#     if event.item.role == "user":
#         logger.info("User input captured", extra={"room_id": room_id, "text": text})
#     elif event.item.role == "assistant":
#         logger.debug(f"Agent replied in room {room_id}")
#     print(f"message_data: {message_data}")
#     return message_data


def get_transcript_item(event, room_id, logger):
    """
    Extracts a single event into your exact dictionary schema.
    Returns the dictionary so you can append it to your list in agent.py.
    """
    if event.item.role not in ["user", "assistant"]:
        return None

    # Safely extract text directly using text_content
    text = event.item.text_content if hasattr(event.item, "text_content") else str(event.item)

    # Build the exact schema
    message_data = {
        "id": getattr(event.item, "id", "no_id_found"),
        "role": event.item.role,
        "content": text,
    }
    
    # Keep structured logging for backend tracking
    if event.item.role == "user":
        logger.info("User input captured", extra={"room_id": room_id, "text": text})
    elif event.item.role == "assistant":
        logger.debug(f"Agent replied in room {room_id}")
        
    print(f"message_data: {message_data}")
    return message_data

async def summarize_conversation(conversation_list):
    """
    Takes the full list of transcript dictionaries and generates a strict summary using Gemini.
    """
    if not conversation_list:
        return "No conversation to summarize."

    # Format the structured list into a readable text script (This acts as the prompt)
    script = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_list]
    )

    # Your exact provided system instruction
    system_instruction = textwrap.dedent(
        """\
        ROLE: You are an elite, highly deterministic conversational summarization engine. Your sole function is to extract the core signal from user-agent transcripts with absolute precision and zero noise.
        
        OBJECTIVE: Analyze the provided conversation and generate a dense, objective summary.
        
        STRICT CONSTRAINTS:
        - Length Control [CRITICAL MAXIMUM]: Your output MUST be strictly calibrated to exactly 100 words. (Acceptable variance is strictly limited to 90 - 110 words). Count your words internally before outputting.
        - Direct Output: Do NOT output conversational filler, pleasantries, or meta-commentary (e.g., avoid "Here is the summary," "In this conversation"). Start the very first word with the summary itself.
        - Perspective: Use a neutral, objective, third-person perspective (e.g., "The user requested...", "The agent provided...").
        - Information Hierarchy: Your summary must synthesize:
            * The user's primary intent, context, or problem.
            * The agent's key actions, answers, or troubleshooting steps.
            * The final resolution, outcome, or pending next steps.
        - Fidelity: Never hallucinate, infer, or add information not explicitly present in the source transcript.
        
        FORMAT: Output a single, densely informative paragraph."""
    )

    # Initialize the Gemini client using the environment variable
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    try:
        # We use client.aio for asynchronous generation and pass the system instructions via config
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=script,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )
        return response.text
    except Exception as e:
        return f"Failed to generate summary: {str(e)}"
