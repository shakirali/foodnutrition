# Nutrition-Based Local Food Advisor App — Specifications (Updated)

## 1. Overview

The **Nutrition-Based Local Food Advisor App** is an AI agent–powered application that recommends locally available, economical, and nutrient-rich foods. It uses nutritional datasets, government dietary recommendations, and user-specific attributes (age, gender, dietary needs) to generate personalised, health‑focused suggestions.

The application follows the **agentic architecture defined at [https://xspoonai.github.io/](https://xspoonai.github.io/)**, featuring a primary LLM agent supported by specialised sub‑agents/tools for nutrition lookup, recommendation generation, and local store search.

---

## 2. Purpose & Goals

* Promote healthier eating based on scientific nutritional guidelines.
* Recommend **foods, vegetables, dishes, and packaged items** with high nutrition density and good cost value.
* Provide recommendations using **FoodData Central (USDA)** nutritional dataset:

  * [https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2025-04-24.zip](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2025-04-24.zip)
* Align user recommendations with **age‑ and gender‑specific dietary requirements**:

  * [https://www.nutrition.org.uk/nutritional-information/nutrient-requirements/](https://www.nutrition.org.uk/nutritional-information/nutrient-requirements/)
  * [https://assets.publishing.service.gov.uk/media/5a749fece5274a44083b82d8/government_dietary_recommendations.pdf](https://assets.publishing.service.gov.uk/media/5a749fece5274a44083b82d8/government_dietary_recommendations.pdf)
* Help users compare dishes based on nutritional composition.
* Suggest healthier alternatives based on what the user ate that day.
* Provide local sourcing options (shops, supermarkets) for recommended foods.

---

## 3. Target Users

* Adults and children seeking personalised nutrition guidance.
* Users with dietary restrictions (vegan, halal, gluten-free, etc.).
* Individuals tracking nutritional goals or improving dietary balance.
* Budget-conscious users searching for healthy, economical food options.

---

## 4. Agentic Architecture

The implementation follows **xspoon agentic architecture**, consisting of:

### 4.1 LLM Primary Agent

Responsible for:

* Interacting with user.
* Asking onboarding questions.
* Managing conversation flow.
* Calling sub‑agents/tools as needed.
* Storing user profile and preferences in memory.

### 4.2 Memory System

Stores:

* User name
* Age
* Gender
* Dietary restrictions
* Reported foods eaten for breakfast, lunch, dinner
* Any previously viewed recommendations

### 4.3 Sub‑Agents / Tools

#### **1. Nutrition Lookup Tool**

* Loads and queries USDA FoodData Central dataset.
* Converts raw nutritional info into structured consumable form.
* Computes nutrient density.

#### **2. Dietary Requirements Tool**

* Fetches recommended nutrient intake for age and gender from official guidelines.
* Computes gaps between user's actual vs recommended intake.

#### **3. Recommendation Agent**

* Suggests alternative foods to improve deficient nutrients.
* Ranks foods based on:

  * Nutrient density
  * Affordability
  * Dietary restrictions
  * Local availability (if requested)

#### **4. Comparison Agent**

* Compares two or more dishes/foods by nutritional values.
* Produces structured comparison tables.

#### **5. Local Store Search Tool**

* Uses a search API (e.g., Google Search API or Maps API) to find local shops/superstores.
* Optionally includes availability and price comparisons.

---

## 5. User Interaction Flow

### Step 1 — Greeting & Profile Setup

The LLM agent asks:

* User name (stored in memory)
* Age
* Gender
* Dietary requirements or restrictions

### Step 2 — Daily Diet Intake

Agent asks:

* What did you eat for **breakfast**?
* What did you eat for **lunch**?
* What did you eat for **dinner**?

Foods are parsed and normalised using the nutrition lookup tool.

### Step 3 — Nutritional Analysis

The system compares:

* Consumed nutrients
* Recommended intake for age + gender

Identifies deficiencies or imbalances.

### Step 4 — Suggesting Alternatives

Agent suggests food items that:

* Improve nutritional balance
* Fit user’s dietary needs
* Are economical
* Are locally available (optional)

### Step 5 — Ask About Local Sourcing

Agent asks:

> "Would you like me to show where to buy these items locally?"

If yes → uses local store search tool.

---

## 6. Data Sources

### 6.1 Nutrition Database

* **USDA FoodData Central Foundation Foods Dataset**
* Contains detailed nutrient values per food, including vitamins, minerals, macros.
* Used to calculate nutrient density and compare foods.

### 6.2 Government Nutritional Requirements

* UK recommended nutrient intakes sorted by age and gender.
* Includes RNI (Reference Nutrient Intake) for:

  * Protein
  * Fat
  * Carbohydrates
  * Fibre
  * Vitamins (A, D, E, etc.)
  * Minerals (Iron, Zinc, Calcium, etc.)
* Used for deficiency detection.

### 6.3 Local Store Data

* Google Search / Maps API
* Store APIs where available
* Price comparison tools

---

## 7. Functional Requirements

### **FR1:** Collect and store user profile.

### **FR2:** Parse user dietary intake.

### **FR3:** Retrieve nutrient composition of foods.

### **FR4:** Access government nutrient recommendations.

### **FR5:** Compute nutritional deficiencies.

### **FR6:** Recommend alternative foods.

### **FR7:** Allow dish comparison.

### **FR8:** Ask user whether they want local sourcing.

### **FR9:** Search nearby shops and supermarkets.

### **FR10:** Provide clear explanations of recommendations.

---

## 8. Non-Functional Requirements

* **Latency:** 2–5 seconds per query.
* **Accuracy:** Use verified datasets only.
* **Scalability:** Support many concurrent users.
* **Privacy:** User data stored securely and GDPR compliant.
* **Extensibility:** Ability to add new nutrition guidelines or store APIs.

---

## 9. Outputs

### 9.1 Nutritional Report

* Summary of consumed nutrients
* Gaps vs recommended intake

### 9.2 Food Recommendations

Fields:

* Food name
* Nutrient benefit summary
* Cost estimate
* Availability (if searched)

### 9.3 Comparison Table

| Nutrient | Food A | Food B |
| -------- | ------ | ------ |
| Protein  | 28g    | 14g    |
| Iron     | 12mg   | 3mg    |
| Fibre    | 4g     | 8g     |

### 9.4 Local Store List

* Store name
* Address
* Items available

---

## 10. Future Enhancements

* Meal planning
* Daily nutrition tracking
* User progress dashboard
* Recipe recommendations based on deficiencies
* Barcode scanning

---

## 11. Summary

This updated specification integrates new requirements including USDA nutrition dataset usage, UK nutrient intake guidelines, and the xspoon agentic architecture. The system provides personalised nutritional improvements, actionable alternatives, and searchable local food sourcing functionality.

---

**End of Updated specifications.md**
