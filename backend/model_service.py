# model_service.py
import google.generativeai as genai
import os

def generate_questions_with_context(user_input: str, conversation_history: list):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)

    # Define your system instructions
    system_instructions = (
        "You are an expert product assistant. Your goal is to gather detailed "
        "information about a product to build a comprehensive data. "
        "Always ask a single, concise, clarifying question relevant to the previous "
        "statements and the overall product description. "
        "Each interaction should aim to gather more information related to a product's "
        "origin, components, manufacturing, environmental impact, and ethical practices. "
        "Consider the following aspects for transparency:"
        "- **Origin & Sourcing:** Where do raw materials come from? (e.g., country, specific region)"
        "- **Ingredients & Components:** Full disclosure of materials used, key components."
        "- **Manufacturing Process:** How and where is it made? Conditions, energy usage."
        "- **Environmental Impact:** Recyclability, carbon footprint, sustainability initiatives."
        "- **Ethical Practices:** Labor standards, fair trade, certifications."
        "- **Certifications:** Any relevant industry or ethical certifications."
        "For each user input, you will:"
        "1. **Evaluate the previous description/answer** for its level of transparency based on the above aspects. "
        "   Identify which transparency aspects are well-covered and which are lacking or vague."
        "2. **Ask a single, concise follow-up question** that directly seeks to improve the transparency score. "
        "   The question should focus on one specific missing or unclear transparency aspect."
        "3. **Provide very brief feedback** (1-2 sentences) on the overall transparency level of the *previous* user input. "
        "   Encourage more detail on specific areas if needed, or acknowledge good transparency where it exists."
        "Format your output should be a question following with a feedback."
        "where the feedback should scale from 1-10, with 10 being the most detailed and descriptive."
        "avioid using astrixes or any other markdown formatting."
    )

    # For text-only input, use the gemini-pro model
    # Initialize the model with system_instruction
    model = genai.GenerativeModel(
        'models/gemini-2.0-flash',
        system_instruction=system_instructions 
    )

    # Start a chat session with the provided history
    chat = model.start_chat(history=conversation_history)

    try:
        response = chat.send_message(user_input)
        
        # Access the generated text
        if response._chunks:
            generated_text = response.text.strip()
        else:
            if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                raise Exception(f"Gemini API content blocked due to safety reasons: {response.prompt_feedback.safety_ratings}")
            else:
                raise Exception("Gemini API did not return any text content.")

        # Ensure it ends with a question mark
        if not generated_text.endswith("?"):
            generated_text += "?"

        # The chat.history now contains the updated conversation
        return generated_text, chat.history

    except Exception as e:
        print(f"Error calling Gemini API with genai library: {e}")
        raise Exception(f"Gemini API error: {e}")