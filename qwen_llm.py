import os
import torch
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


# Load environment variables
load_dotenv()

# Authenticate with Hugging Face Hub
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token, add_to_git_credential=True)
else:
    raise ValueError("Hugging Face token not found. Please set HF_TOKEN in your .env file.")

# Load the model and tokenizer
model_id = "Qwen/Qwen2-1.5B-Instruct"

# Automatically choose GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",          # Auto-assign model layers to device (GPU or CPU)
    torch_dtype="auto",         # Use the model's native dtype (float16/bfloat16/etc.)
    trust_remote_code=True
)

# Create text-generation pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

def get_response_qwen(prompt: str) -> str:
    """Generate a response using Qwen2 based on a prompt string."""
    messages = [
        {"role": "system", "content": "You are a helpful agent reasoning about social deception in a deduction game."},
        {"role": "user", "content": prompt}
    ]
    
    # Format prompt using Qwen's chat template
    prompt_str = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Generate response
    output = pipe(
        prompt_str,
        max_new_tokens=128,
        temperature=0.7,
        do_sample=True,
        return_full_text=False
    )
    
    return output[0]["generated_text"]

# Load model and move to GPU with half precision
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     torch_dtype=torch.float16,
#     trust_remote_code=True
# ).to(device)

# def get_response2(prompt: str) -> str:
#     """Generate a fast response using Qwen2 based on a prompt string."""
#     messages = [
#         {"role": "system", "content": "You are a helpful agent reasoning about social deception in a deduction game."},
#         {"role": "user", "content": prompt}
#     ]

#     # Format prompt using chat template
#     prompt_str = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

#     # Tokenize and move input to device
#     inputs = tokenizer(prompt_str, return_tensors="pt").to(device)

#     # Generate response (greedy decoding = fast)
#     with torch.no_grad():
#         output_ids = model.generate(
#             inputs.input_ids,
#             max_new_tokens=128,
#             do_sample=True,
#             temperature=0.7,
#             attention_mask=inputs.attention_mask  
#         )

#     # Decode and strip prompt part
#     full_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#     generated_text = full_output.replace(prompt_str, "").strip()
#     return generated_text

# For test runs
if __name__ == "__main__":
    sample_prompt = "How are you doing today?"
    print(get_response_qwen(sample_prompt))
