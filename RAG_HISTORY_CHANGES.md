# RAG-Based Chat History Implementation (RAM-Based)

## Overview

The chat history method has been changed from a sliding window approach to a RAG-based approach using **RAM storage** instead of database collections. This provides faster access and simpler management while maintaining semantic search capabilities.

## Changes Made

### 1. Removed Sliding Window Approach
- **Before**: Fixed `MAX_HISTORY = 10` limit for question-answer pairs
- **After**: Dynamic retrieval based on semantic similarity

### 2. Added RAM-Based History Storage
- **New Class**: `RAMChatHistory` - In-memory storage with semantic search
- **New Function**: `store_conversation_turn(question, answer, session_id)`
  - Stores each conversation turn in RAM
  - Creates embeddings for question-answer pairs
  - Includes metadata (session_id, timestamp, question, answer)

### 3. Added Intelligent History Retrieval
- **New Function**: `retrieve_relevant_history(current_question, session_id, top_k)`
  - Finds semantically similar previous conversations using cosine similarity
  - Prioritizes conversations from the same session
  - Returns top-k most relevant conversations

### 4. Enhanced Prompt Generation
- **New Function**: `format_chat_history_for_prompt(relevant_conversations, metadatas)`
  - Formats retrieved conversations for inclusion in prompts
  - Provides context about previous relevant discussions

## Key Benefits

### 1. **Speed & Performance**
- **RAM Storage**: Much faster than database queries
- **In-Memory Search**: Direct vector similarity calculations
- **No I/O Overhead**: No disk reads/writes for chat history

### 2. **Semantic Relevance**
- Instead of just keeping the last N messages, the system finds conversations that are semantically similar to the current question
- More intelligent context provision

### 3. **Session Awareness**
- Conversations from the same session are prioritized
- Maintains conversation continuity within a session

### 4. **Simplicity**
- No database setup required for chat history
- Self-contained implementation
- Easy to debug and monitor

## Technical Implementation

### RAM Storage Structure
```python
class RAMChatHistory:
    def __init__(self):
        self.conversations: List[Dict] = []           # All conversation data
        self.embeddings: List[List[float]] = []       # Vector embeddings
        self.session_embeddings: Dict[str, List[int]] # Session mapping
```

### Data Structure
```python
conversation_data = {
    "text": "Soru: ...\nCevap: ...",
    "metadata": {
        "session_id": str,
        "timestamp": str,
        "question": str,
        "answer": str,
        "type": "conversation"
    },
    "embedding": List[float]
}
```

### Retrieval Process
1. **Embed Current Question**: Create embedding for the new question
2. **Calculate Similarities**: Compute cosine similarity with all stored conversations
3. **Session Prioritization**: If session_id provided, prioritize same-session conversations
4. **Sort & Select**: Return top-k most similar conversations

## Usage Example

```python
# Store a conversation turn
session_id = store_conversation_turn(
    question="Vadeli mevduat nedir?",
    answer="Vadeli mevduat, belirli bir süre için bankaya yatırılan paradır.",
    session_id="user_session_123"
)

# Retrieve relevant history
relevant_conversations, metadatas = retrieve_relevant_history(
    current_question="Faiz oranları nasıl?",
    session_id="user_session_123",
    top_k=5
)
```

## Performance Characteristics

### Storage Performance
- **Memory Usage**: ~1-2KB per conversation turn (including embedding)
- **Insertion Speed**: O(1) - Direct list append
- **Scalability**: Can handle thousands of conversations efficiently

### Search Performance
- **Search Speed**: O(n) where n = number of conversations
- **Cosine Similarity**: Fast numpy-based calculations
- **Session Filtering**: O(1) hash table lookups

### Memory Management
- **Automatic Cleanup**: No automatic cleanup (manual session clearing available)
- **Memory Growth**: Linear with conversation count
- **Session Isolation**: Each session's data is tracked separately

## Testing

Run the test script to see the RAM-based RAG history in action:

```bash
python scripts/test_rag_history.py
```

This will test:
- Basic conversation storage and retrieval
- Session management
- Performance with larger datasets
- Semantic search accuracy

## Migration Notes

- **No Database Dependencies**: Chat history no longer requires ChromaDB
- **Faster Startup**: No database initialization for chat history
- **Memory Considerations**: Monitor memory usage for long-running sessions
- **Session Management**: Use `chat_history.clear_session(session_id)` to clean up

## Advanced Features

### Session Management
```python
# Get all conversations for a session
session_conversations = chat_history.get_session_conversations(session_id)

# Clear a specific session
chat_history.clear_session(session_id)
```

### Performance Monitoring
```python
# Check current memory usage
total_conversations = len(chat_history.conversations)
total_sessions = len(chat_history.session_embeddings)
```

## Comparison: RAM vs Database Storage

| Feature | RAM Storage | Database Storage |
|---------|-------------|------------------|
| **Speed** | ⚡ Very Fast | 🐌 Slower |
| **Memory** | 📈 Uses RAM | 💾 Uses Disk |
| **Persistence** | ❌ Lost on restart | ✅ Persistent |
| **Scalability** | 🔢 Limited by RAM | 📊 Limited by disk |
| **Complexity** | 🎯 Simple | 🔧 More complex |
| **Setup** | ✅ No setup | ⚙️ Requires setup |

## Best Practices

1. **Monitor Memory Usage**: Keep track of conversation count
2. **Session Cleanup**: Clear old sessions when no longer needed
3. **Embedding Model**: Use efficient embedding models for large datasets
4. **Similarity Threshold**: Consider adding minimum similarity thresholds for retrieval 