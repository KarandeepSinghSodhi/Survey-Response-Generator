# Survey Form - Quick Start Guide

## Overview

The Survey Form page (`/survey`) allows you to manually input survey responses with an intuitive UI featuring sliders, toggles, and dropdown selectors.

## Step-by-Step Usage

### 1. Navigate to the Survey Form
- From the home page, click **"Add responses manually"**
- Or directly visit `/survey`

### 2. Set Satisfaction Level
- **Slider Range**: 1-5
- **Labels**:
  - 1 = Very Unsatisfied
  - 2 = Unsatisfied
  - 3 = Neutral
  - 4 = Satisfied
  - 5 = Very Satisfied
- Drag the slider to select your rating
- The descriptive label updates in real-time

### 3. Set NPS (Likelihood to Recommend)
- **Slider Range**: 0-10
- **Classifications**:
  - 0-6 = **Detractor** (customer may damage brand)
  - 7-8 = **Passive** (neutral customer)
  - 9-10 = **Promoter** (loyal customer likely to recommend)
- The NPS classification displays automatically
- This is a key metric for customer loyalty

### 4. Select Product Category
- Click one of 4 buttons:
  - **Electronics**
  - **Clothing**
  - **Home**
  - **Other**
- Selected category highlights in purple
- Required for distribution analysis

### 5. Indicate Delivery Status
- Click **Yes** or **No**
- **Yes** = On-time delivery ✓
- **No** = Late or problematic delivery ✗
- Selected option highlights in blue

### 6. Add Optional Feedback
- Enter your thoughts in the textarea
- Topics to consider:
  - Product quality
  - Delivery experience
  - Packaging
  - Value for money
  - Suggestions for improvement
- This field is optional but valuable for qualitative analysis

### 7. Submit Response
- Click **"Add Response"** button
- Success notification shows with total count
- Form automatically resets for next entry
- Response saved to browser storage

## Viewing Your Responses

### Quick Summary (On Page)
After submitting responses, see:
- **Total Responses**: Number of entries added
- **Average Satisfaction**: Mean of all satisfaction ratings
- **Average NPS**: Mean NPS score
- **Top Category**: Most common product category

### Full Report
- Click **"View Report"** button
- See interactive charts and aggregated analytics
- Compare metrics across categories
- Analyze delivery reliability trends

### Response Table
- Click **"View All Responses"** button
- Browse full response data in table format
- Search/filter by category, feedback text, etc.
- Export-ready data structure

## Tips & Best Practices

### 💡 For Accurate Data
- Use the full range of sliders (1-5, 0-10)
- Ensure satisfaction and NPS correlate reasonably
- Write genuine feedback when possible
- Try to represent different customer segments

### 📊 For Better Analysis
- Add at least 10-20 responses for meaningful patterns
- Include responses across all categories
- Mix of on-time and late deliveries for realism
- Vary satisfaction levels to see distribution

### ⚡ Keyboard Shortcuts
- Tab: Move between fields
- Enter: Submit form (when focused on submit button)
- Arrow keys: Adjust sliders

## Data Structure

Each response contains:

```json
{
  "id": 1,
  "satisfaction": 4,
  "nps": 8,
  "category": "Electronics",
  "delivery": "Yes",
  "feedback": "Great product but delivery was delayed"
}
```

## Storage

- Data stored in browser's **localStorage** automatically
- Persists between browser sessions
- Not synced to cloud (local only)
- Clear browser data to reset

## Troubleshooting

### Responses not saving?
- Check browser localStorage is enabled
- Try refreshing the page
- Ensure you're not in private/incognito mode
- Check browser console for errors

### Can't see the report?
- Add at least 1 response first
- Go to `/report` directly
- Check if data exists in responses page

### Form not responding?
- Refresh the page
- Check browser console for JavaScript errors
- Try a different browser
- Clear cache and reload

## Integration with Backend

To connect to a real backend API:

1. **Update Survey Form** (`pages/survey.tsx`)
   - Replace `localStorage.setItem()` with API POST call
   - Add loading and error states

2. **Example Implementation**:
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  const response = await fetch('/api/responses', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  
  if (response.ok) {
    // Success handling
  }
};
```

## Advanced Usage

### Bulk Import
Create a JSON file and import multiple responses:

```json
[
  { "satisfaction": 5, "nps": 9, "category": "Electronics", "delivery": "Yes", "feedback": "Excellent!" },
  { "satisfaction": 3, "nps": 6, "category": "Clothing", "delivery": "No", "feedback": "OK product, late delivery" }
]
```

### Export Data
Currently exports via:
1. View responses page
2. Copy table data
3. Paste into Excel/CSV

Future: Add download button for CSV/JSON export.

## Feedback

Questions or suggestions?
- Check the DEPLOYMENT.md for technical details
- Review the Next.js documentation for customization
- Inspect network requests to debug API calls

---

Happy surveying! 📋✨
