import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# Configuration
endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.environ["GITHUB_TOKEN"]

# Initialize client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def display_header():
    """Display chat header"""
    print("\n" + "=" * 50)
    print("       🤖 AI Chat Assistant (DeepSeek V3)")
    print("=" * 50)
    print("Type your message and press Enter to chat.")
    print("Commands: 'quit' or 'exit' to end, 'clear' to reset")
    print("=" * 50 + "\n")

def chat():
    """Main interactive chat function"""
    display_header()
    
    # Initialize conversation with system message
    messages = [
        SystemMessage("You are a helpful, friendly AI assistant. Provide clear and concise responses.")
    ]
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Handle empty input
            if not user_input:
                print("   (Please type something...)")
                continue
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🤖 Assistant: Goodbye! Have a great day! 👋\n")
                break
            
            # Handle clear command
            if user_input.lower() == 'clear':
                messages = [
                    SystemMessage("You are a helpful, friendly AI assistant. Provide clear and concise responses.")
                ]
                print("\n   ✅ Chat history cleared!\n")
                display_header()
                continue
            
            # Add user message to history
            messages.append(UserMessage(user_input))
            
            # Get AI response
            print("\n🤖 Assistant: ", end="", flush=True)
            
            response = client.complete(
                messages=messages,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1000,
                model=model
            )
            
            # Extract and display response
            assistant_response = response.choices[0].message.content
            print(assistant_response)
            
            # Add assistant response to history for context
            messages.append(AssistantMessage(assistant_response))
            
        except KeyboardInterrupt:
            print("\n\n🤖 Assistant: Chat interrupted. Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n   ❌ Error: {e}")
            print("   (Please try again...)")

if __name__ == "__main__":
    chat()