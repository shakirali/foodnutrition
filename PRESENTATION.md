# Nutrition-Based Local Food Advisor App
## 5-Slide Presentation

---

## Slide 1: The Problem & Solution

# Nutrition-Based Local Food Advisor App

### The Challenge
- **Nutritional Confusion**: People struggle to understand their daily nutritional needs
- **Lack of Personalization**: Generic advice doesn't account for age, gender, or dietary restrictions
- **Information Overload**: Too many sources, hard to find reliable data

### Our Solution
**AI-powered personalized nutrition guidance** using:
- ✅ Verified scientific data (USDA FoodData Central + UK Government recommendations)
- ✅ Age and gender-specific dietary requirements
- ✅ RAG system for intelligent food lookups
- ✅ Modern web interface with conversational AI

---

## Slide 2: Architecture & Technology

### SpoonOS Agentic Architecture

```
┌─────────────────────────────────────────┐
│      Primary LLM Agent                   │
│  (Conversation & Coordination)          │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐
│Nutrition│ │Dietary│
│ Lookup │ │Reqs   │
│  (RAG) │ │ Tool  │
└────────┘  └───────┘
```

### Key Technologies
- **RAG System**: ChromaDB + Sentence Transformers (local, no API calls)
- **Backend**: FastAPI + Python
- **Frontend**: Modern responsive web UI with dark mode
- **Data**: 340+ USDA foods + UK dietary recommendations

---

## Slide 3: Core Features

### Implemented Capabilities ✅

**1. Nutrition Lookup Tool**
- Semantic search across 340+ USDA foods
- Natural language queries: "high protein foods", "foods rich in iron"
- Detailed nutritional breakdowns

**2. Dietary Requirements Tool**
- Age and gender-specific recommendations
- Covers minerals, vitamins, macronutrients
- Based on UK Government guidelines

**3. Web Interface**
- Real-time chat interface
- Quick actions: Analyze meals, Check requirements, Find foods
- Mobile-responsive with dark mode

**4. Meal Analysis**
- Track breakfast, lunch, dinner
- Compare intake vs. recommended requirements
- Identify nutritional gaps

---

## Slide 4: Technical Highlights

### What Makes This Special

**Local RAG System**
- No external API calls for nutrition data
- Fast semantic search (<100ms)
- Handles 340+ food items efficiently

**Agentic Architecture**
- Modular tool system
- Extensible design
- Natural conversation flow

**Scientific Data Sources**
- USDA FoodData Central (official government data)
- UK Government dietary recommendations
- Verified, reliable information

**Performance**
- 2-5 second response times
- Efficient vector search
- Scalable architecture

---

## Slide 5: Impact & Next Steps

### Benefits

✅ **Personalized**: Tailored to age, gender, dietary restrictions  
✅ **Scientific**: Based on verified government data  
✅ **Accessible**: Easy-to-use conversational interface  
✅ **Actionable**: Clear recommendations with explanations  

### Future Enhancements

- 🚧 Recommendation agent for alternative foods
- 🚧 Local store search integration
- 🚧 Meal planning and progress tracking
- 🚧 Recipe recommendations based on deficiencies

### Demo

**Try it now:**
```bash
python web/run_server.py
# Visit http://localhost:8000
```

**Making personalized nutrition guidance accessible to everyone**

---

**End of Presentation**

