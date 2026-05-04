"""
Automated Email Rewriter
Rewrite emails in multiple styles using OpenAI API
"""

from utils import send_prompt
import os
from datetime import datetime

# Style definitions with specific prompts
STYLES = {
    "Polite": {
        "description": "Make the email more polite and considerate",
        "instruction": "Please rewrite the following email to be more polite, courteous, and considerate. Use respectful language and soften any demands."
    },
    "Concise": {
        "description": "Make the email brief and to the point",
        "instruction": "Please rewrite the following email to be more concise and direct. Remove unnecessary words while preserving the core message."
    },
    "Formal": {
        "description": "Make the email professional and formal",
        "instruction": "Please rewrite the following email in a formal, professional tone suitable for business communication. Use proper structure and formal language."
    },
    "Friendly": {
        "description": "Make the email warm and approachable",
        "instruction": "Please rewrite the following email to be more friendly and warm. Use a conversational tone that builds rapport."
    },
    "Professional": {
        "description": "Make the email balanced and professional",
        "instruction": "Please rewrite the following email to strike a balance between professionalism and warmth. Use clear, respectful language suitable for business."
    }
}

def load_email(filepath: str) -> str:
    """Load email content from a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Email file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        return f.read().strip()

def rewrite_email(email_text: str, style: str, instruction: str) -> str:
    """
    Rewrite email in a specific style using OpenAI API.
    
    Args:
        email_text: Original email content
        style: Name of the style
        instruction: Specific instruction for the rewrite
    
    Returns:
        Rewritten email
    """
    prompt = f"{instruction}\n\nOriginal Email:\n{email_text}"
    
    print(f"  → Rewriting in {style} style...")
    
    rewritten = send_prompt(
        prompt,
        max_tokens=300,
        temperature=0.3
    )
    
    return rewritten

def save_rewritten_email(email_text: str, style: str, output_dir: str = "rewritten_emails") -> str:
    """
    Save rewritten email to a file.
    
    Args:
        email_text: Rewritten email content
        style: Style name
        output_dir: Directory to save files
    
    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create filename with timestamp and style
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rewritten_email_{style.lower()}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(email_text)
    
    return filepath

def print_separator(title: str = "") -> None:
    """Print a formatted separator."""
    separator = "=" * 70
    if title:
        print(f"\n{separator}")
        print(f"  {title}")
        print(f"{separator}\n")
    else:
        print(f"{separator}\n")

def main():
    """Main function to orchestrate email rewriting."""
    email_path = "email_sample.txt"
    
    print_separator("EMAIL REWRITER - Multi-Style Automation")
    
    try:
        # Load original email
        print(f"Loading email from: {email_path}")
        original_email = load_email(email_path)
        print(f"✓ Email loaded successfully\n")
        
        print_separator("ORIGINAL EMAIL")
        print(original_email)
        print()
        
        # Rewrite in each style
        results = {}
        print_separator("REWRITING EMAIL")
        print(f"Processing {len(STYLES)} styles...\n")
        
        for style, config in STYLES.items():
            try:
                print(f"Processing: {style}")
                print(f"  Description: {config['description']}")
                
                rewritten = rewrite_email(
                    original_email,
                    style,
                    config['instruction']
                )
                
                # Save to file
                filepath = save_rewritten_email(rewritten, style)
                results[style] = {
                    "content": rewritten,
                    "filepath": filepath
                }
                
                print(f"  ✓ Saved to: {filepath}\n")
                
            except Exception as e:
                print(f"  ✗ Error processing {style}: {str(e)}\n")
                continue
        
        # Print all rewritten versions
        print_separator("REWRITTEN EMAILS")
        
        for style, config in STYLES.items():
            if style in results:
                print(f"\n{style.upper()} VERSION:")
                print("-" * 70)
                print(results[style]["content"])
                print()
        
        # Summary
        print_separator("PROCESSING COMPLETE")
        print(f"✓ Successfully rewritten: {len(results)}/{len(STYLES)} styles")
        print(f"✓ Files saved to: rewritten_emails/\n")
        
        return results
    
    except FileNotFoundError as e:
        print(f"✗ Error: {str(e)}")
        print(f"  Make sure '{email_path}' exists in the current directory.")
        return None
    
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
