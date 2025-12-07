# Nutrition-Based Local Food Advisor App - Web App Design

## 1. Design Overview

### 1.1 Design Philosophy
- **Clean & Modern**: Minimalist interface with focus on content
- **User-Centric**: Conversational AI-first experience
- **Accessible**: WCAG 2.1 AA compliant
- **Responsive**: Mobile-first design approach
- **Trustworthy**: Scientific data presentation with clear sources

### 1.2 Color Palette

**Primary Colors:**
- Primary Green: `#10B981` (Healthy, fresh, natural)
- Primary Dark: `#059669` (Hover states, emphasis)
- Primary Light: `#D1FAE5` (Backgrounds, highlights)

**Secondary Colors:**
- Accent Orange: `#F59E0B` (Warnings, important info)
- Accent Blue: `#3B82F6` (Information, links)
- Accent Red: `#EF4444` (Deficiencies, alerts)

**Neutral Colors:**
- Background: `#FFFFFF` (Light mode), `#1F2937` (Dark mode)
- Surface: `#F9FAFB` (Light mode), `#374151` (Dark mode)
- Text Primary: `#111827` (Light mode), `#F9FAFB` (Dark mode)
- Text Secondary: `#6B7280` (Light mode), `#9CA3AF` (Dark mode)
- Border: `#E5E7EB` (Light mode), `#4B5563` (Dark mode)

### 1.3 Typography

**Font Family:**
- Primary: `Inter` or `System UI` (Clean, readable)
- Headings: `Inter Bold` or `System UI Bold`
- Code/Data: `JetBrains Mono` or `Monaco` (For nutritional data tables)

**Font Sizes:**
- H1: `32px` / `2rem` (Page titles)
- H2: `24px` / `1.5rem` (Section headers)
- H3: `20px` / `1.25rem` (Subsection headers)
- Body: `16px` / `1rem` (Default text)
- Small: `14px` / `0.875rem` (Captions, metadata)
- Tiny: `12px` / `0.75rem` (Labels, badges)

### 1.4 Spacing System
- Base unit: `4px`
- Spacing scale: `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`

### 1.5 Component Library

**Buttons:**
- Primary: Green background, white text, rounded corners (8px)
- Secondary: White background, green border, green text
- Text: Transparent background, green text
- Sizes: Small (32px), Medium (40px), Large (48px)

**Input Fields:**
- Border: 1px solid, rounded (8px)
- Padding: 12px 16px
- Focus: Green border (2px), shadow

**Cards:**
- Background: White/Surface color
- Border: 1px solid border color
- Border radius: 12px
- Shadow: Subtle elevation (0 1px 3px rgba(0,0,0,0.1))
- Padding: 24px

---

## 2. Page Layouts

### 2.1 Main Layout Structure

```
┌─────────────────────────────────────────┐
│           Header / Navigation           │
├─────────────────────────────────────────┤
│                                         │
│         Main Content Area               │
│    (Chat Interface / Dashboard)         │
│                                         │
├─────────────────────────────────────────┤
│           Footer (Optional)             │
└─────────────────────────────────────────┘
```

### 2.2 Header Component

**Elements:**
- Logo (left): App name + icon
- Navigation (center): Links to Dashboard, History, Settings
- User Profile (right): Avatar, name dropdown menu

**Features:**
- Sticky header (scrolls with content)
- Dark mode toggle
- Notification bell (if recommendations available)

---

## 3. Core Pages & Components

### 3.1 Landing / Chat Page

