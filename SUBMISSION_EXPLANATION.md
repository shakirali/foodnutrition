# Nutrition-Based Local Food Advisor App

---

## Executive Summary

The **Nutrition-Based Local Food Advisor App** is an AI agent-powered application that provides personalized nutrition guidance using verified scientific data. Built on the **SpoonOS framework**, the application integrates USDA nutritional databases, UK government dietary recommendations, and RAG (Retrieval-Augmented Generation) technology to deliver personalized nutrition advice based on user-specific attributes (age, gender, dietary needs).

The application uses local RAG processing for nutrition data lookups, enabling real-time analysis without external API dependencies for the nutrition database, ensuring privacy and cost-efficiency.

---

## 1. What We've Built

### Core Application

A nutrition advisory system that provides:

- **Personalized Nutrition Guidance**: Recommendations tailored to individual age, gender, and dietary restrictions
- **Daily Meal Analysis**: Tracks breakfast, lunch, and dinner to compute nutritional intake and identify gaps
- **Food Lookups**: RAG system for semantic search across 340+ USDA food items
- **Age & Gender-Specific Requirements**: Daily nutrient requirements sourced from UK government guidelines

### Dual Interface

**Web Interface**: Chat-based UI with real-time messaging, quick actions, dark mode, and mobile responsiveness.

**CLI Interface**: Terminal-based interface with complete feature parity for developers and automation.

### Technical Architecture

The application follows the SpoonOS agentic architecture:

- **Primary LLM Agent**: Manages conversation flow, collects user profile, coordinates tool usage
- **Specialized Tools**: Modular tools for nutrition lookup and dietary requirements analysis
- **RAG System**: Local vector database (ChromaDB) for semantic search without external API calls
- **Memory System**: Stores user profile and preferences during conversation

---

## 2. Development Process

### Phase 1: Foundation & RAG Implementation

- Designed agentic architecture following SpoonOS framework
- Processed USDA FoodData Central dataset (340 food items) into searchable documents
- Processed UK government dietary recommendations (minerals, vitamins, nutrition) organized by age/gender
- Implemented ChromaDB vector stores with `all-MiniLM-L6-v2` embeddings for local processing
- Addressed ChromaDB metadata size limitations by implementing on-demand data loading

### Phase 2: Tool Development

**Nutrition Lookup Tool**: Semantic search across USDA database supporting natural language queries like "high protein foods" and "foods rich in iron" with nutritional breakdowns.

**Dietary Requirements Tool**: Parses age/gender from queries, maps to age groups, and returns personalized nutrient requirements.

### Phase 3: Agent Integration

- Integrated tools into primary LLM agent with context-aware tool selection
- Designed flexible conversation flow for context gathering
- Created system prompts to guide agent behavior and tool usage

### Phase 4: Web Interface

**Backend (FastAPI)**: RESTful API with chat endpoint, lifespan event management, and health checks.

**Frontend**: Chat interface with message bubbles, real-time updates, quick actions, dark mode, and responsive design following the design system (Primary Green #10B981, WCAG 2.1 AA compliant).

---

## 3. Technical Implementation

### RAG System Architecture

- **Vector Database**: ChromaDB with two collections (USDA nutrition data, dietary requirements)
- **Embeddings**: `sentence-transformers` with `all-MiniLM-L6-v2` model (384 dimensions), local processing
- **Pipeline**: Load JSON → Transform to searchable documents → Generate embeddings → Store in ChromaDB → Load full data on-demand
- **Performance**: <100ms vector search, 2-5 second total query latency including LLM processing

### Data Sources

- **USDA FoodData Central**: Official Foundation Foods dataset (340 items) with complete nutritional profiles
- **UK Government Recommendations**: Age and gender-specific requirements for minerals, vitamins, and macronutrients
- **Age Group Mapping**: Logic to map user age to predefined groups (1, 2-3, 4-6, 7-10, 11-14, 15-18, 19-64, 65-74, 75+) with edge case handling

### Web Stack

- **Backend**: FastAPI + Uvicorn with lifespan event handling
- **Frontend**: Vanilla JavaScript with modern CSS (Flexbox, Grid, CSS Variables), responsive design
- **Architecture**: RESTful API with real-time chat via polling and static file serving

---

## 4. Key Features

### Implemented Features

1. **Nutrition Lookup Tool**: Semantic search across 340+ USDA foods with natural language query support
2. **Dietary Requirements Tool**: Age/gender-specific recommendations from UK guidelines
3. **Web Interface**: Real-time chat with quick actions, dark mode, and mobile responsiveness
4. **CLI Interface**: Complete feature parity for terminal users
5. **Meal Analysis**: Meal tracking with gap identification against recommended requirements
6. **User Profile Management**: Context-aware collection of name, age, gender, and dietary restrictions

---

## 5. Data Sources & Verification

The application uses verified data sources:

- **USDA FoodData Central**: [Official Dataset](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2025-04-24.zip) — 340 food items with complete nutritional profiles from the United States Department of Agriculture
- **UK Government Recommendations**: [Official Guidelines](https://www.nutrition.org.uk/nutritional-information/nutrient-requirements/) — Age and gender-specific nutrient requirements from the UK Government's dietary recommendations

All data sources are official government publications, regularly updated, and represent established standards in nutritional science.

---

## 6. Performance & Scalability

### Performance Metrics

- **Vector Search**: <100ms for 340 food items
- **Query Latency**: 2-5 seconds (includes LLM + RAG search)
- **Setup Time**: ~2-3 minutes (one-time, includes model download)
- **Memory Usage**: ~500MB (includes embedding model)

### Scalability

- **Local Processing**: RAG system runs locally — no external API calls for nutrition data
- **Modular Design**: Extensible architecture for adding new tools and features
- **Efficient Data Management**: Lazy loading and caching to minimize memory footprint
- **Async Framework**: FastAPI's async architecture supports concurrent user sessions

### Optimization

- **Model Caching**: Embedding model downloaded once, cached for future sessions
- **On-Demand Loading**: Full food data loaded only when needed
- **Vector Search**: Cosine similarity algorithms for efficient retrieval
- **Frontend**: Minimal dependencies, optimized rendering

---

## 7. Future Roadmap

- **Short-term**: Recommendation agent for alternative foods, comparison agent for nutritional analysis, user profile persistence, meal history tracking
- **Medium-term**: Local store search integration, meal planning calendar, progress dashboard, recipe recommendations
- **Long-term**: Barcode scanning, fitness tracker integration, community features, mobile app development

---

## 8. Conclusion

We have developed a Nutrition-Based Local Food Advisor App that:

✅ **Uses Agentic Architecture**: SpoonOS framework for flexible, modular system  
✅ **Provides Personalized Guidance**: Tailored to user's age, gender, and dietary needs  
✅ **Uses Verified Data**: USDA and UK government sources  
✅ **Implements RAG System**: Semantic search with local processing  
✅ **Offers Web Interface**: Responsive chat interface with mobile support  
✅ **Maintains Performance**: Fast queries, local processing, scalable architecture  

The application demonstrates how AI agentic architecture combined with RAG systems can create practical solutions for personalized nutrition guidance. The modular design enables easy extensibility for future enhancements.

---

## Technical Stack

**Backend**: Python 3.8+, SpoonOS SDK, FastAPI, ChromaDB, Sentence Transformers  
**Frontend**: HTML5/CSS3/JavaScript, responsive design, dark mode support  
**Data**: USDA FoodData Central (340 foods), UK Government Recommendations, local vector databases  
**Infrastructure**: Local processing architecture, environment-based configuration, modular extensible design
