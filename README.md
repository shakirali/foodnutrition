# Nutrition-Based Local Food Advisor App

An AI agent-powered application that recommends locally available, economical, and nutrient-rich foods. The app uses nutritional datasets, government dietary recommendations, and user-specific attributes (age, gender, dietary needs) to generate personalized, health-focused suggestions.

Built with [SpoonOS agentic architecture](https://xspoonai.github.io/), featuring a primary LLM agent supported by specialized sub-agents/tools for nutrition lookup, recommendation generation, and local store search.

## 🎯 Features

- **Personalized Nutrition Guidance**: Get recommendations based on your age, gender, and dietary restrictions
- **Daily Diet Analysis**: Track and analyze your breakfast, lunch, and dinner intake
- **Nutritional Gap Detection**: Compare your actual intake with recommended dietary requirements
- **Food Recommendations**: Receive suggestions for foods that improve nutritional balance
- **Dish Comparison**: Compare different dishes based on nutritional composition
- **Local Store Search**: Find nearby shops and supermarkets for recommended foods (coming soon)

## 🏗️ Architecture

The application follows the **xspoon agentic architecture**, consisting of:

### Primary LLM Agent
- Interacts with users to collect profile information
- Manages conversation flow for onboarding
- Calls sub-agents/tools as needed
- Stores user profile and preferences in memory

### Sub-Agents / Tools (Planned)
1. **Nutrition Lookup Tool**: Queries USDA FoodData Central dataset
2. **Dietary Requirements Tool**: Fetches recommended nutrient intake based on age and gender
3. **Recommendation Agent**: Suggests alternative foods to improve deficient nutrients
4. **Comparison Agent**: Compares dishes nutritionally
5. **Local Store Search Tool**: Finds nearby shops and supermarkets

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
   DEFAULT_LLM_TEMPERATURE=0.7
   ```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEFAULT_LLM_PROVIDER` | LLM provider (e.g., openai, anthropic) | `openai` | No |
| `DEFAULT_LLM_API_KEY` | API key for LLM provider | - | Yes |
| `DEFAULT_LLM_TEMPERATURE` | Temperature for LLM responses (0.0-2.0) | `0.7` | No |
| `GOOGLE_API_KEY` | Google API key for local store search | - | No* |
| `GOOGLE_SEARCH_ENGINE_ID` | Google Search Engine ID | - | No* |

*Required only if using local store search feature

**Note**: `DEFAULT_LLM_API_KEY` will fallback to `OPENAI_API_KEY` if not set.

## 💻 Usage

Run the application:

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

5. **Local Sourcing** (optional): Ask to find local stores for recommended foods

### Commands

- Type `exit`, `quit`, or `bye` to end the conversation
- Press `Ctrl+C` to interrupt the conversation

## 📁 Project Structure

```
foodnutrition/
├── agents/
│   └── advisor_agent.py      # Primary NutritionAdvisorAgent class
├── config/
│   ├── __init__.py
│   └── config.py             # Application configuration
├── data/                      # Data directory (for USDA dataset, user memory)
├── tests/                     # Test files
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example                # Environment variables template
├── .env                        # Your environment variables (not in git)
└── README.md                   # This file
```

## 🔧 Development

### Running Tests

```bash
# Tests will be added here
pytest tests/
```

### Code Structure

- **`main.py`**: Entry point that initializes and runs the agent
- **`agents/advisor_agent.py`**: Defines the `NutritionAdvisorAgent` class
- **`config/config.py`**: Manages application configuration and environment variables

## 📊 Data Sources

The application uses (or will use):

- **USDA FoodData Central Foundation Foods Dataset**: [Download](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2025-04-24.zip)
- **UK Government Dietary Recommendations**: [Reference](https://www.nutrition.org.uk/nutritional-information/nutrient-requirements/)
- **Government Dietary Recommendations PDF**: [Download](https://assets.publishing.service.gov.uk/media/5a749fece5274a44083b82d8/government_dietary_recommendations.pdf)

## 🛠️ Dependencies

- `spoon-ai-sdk`: Core SpoonOS agentic architecture framework
- `spoon-toolkits`: Extended toolkits (optional)
- `python-dotenv`: Environment variable management

See `requirements.txt` for the complete list.

## 🚧 Future Enhancements

- [ ] Meal planning
- [ ] Daily nutrition tracking
- [ ] User progress dashboard
- [ ] Recipe recommendations based on deficiencies
- [ ] Barcode scanning
- [ ] Integration with USDA FoodData Central dataset
- [ ] UK dietary requirements integration
- [ ] Local store search functionality

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