**Layout:**
```
┌─────────────────────────────────────────┐
│              Header                     │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │   Chat Container                 │  │
│  │                                  │  │
│  │  [Welcome Message]               │  │
│  │  [User Input Field]              │  │
│  │                                  │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │   Quick Actions                  │  │
│  │   [Analyze Today's Meals]        │  │
│  │   [Check Requirements]            │  │
│  │   [Find Foods]                   │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**Chat Interface Components:**

1. **Message Bubbles:**
   - User messages: Right-aligned, blue background
   - Agent messages: Left-aligned, white/gray background
   - Typing indicator: Animated dots
   - Timestamp: Small, muted text below messages

2. **Input Area:**
   - Text input field (multiline, auto-resize)
   - Send button (green, with icon)
   - Attachment button (for future: image upload)
   - Voice input button (for future: speech-to-text)

3. **Quick Actions Panel:**
   - Card-based buttons for common actions
   - Icons + text labels
   - Hover effects

---

### 3.2 Profile Setup Modal / Onboarding Flow

**Step 1: Welcome**
```
┌─────────────────────────────────────────┐
│  👋 Welcome to Nutrition Advisor!       │
│                                         │
│  I'm here to help you achieve your      │
│  nutrition goals. Let's get started!    │
│                                         │
│  What's your name?                      │
│  [________________________]            │
│                                         │
│              [Continue]                 │
└─────────────────────────────────────────┘
```

**Step 2: Basic Info**
```
┌─────────────────────────────────────────┐
│  Hi [Name]! 👋                          │
│                                         │
│  To provide personalized recommendations│
│  I need a few details:                  │
│                                         │
│  Age:     [____] years                  │
│  Gender:  [○] Male  [○] Female         │
│                                         │
│  Dietary Restrictions:                  │
│  ☐ Vegan  ☐ Vegetarian  ☐ Halal        │
│  ☐ Gluten-free  ☐ Other: [_____]      │
│                                         │
│  [Back]              [Continue]        │
└─────────────────────────────────────────┘
```

**Step 3: Goals (Optional)**
```
┌─────────────────────────────────────────┐
│  What are your nutrition goals?         │
│  (You can skip this for now)            │
│                                         │
│  ☐ Weight loss                          │
│  ☐ Muscle gain                          │
│  ☐ Better energy                        │
│  ☐ Improve specific nutrients           │
│  ☐ General health improvement           │
│                                         │
│  [Skip]              [Continue]        │
└─────────────────────────────────────────┘
```

---

### 3.3 Daily Diet Intake Page

**Layout:**
```
┌─────────────────────────────────────────┐
│  Today's Meals                          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │ Breakfast│  │  Lunch   │  │Dinner│ │
│  ├──────────┤  ├──────────┤  ├──────┤ │
│  │          │  │          │  │      │ │
│  │ [Add]    │  │ [Add]    │  │[Add] │ │
│  └──────────┘  └──────────┘  └──────┘ │
│                                         │
│  [Analyze Nutrition]                   │
│                                         │
└─────────────────────────────────────────┘
```

**Meal Card Component:**
- Header: Meal name + time
- Food list: Chips/tags for each food item
- Add button: Opens food search modal
- Edit/Delete: Hover actions on food items

**Food Search Modal:**
- Search input (autocomplete)
- Results list (from USDA database)
- Add to meal button

---

### 3.4 Nutritional Analysis Dashboard

**Layout:**
```
┌─────────────────────────────────────────┐
│  Your Nutrition Analysis                │
│  Date: [Today]                          │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Summary Cards                   │  │
│  │  [Calories] [Protein] [Carbs]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Daily Requirements vs Intake   │  │
│  │  [Progress Bars / Charts]        │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Deficiencies & Surpluses        │  │
│  │  [List with indicators]         │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [View Recommendations]                 │
│                                         │
└─────────────────────────────────────────┘
```

**Components:**

1. **Summary Cards:**
   - Large number (current intake)
   - Small text (recommended)
   - Progress bar (percentage)
   - Color coding (green = good, yellow = moderate, red = low)

2. **Nutrient Progress Bars:**
   - Horizontal bars for each nutrient
   - Color-coded (green/yellow/red)
   - Tooltip on hover (exact values)
   - Grouped by category (Minerals, Vitamins, Macronutrients)

3. **Deficiency Alerts:**
   - Red badge with warning icon
   - Nutrient name + gap amount
   - "Find foods rich in [nutrient]" link

---

### 3.5 Food Recommendations Page

**Layout:**
```
┌─────────────────────────────────────────┐
│  Recommended Foods                      │
│  Based on your nutritional needs        │
├─────────────────────────────────────────┤
│                                         │
│  Sort by: [Relevance ▼] [Price] [Nutr] │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Food Card 1                     │  │
│  │  [Image]  Name: Apple            │  │
│  │          Benefits: High in Fiber │  │
│  │          Cost: $2.50/kg          │  │
│  │          [View Details] [Add]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Food Card 2                     │  │
│  │  ...                             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [Find Local Stores]                   │
│                                         │
└─────────────────────────────────────────┘
```

**Food Card Component:**
- Image placeholder (or icon)
- Food name (bold)
- Key benefits (bullet points)
- Nutrient highlights (chips/badges)
- Cost estimate (if available)
- Actions: View details, Add to meal, Find stores

**Food Detail Modal:**
- Full nutritional table
- Comparison with similar foods
- Serving size information
- "Add to meal" button

---

### 3.6 Food Comparison Page

**Layout:**
```
┌─────────────────────────────────────────┐
│  Compare Foods                          │
├─────────────────────────────────────────┤
│                                         │
│  Select foods to compare:               │
│  [Food 1: Apple ▼] [Food 2: Orange ▼]  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Comparison Table               │  │
│  │                                 │  │
│  │  Nutrient  │ Apple │ Orange    │  │
│  │  ──────────┼───────┼───────────│  │
│  │  Calories  │  52   │   47     │  │
│  │  Protein   │  0.3g │   0.9g   │  │
│  │  ...       │  ...  │   ...    │  │
│  │                                 │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [Add More Foods]                       │
│                                         │
└─────────────────────────────────────────┘
```

**Comparison Table:**
- Sortable columns
- Highlight differences (color-coded)
- Expandable rows for detailed nutrients
- Export option (CSV, PDF)

---

### 3.7 Local Stores Page

**Layout:**
```
┌─────────────────────────────────────────┐
│  Nearby Stores                          │
│  For: [Selected Foods]                  │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  Store Card 1                    │  │
│  │  🏪 Store Name                   │  │
│  │  📍 Address                      │  │
│  │  📞 Phone                        │  │
│  │  ⭐ Rating: 4.5                  │  │
│  │  🛒 Available: Apple, Orange     │  │
│  │  [Directions] [Call]            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [Map View] [List View]                │
│                                         │
└─────────────────────────────────────────┘
```

**Map View:**
- Interactive map (Google Maps integration)
- Markers for each store
- Info windows with store details
- Route planning

---

## 4. User Flows

### 4.1 First-Time User Flow

```
1. Landing Page
   ↓
