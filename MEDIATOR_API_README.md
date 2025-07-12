# Mediator API Documentation

## Overview

The Mediator API is an intelligent endpoint that acts as an intent identifier and router for the Enchain Gifts application. It uses DeepSeek AI to analyze user input and automatically routes requests to the appropriate internal endpoints based on identified intents.

## Features

- 🤖 **AI-Powered Intent Recognition**: Uses DeepSeek to analyze natural language input
- 🔄 **Automatic Routing**: Routes requests to appropriate internal endpoints
- 📝 **Structured Responses**: Returns consistent JSON responses with metadata
- 🛡️ **Error Handling**: Comprehensive error handling and fallback mechanisms
- 🔧 **Extensible**: Easy to add new intents and endpoints

## API Endpoint

### POST `/mediator`

**URL**: `http://your-domain.com/mediator`

**Method**: `POST`

**Content-Type**: `application/json`

## Request Format

```json
{
  "user_input": "I want to create a pendant with the name Sarah"
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "intent": "generate_pendant",
  "url": "/images/pendant_abc123.png",
  "file_path": "/path/to/pendant_abc123.png",
  "parameters": {
    "name": "Sarah"
  },
  "user_input": "I want to create a pendant with the name Sarah",
  "intent_analysis": {
    "intent": "generate_pendant",
    "parameters": {
      "name": "Sarah"
    }
  },
  "timestamp": "abc123-def456-ghi789"
}
```

### Error Response
```json
{
  "success": false,
  "error": "DeepSeek API key not configured",
  "user_input": "I want to create a pendant with the name Sarah"
}
```

## Supported Intents

The mediator API currently supports the following intents:

### 1. `generate_pendant`
Creates a personalized pendant with a given name.

**Parameters:**
- `name` (string): The name to be engraved on the pendant

**Example Input:**
- "I want to create a pendant with the name Sarah"
- "Generate a pendant for my friend John"
- "Make me a pendant with name Emma"

### 2. `create_gift`
Initiates gift creation process.

**Parameters:**
- `type` (string): Type of gift (e.g., "birthday", "wedding", "Christmas")
- `recipient` (string): Recipient of the gift

**Example Input:**
- "I need to create a birthday gift for my mom"
- "Create a wedding gift for my sister"
- "I want to make a Christmas gift for my dad"

### 3. `customize_design`
Customizes design parameters.

**Parameters:**
- `style` (string): Design style (e.g., "modern", "vintage", "minimalist")
- `color` (string): Color preference (e.g., "gold", "silver", "black")

**Example Input:**
- "Customize the design with a modern style and silver color"
- "I want a vintage style pendant in gold"
- "Change the design to minimalist style with black color"

### 4. `get_catalog`
Retrieves product catalog.

**Parameters:**
- `category` (string): Category filter (e.g., "pendants", "gifts", "women")

**Example Input:**
- "Show me the pendant catalog"
- "Get me the gift catalog for women"
- "I want to see all available designs"

### 5. `contact_support`
Creates support tickets.

**Parameters:**
- `issue` (string): Description of the issue

**Example Input:**
- "I have an issue with my order"
- "Contact support about delivery problems"
- "I need help with customization"

## Configuration

### Environment Variables

Set the following environment variables:

```bash
# Required: DeepSeek API key
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional: Images directory (defaults to ./images)
IMAGES_DIR=/path/to/images/directory

# Optional: Port (defaults to 8082)
PORT=8082
```

### Getting DeepSeek API Key

1. Visit [DeepSeek AI](https://platform.deepseek.com/)
2. Create an account or sign in
3. Navigate to API section
4. Generate a new API key
5. Add the key to your environment variables

## Installation and Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   ```bash
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Test the API:**
   ```bash
   python test_mediator.py
   ```

## Usage Examples

### Using curl

```bash
# Test pendant generation
curl -X POST http://localhost:8082/mediator \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I want to create a pendant with the name Sarah"}'

# Test gift creation
curl -X POST http://localhost:8082/mediator \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Create a birthday gift for my mom"}'

# Test design customization
curl -X POST http://localhost:8082/mediator \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Customize the design with modern style and silver color"}'
```

### Using Python

```python
import requests
import json

def call_mediator_api(user_input):
    url = "http://localhost:8082/mediator"
    payload = {"user_input": user_input}
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
result = call_mediator_api("I want to create a pendant with the name Sarah")
print(json.dumps(result, indent=2))
```

### Using JavaScript/Node.js

```javascript
async function callMediatorAPI(userInput) {
    const response = await fetch('http://localhost:8082/mediator', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_input: userInput
        })
    });
    
    return await response.json();
}

// Example usage
callMediatorAPI("I want to create a pendant with the name Sarah")
    .then(result => console.log(JSON.stringify(result, null, 2)))
    .catch(error => console.error('Error:', error));
```

## Error Handling

The API includes comprehensive error handling:

1. **Missing API Key**: Returns error if DeepSeek API key is not configured
2. **Invalid Input**: Returns error for malformed requests
3. **DeepSeek Errors**: Handles API timeouts and connection issues
4. **Unknown Intents**: Returns available intents when intent cannot be determined
5. **Internal Errors**: Graceful handling of internal endpoint errors

## Extending the API

### Adding New Intents

1. **Update the DeepSeek prompt** in `analyze_intent_with_deepseek()` function
2. **Add routing logic** in `route_to_internal_endpoint()` function
3. **Implement internal function** for the new intent
4. **Update documentation** with new intent details

### Example: Adding a "track_order" intent

```python
# 1. Add to DeepSeek prompt
"6. track_order: {\"intent\": \"track_order\", \"parameters\": {\"order_id\": \"string\"}}"

# 2. Add routing logic
elif intent == "track_order":
    order_id = parameters.get('order_id', '')
    return track_order_internal(order_id)

# 3. Implement internal function
def track_order_internal(order_id):
    return {
        "success": True,
        "intent": "track_order",
        "message": f"Order {order_id} status retrieved",
        "parameters": {"order_id": order_id}
    }
```

## Testing

Run the comprehensive test suite:

```bash
python test_mediator.py
```

This will test various user inputs and verify that:
- Intent recognition works correctly
- Parameters are extracted properly
- Responses are formatted correctly
- Error handling works as expected

## Performance Considerations

- **Caching**: Consider implementing response caching for repeated requests
- **Rate Limiting**: Implement rate limiting for DeepSeek API calls
- **Timeout Handling**: Set appropriate timeouts for external API calls
- **Error Recovery**: Implement retry logic for transient failures

## Security Considerations

- **API Key Protection**: Never expose API keys in client-side code
- **Input Validation**: Validate and sanitize all user inputs
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **HTTPS**: Use HTTPS in production environments

## Troubleshooting

### Common Issues

1. **"DeepSeek API key not configured"**
   - Solution: Set the `DEEPSEEK_API_KEY` environment variable

2. **"Failed to parse DeepSeek response"**
   - Solution: Check DeepSeek API status and response format

3. **"Unknown intent"**
   - Solution: Check if the user input matches any defined intents

4. **Timeout errors**
   - Solution: Increase timeout values or check network connectivity

### Debug Mode

Enable debug mode for detailed logging:

```python
app.run(debug=True, host='0.0.0.0', port=port)
```

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test cases in `test_mediator.py`
3. Verify your DeepSeek API key is valid
4. Check the application logs for detailed error messages 