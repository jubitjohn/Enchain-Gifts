#!/usr/bin/env python3
"""
Test script for the Mediator API endpoint
This script demonstrates how to use the new mediator API that acts as an intent identifier
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8082"  # Change this to your actual server URL
MEDIATOR_ENDPOINT = f"{BASE_URL}/mediator"

def test_mediator_api(user_input):
    """
    Test the mediator API with different user inputs
    """
    print(f"\n{'='*60}")
    print(f"Testing with input: '{user_input}'")
    print(f"{'='*60}")
    
    try:
        # Prepare the request payload
        payload = {
            "user_input": user_input
        }
        
        # Make the POST request to the mediator endpoint
        response = requests.post(
            MEDIATOR_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Parse and print the response
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS Response:")
            print(json.dumps(result, indent=2))
            
            # Extract key information
            if result.get("success"):
                print(f"\n📋 Summary:")
                print(f"  Intent: {result.get('intent_analysis', {}).get('intent', 'unknown')}")
                print(f"  Parameters: {result.get('intent_analysis', {}).get('parameters', {})}")
                if 'url' in result:
                    print(f"  Generated URL: {result['url']}")
                if 'message' in result:
                    print(f"  Message: {result['message']}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"\n❌ ERROR Response:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request Error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Decode Error: {str(e)}")
        print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")

def main():
    """
    Main function to run various test cases
    """
    print("🧪 Mediator API Test Suite")
    print("This script tests the intent identification and routing functionality")
    
    # Test cases for different intents
    test_cases = [
        # Pendant generation tests
        "I want to create a pendant with the name Sarah",
        "Generate a pendant for my friend John",
        "Make me a pendant with name Emma",
        
        # Gift creation tests
        "I need to create a birthday gift for my mom",
        "Create a wedding gift for my sister",
        "I want to make a Christmas gift for my dad",
        
        # Design customization tests
        "Customize the design with a modern style and silver color",
        "I want a vintage style pendant in gold",
        "Change the design to minimalist style with black color",
        
        # Catalog tests
        "Show me the pendant catalog",
        "Get me the gift catalog for women",
        "I want to see all available designs",
        
        # Support tests
        "I have an issue with my order",
        "Contact support about delivery problems",
        "I need help with customization",
        
        # Unknown intent tests
        "What's the weather like today?",
        "Tell me a joke",
        "Random text that doesn't match any intent"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}/{len(test_cases)}")
        test_mediator_api(test_input)
        
        # Add a small delay between requests
        import time
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print("✅ Test suite completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 