2. Welcome Modal (Name)
   ↓
3. Profile Setup (Age, Gender, Restrictions)
   ↓
4. Goals (Optional)
   ↓
5. Main Chat Interface
   ↓
6. Agent asks: "How can I help you today?"
```

### 4.2 Daily Analysis Flow

```
1. User clicks "Analyze Today's Meals"
   ↓
2. Meal Entry Page (Breakfast, Lunch, Dinner)
   ↓
3. User adds foods (Search & Add)
   ↓
4. Click "Analyze"
   ↓
5. Analysis Dashboard
   ↓
6. View Recommendations
   ↓
7. (Optional) Find Local Stores
```

### 4.3 Quick Nutrition Lookup Flow

```
1. User types: "What nutrients are in an apple?"
   ↓
2. Agent uses NutritionLookupTool
   ↓
3. Display results in chat
   ↓
4. User can: Compare, Add to meal, Get more info
```

### 4.4 Requirements Check Flow

```
1. User asks: "How much nutrition do I need?"
   ↓
2. Agent uses DietaryRequirementsTool
   ↓
3. Display personalized requirements
   ↓
4. User can: Save, Compare with intake, Get recommendations
```

---

## 5. Component Specifications

### 5.1 Chat Message Component

**Props:**
- `message`: string (message text)
- `sender`: 'user' | 'agent'
- `timestamp`: Date
- `attachments`: Array (for future: images, links)
- `actions`: Array (buttons for recommendations, etc.)

**States:**
- Default
- Typing (for agent messages)
- Error (if tool call fails)

**Styling:**
- User: Right-aligned, blue background (#3B82F6)
- Agent: Left-aligned, white/gray background
- Max width: 70% of container
- Border radius: 12px (first), 4px (middle), 12px (last)

### 5.2 Nutrient Progress Bar

**Props:**
- `nutrient`: string (name)
- `current`: number (current intake)
- `recommended`: number (recommended intake)
- `unit`: string (g, mg, mcg, etc.)
- `category`: 'mineral' | 'vitamin' | 'macro'

**Visual:**
- Horizontal bar
- Color: Green (100%+), Yellow (50-99%), Red (<50%)
- Tooltip on hover
- Percentage label

### 5.3 Food Card

**Props:**
- `food`: Food object (name, nutrients, image, cost)
- `onAdd`: Function (add to meal)
- `onViewDetails`: Function (open detail modal)
- `onFindStores`: Function (navigate to stores)

**Layout:**
- Image/Icon (left)
- Name + Benefits (center)
- Actions (right)
- Responsive: Stack on mobile

### 5.4 Comparison Table

**Props:**
- `foods`: Array of Food objects
- `nutrients`: Array of nutrient names to compare
- `sortable`: boolean

**Features:**
- Sortable columns
- Highlight best/worst values
- Expandable rows
- Export functionality

---

## 6. Responsive Design

### 6.1 Breakpoints

- Mobile: `320px - 767px`
- Tablet: `768px - 1023px`
- Desktop: `1024px+`

### 6.2 Mobile Adaptations

**Chat Interface:**
- Full-width messages
- Bottom-fixed input
- Swipe to dismiss suggestions

**Dashboard:**
- Stack cards vertically
- Collapsible sections
- Bottom navigation bar

**Tables:**
- Horizontal scroll
- Card view option
- Expandable rows

### 6.3 Tablet Adaptations

- 2-column layout for cards
- Side-by-side comparison
- Collapsible sidebar navigation

---

## 7. Accessibility Features

### 7.1 Keyboard Navigation
- Tab order: Logical flow
- Focus indicators: Clear, visible
- Shortcuts: Common actions (Ctrl+K for search)

### 7.2 Screen Reader Support
- ARIA labels on all interactive elements
- Semantic HTML (header, nav, main, footer)
- Alt text for images/icons
- Live regions for dynamic content

### 7.3 Visual Accessibility
- High contrast mode support
- Font size adjustment
- Color-blind friendly palette
- Focus indicators (2px solid outline)

---

## 8. Performance Considerations

### 8.1 Loading States
- Skeleton screens for data loading
- Progress indicators for tool calls
- Optimistic UI updates

### 8.2 Caching
- Cache user profile
- Cache recent searches
- Cache nutritional data

### 8.3 Optimization
- Lazy load images
- Virtual scrolling for long lists
- Debounce search inputs
- Code splitting for routes

---

## 9. Dark Mode

### 9.1 Color Scheme
- Background: Dark gray (#1F2937)
- Surface: Medium gray (#374151)
- Text: Light gray (#F9FAFB)
- Accents: Same as light mode (adjusted opacity)

### 9.2 Implementation
- System preference detection
- Manual toggle in header
- Persist user preference
- Smooth transition animation

---

## 10. Future Enhancements UI

### 10.1 Meal Planning
- Calendar view
- Drag-and-drop meal assignment
- Shopping list generation

### 10.2 Progress Dashboard
- Weekly/monthly charts
- Goal tracking
- Achievement badges

### 10.3 Recipe Recommendations
- Recipe cards with images
- Step-by-step instructions
- Nutritional breakdown per serving

### 10.4 Barcode Scanner
- Camera interface
- Product lookup
- Quick add to meal

---

## 11. Design Mockups Summary

### Key Screens:
1. **Landing/Chat Page**: Primary interface with conversational AI
2. **Profile Setup**: Multi-step onboarding modal
3. **Meal Entry**: Card-based meal input interface
4. **Analysis Dashboard**: Visual nutrition breakdown
5. **Recommendations**: Grid/list of food suggestions
6. **Comparison**: Table view for food comparison
7. **Local Stores**: Map and list view of nearby stores

### Design Principles:
- **Simplicity**: Clean, uncluttered interface
- **Clarity**: Clear data visualization
- **Engagement**: Conversational, friendly tone
- **Trust**: Scientific data presentation
- **Accessibility**: Inclusive design for all users

---

**End of Web App Design Document**

