# Nutrition-Based Local Food Advisor App

An AI agent-powered application that recommends locally available, economical, and nutrient-rich foods. The app uses nutritional datasets, government dietary recommendations, and user-specific attributes (age, gender, dietary needs) to generate personalized, health-focused suggestions.

Built with [SpoonOS agentic architecture](https://xspoonai.github.io/), featuring a primary LLM agent supported by specialized sub-agents/tools for nutrition lookup, recommendation generation, and local store search.

## 🎯 Features

- **Web Interface** ✅: Modern, responsive web UI with real-time chat interface
- **CLI Interface**: Command-line interface for terminal-based interactions
- **Personalized Nutrition Guidance**: Get recommendations based on your age, gender, and dietary restrictions
- **Daily Diet Analysis**: Track and analyze your breakfast, lunch, and dinner intake
- **Nutritional Gap Detection**: Compare your actual intake with recommended dietary requirements
- **Food Recommendations**: Receive suggestions for foods that improve nutritional balance
- **Nutrition Lookup**: Query USDA FoodData Central database using RAG (Retrieval-Augmented Generation)
- **Dietary Requirements Lookup**: Get age and gender-specific nutrient requirements
- **Dish Comparison**: Compare different dishes based on nutritional composition
- **Local Store Search**: Find nearby shops and supermarkets for recommended foods (coming soon)

## 🏗️ Architecture

The application follows the **xspoon agentic architecture**, consisting of:

### Primary LLM Agent
- Interacts with users to collect profile information
- Manages conversation flow for onboarding
- Calls sub-agents/tools as needed
- Stores user profile and preferences in memory

### Sub-Agents / Tools
1. **Nutrition Lookup Tool** ✅: Queries USDA FoodData Central dataset using RAG
2. **Dietary Requirements Tool** ✅: Fetches recommended nutrient intake based on age and gender
3. **Recommendation Agent** (Planned): Suggests alternative foods to improve deficient nutrients
4. **Comparison Agent** (Planned): Compares dishes nutritionally
5. **Local Store Search Tool** (Planned): Finds nearby shops and supermarkets

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An API key for your chosen LLM provider (OpenAI, Anthropic, etc.)

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd foodnutrition
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   DEFAULT_LLM_PROVIDER=openai
   DEFAULT_LLM_API_KEY=your-api-key-here
   DEFAULT_LLM_MODEL=gpt-4o-mini
   DEFAULT_LLM_TEMPERATURE=0.7
   ```

5. **Set up RAG system** (one-time setup):
   ```bash
   python scripts/setup_rag.py
   ```
   
   This will:
   - Process the USDA FoodData Central JSON file (340 food items)
   - Generate embeddings for all food items using sentence-transformers (local, no API needed)
   - Create a vector database using ChromaDB
   - Store the indexed data in `data/vector_db/`
   
   **Note**: 
   - The first run may take a few minutes to download the embedding model (`all-MiniLM-L6-v2`) and generate embeddings. Subsequent runs will be faster as the model is cached.
   - If the vector database already exists, you'll be prompted to re-index. This is useful if you update the USDA data file.
   - The setup script automatically handles metadata size limits by storing full food data separately and loading it on demand.

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEFAULT_LLM_PROVIDER` | LLM provider (e.g., openai, anthropic) | `openai` | No |
| `DEFAULT_LLM_API_KEY` | API key for LLM provider | - | Yes |
| `DEFAULT_LLM_MODEL` | LLM model name | `gpt-4o-mini` | No |
| `DEFAULT_LLM_TEMPERATURE` | Temperature for LLM responses (0.0-2.0) | `0.7` | No |
| `GOOGLE_API_KEY` | Google API key for local store search | - | No* |
| `GOOGLE_SEARCH_ENGINE_ID` | Google Search Engine ID | - | No* |

*Required only if using local store search feature

**Note**: `DEFAULT_LLM_API_KEY` will fallback to `OPENAI_API_KEY` if not set.

## 💻 Usage

The application can be used in two ways:

### Option 1: Web Interface (Recommended) 🌐

Start the web server:

```bash
python web/run_server.py
```

Or using uvicorn directly:

```bash
uvicorn web.api:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Web Interface Features:**
- Modern, responsive chat interface with real-time messaging
- Quick action buttons for common queries:
  - Analyze Today's Meals
  - Check Requirements
  - Find Foods
  - Compare Foods
- Dark mode support (toggle in header)
- Mobile-friendly responsive design
- Typing indicators for better UX
- Auto-scrolling chat messages

### Option 2: Command-Line Interface (CLI) 💻

Run the application in terminal:

```bash
python main.py
```

Or:

```bash
python3 main.py
```

### User Interaction Flow

1. **Profile Setup**: The agent will ask for:
   - Your name
   - Age
   - Gender
   - Dietary restrictions (vegan, halal, gluten-free, etc.)

2. **Daily Diet Intake**: Share what you ate:
   - Breakfast
   - Lunch
   - Dinner

3. **Nutritional Analysis**: The system will:
   - Analyze your nutritional intake
   - Compare with recommended dietary requirements
   - Identify deficiencies or imbalances

4. **Recommendations**: Receive personalized food suggestions

5. **Nutrition Lookup**: Ask questions like:
   - "What are the nutrients in an apple?"
   - "Find high protein foods"
   - "What foods are rich in iron?"
   - "Show me foods with high calcium"
   - "What are the nutritional values of eggs?"
   
   The agent will use the RAG system to search the USDA database and return detailed nutritional information.

6. **Local Sourcing** (optional): Ask to find local stores for recommended foods

### Commands

- Type `exit`, `quit`, or `bye` to end the conversation
- Press `Ctrl+C` to interrupt the conversation

## 📁 Project Structure

```
foodnutrition/
├── agents/
│   ├── advisor_agent.py              # Primary NutritionAdvisorAgent class
│   └── tools/
│       ├── nutrition_lookup_tool.py          # Nutrition lookup tool using RAG
│       └── dietary_requirements_tool.py       # Dietary requirements lookup tool
├── config/
│   ├── __init__.py
│   └── config.py                      # Application configuration
├── data/
│   ├── FoodData_Central_foundation_food_json_2025-04-24.json  # USDA dataset (340 food items)
│   ├── mineral_requirements.json      # Mineral requirements by age/gender
│   ├── vitamin_recommendations.json   # Vitamin requirements by age/gender
│   ├── nutrition_recommendations.json # Nutrition recommendations by age/gender
│   ├── process_usda_data.py           # Data processing for RAG (USDA data)
│   ├── process_dietary_data.py        # Data processing for dietary requirements
│   ├── vector_store.py                # ChromaDB vector store (USDA nutrition data)
│   ├── dietary_vector_store.py        # ChromaDB vector store (dietary requirements)
│   ├── vector_db/                      # Vector database (USDA data)
│   └── dietary_vector_db/              # Vector database (dietary requirements)
├── web/
│   ├── api.py                         # FastAPI backend
│   ├── run_server.py                  # Web server startup script
│   ├── templates/
│   │   └── index.html                 # Main web page
│   └── static/
│       ├── css/
│       │   └── style.css              # Stylesheet
│       └── js/
│           └── app.js                 # Frontend JavaScript
├── scripts/
│   └── setup_rag.py                   # RAG setup script (both vector databases)
├── tests/                             # Test files
├── main.py                            # CLI application entry point
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                               # Your environment variables (not in git)
├── WEB_APP_DESIGN.md                  # Web app design documentation
└── README.md                          # This file
```

## 🔧 Development

### Running Tests

```bash
# Tests will be added here
pytest tests/
```

### Code Structure

**Backend:**
- **`main.py`**: CLI entry point that initializes and runs the agent
- **`web/api.py`**: FastAPI backend for web interface
- **`web/run_server.py`**: Web server startup script
- **`agents/advisor_agent.py`**: Defines the `NutritionAdvisorAgent` class
- **`agents/tools/nutrition_lookup_tool.py`**: Nutrition lookup tool using RAG
- **`agents/tools/dietary_requirements_tool.py`**: Dietary requirements lookup tool
- **`data/vector_store.py`**: ChromaDB vector store for USDA nutrition data
- **`data/dietary_vector_store.py`**: ChromaDB vector store for dietary requirements
- **`data/process_usda_data.py`**: Processes USDA JSON into searchable documents
- **`data/process_dietary_data.py`**: Processes dietary requirements JSON files
- **`scripts/setup_rag.py`**: One-time setup script for both RAG systems
- **`config/config.py`**: Manages application configuration and environment variables

**Frontend:**
- **`web/templates/index.html`**: Main web page with chat interface
- **`web/static/css/style.css`**: Stylesheet with dark mode support
- **`web/static/js/app.js`**: Frontend JavaScript for chat functionality

### RAG System Architecture

The RAG (Retrieval-Augmented Generation) system uses:
- **ChromaDB**: Local vector database for storing food embeddings
- **Sentence Transformers**: Local embedding model (`all-MiniLM-L6-v2`) - no API calls needed
- **Semantic Search**: Vector similarity search for finding relevant foods based on queries

**Key Implementation Details**:
- Food data is stored with lightweight metadata in ChromaDB
- Full food data is loaded on-demand from the original JSON file to avoid metadata size limits
- The system supports queries like "high protein foods", "foods rich in iron", or specific food names

## 📊 Data Sources

The application uses:

- **USDA FoodData Central Foundation Foods Dataset** ✅: Included in `data/` folder (340 food items)
  - [Download Link](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2025-04-24.zip)
  - Processed and indexed using RAG for semantic search
  - Supports queries by food name, nutrient name, or nutritional properties
  - Full nutritional data available for each food item (calories, protein, vitamins, minerals, etc.)
- **UK Government Dietary Recommendations** ✅: Age and gender-specific nutrient requirements
  - Minerals (iron, calcium, magnesium, etc.)
  - Vitamins (A, B-complex, C, D, etc.)
  - Macronutrients (protein, carbs, fats, fiber)
  - Stored in JSON format and accessible via Dietary Requirements Tool

## 🛠️ Dependencies

**Core:**
- `spoon-ai-sdk`: Core SpoonOS agentic architecture framework
- `spoon-toolkits`: Extended toolkits (optional)
- `python-dotenv`: Environment variable management

**RAG & Data Processing:**
- `chromadb`: Vector database for RAG (local storage, no external service needed)
- `sentence-transformers`: Local embedding generation (no API needed, downloads model on first use)
- `pandas`: Data processing
- `numpy`: Numerical operations

**Web Framework:**
- `fastapi`: Modern web framework for building APIs
- `uvicorn`: ASGI server for FastAPI
- `python-multipart`: For handling form data

See `requirements.txt` for the complete list.

**Note**: All RAG dependencies run locally - no external API calls are required for nutrition lookups.

## 🚧 Future Enhancements

- [x] Web interface with chat UI ✅
- [x] Integration with USDA FoodData Central dataset (RAG implemented) ✅
- [x] UK dietary requirements integration ✅
- [ ] Meal planning
- [ ] Daily nutrition tracking
- [ ] User progress dashboard
- [ ] Recipe recommendations based on deficiencies
- [ ] Barcode scanning
- [ ] Local store search functionality
- [ ] User profile persistence
- [ ] Meal history tracking

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]

## 🙏 Acknowledgments

- [SpoonOS](https://xspoonai.github.io/) for the agentic architecture framework
- USDA FoodData Central for nutritional data
- UK Government for dietary recommendations

---

**Note**: This is an active development project. Some features are planned and not yet implemented.

