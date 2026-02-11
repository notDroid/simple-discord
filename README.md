# Harmony Chat
A fullstack discord/slack based chat app built with FastAPI (backend) and Next.js (frontend) for learning and demonstration purposes.

### Setup
Dependencies:

1. Conda
2. Taskfile
3. Docker and Docker Compose


Create and activate the conda environment:
```bash
conda env create -f environment.yaml
conda activate harmony
python -m pip install -e backend
```

### Run and Test Locally
To run the application locally using Docker Compose, use the following commands:
```bash
task build
task run-local
```

In another terminal, run tests:
```bash
task test
```

### TODO List
- [ ] Implement authentication and authorization
- [ ] Implement pub/sub model for real-time chat updates
- [ ] Implement request/response model for scrolling through chat history
- [ ] Implement caching layer for user-chat membership data to optimize presence checks
- [ ] Deploy app to AWS with terraform and set up CI/CD pipeline

# Implementation Documentation

## Database
We use DynamoDB as our primary database for storing user, chat metadata and chat history data.

### Reasoning
1. Dynamodb is suitable to store real time chat data due to its low latency and high scalability for small message record data model which doesn't require relational operations or complex transactions.
2. User, Chat metadata is relational but can be easily modeled in a denormalized way in DynamoDB with proper partition keys, secondary indexes, and careful use of transactions which makes the implementation simpler and more efficient for our use case. 
    - Although using a relational database is likely a better choice in a real production system.

### Schema Design
Because of these 2 different models we reason about the data access by whether we are accessing user/chat metadata or chat history data and use the appropriate access patterns for each:
1. For user/chat metadata, we use 3 tables: Users, Chats, and UserChats. The Users table stores user information, the Chats table stores chat information, and the UserChats table models the many-to-many relationship between users and chats. 
    - This allows us to efficiently query for a user's chats and a chat's users without needing complex joins and state updates are handled atomically with DynamoDB transactions.
2. For chat history data, we use a single ChatMessages table with a partition key of chat_id and a sort key of ulid. 
    - The ULID allows us to efficiently query for messages in a chat because it encodes a timestamp and ensures lexicographical ordering.

infra/config/tables.json:
```json
{
    "ChatHistory": {
        "TableName": "ChatHistory",
        "BillingMode": "PAY_PER_REQUEST",
        "KeySchema": [
            {"AttributeName": "chat_id", "KeyType": "HASH"},
            {"AttributeName": "ulid", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "chat_id", "AttributeType": "S"},
            {"AttributeName": "ulid", "AttributeType": "S"}
        ]
    },

    "UserData": {
        "TableName": "UserData",
        "BillingMode": "PAY_PER_REQUEST",
        "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"} 
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "EmailIndex",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ]
    },

    "ChatData": {
        "TableName": "ChatData",
        "BillingMode": "PAY_PER_REQUEST",
        "KeySchema": [{"AttributeName": "chat_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "chat_id", "AttributeType": "S"}]
    },
    
    "UserChat": {
        "TableName": "UserChat",
        "BillingMode": "PAY_PER_REQUEST",
        "KeySchema": [
            {"AttributeName": "user_id", "KeyType": "HASH"},
            {"AttributeName": "chat_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "chat_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "ChatIdIndex",
                "KeySchema": [
                    {"AttributeName": "chat_id", "KeyType": "HASH"},
                    {"AttributeName": "user_id", "KeyType": "RANGE"}
                ],
                "Projection": {"ProjectionType": "ALL"}
            }
        ]
    }
}
```

### Data Access Patterns
**Writes:**
1. Transactions: We use DynamoDB transactions to ensure atomic creation of chats and the initial users within it.
    - In the first case we atomically create a chat record, user-chat records for each user in the chat. 
2. Asyncronous batch writes: For operations that can handle eventual consistency like adding users to an existing chat or deleting the history of a chat whose metadata is already deleted, we use asyncronous batch writes to update the relevant tables without blocking the main thread of execution.
3. For user, chat metadata and users message writes we use conditional updates to ensure data integrity and handle concurrent updates:
    - For example, when creating a user_id, chat_id, or chat_message_id (ulid) we use conditional writes to ensure uniqueness.
    - When updating user or chat metadata we use conditional updates (user writes expect the user to not be marked as deletd) and chat writes expect the chat item to exist.

**Reads:**
1. The main read operation we use is querying the ChatMessages table by chat_id to get messages in a chat ordered by timestamp.
    - Since our read/write ratio is about equal we don't use DAX or any other caching layer for chat history data and rely on DynamoDB's low latency for these queries.
    - We offer reads through either a pub/sub model and also have an optional request/response model (when scrolling through chat history).
2. We also very frequently user presence in a chat before allowing chat operations to ensure proper access control.
    - Because this is an extremely repetive check we use redis to cache user-chat membership data and rely on cache invalidation on updates to ensure we minimize latency for these checks while maintaining nearly immediate consistency (although technically a user can still read/write to a chat a bit after they are removed due to lag).

## API Design
The API is made with FastAPI and designed as a RESTful API with the following endpoints:
1. `api/v1/users`: For user registration and management.
    - Includes endpoints for creating users, retrieving user information, and updating user metadata.
2. `api/v1/chats`: For chat creation and management.
    - Includes endpoints for creating chats, retrieving chat information, adding/removing users from chats, and deleting chats and reading/writing chat history.

We use 3 layers of abstraction for our API design:

1. **The API Layer:** which defines the RESTful endpoints and handles request validation and response formatting.
2. **The Service Layer:** which contains the business logic for handling user and chat operations, including interactions with the database and cache.
3. **The Repository Layer:** which abstracts away the details of interacting with DynamoDB and Redis, providing a clean interface for the service layer to perform database operations.

### Authentication and Authorization

### Pub/Sub Model

## Frontend
The frontend is built with Next.js and provides a user interface for interacting with the chat application. It includes features such as user registration, chat creation, and real-time chat updates. The frontend communicates with the backend API to perform these operations and uses WebSockets for real-time updates.

It heavily relies on server-side rendering for fast initial load times while delegating client-side rendering for dynamic interactions and real-time updates. The frontend is designed to be responsive and user-friendly, providing a seamless chat experience across different devices.

We organize our frontend code into features where each feature has 3 parts:
1. `ui/` The UI components for that feature
2. `components/` The client-side logic and state management for that feature
3. `view/` The server side rendering logic for that feature which also serves as the entry point for the feature's route.

styles for the app are organized into a global css file (`app/globals.css`).

We have 2 main features in our frontend:
1. Authentication (user registration and login)
2. Chat (creating chats, viewing chat list, viewing chat history, sending messages)

### Chat Feature
The chat feature includes the UI components for displaying chat messages, the input box for sending messages, and the logic for fetching and updating chat data in real-time. The view handles server-side rendering of the chat page and ensures that the initial chat history is loaded when a user navigates to a chat.

The logic for handling real-time updates is implemented using WebSockets, allowing users to see new messages in a chat without needing to refresh the page. The chat feature also includes functionality for scrolling through chat history, which is implemented using a request/response model to fetch older messages as the user scrolls up.