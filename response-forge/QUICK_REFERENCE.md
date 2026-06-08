# Response Forge - Quick Reference Card

## 🚀 Quick Start

### Local Development
```bash
cd response-forge
npm install
npm run dev
# Visit http://localhost:3000
```

### Deploy to Vercel
```bash
# Option 1: Push to GitHub and use Vercel dashboard
git push origin main
# Then: vercel.com/new → Select repo → Deploy

# Option 2: Use Vercel CLI
npm install -g vercel
vercel

# Option 3: GitHub integration (automatic on push)
```

## 📋 Pages & Routes

| Route | Purpose | Key Feature |
|-------|---------|------------|
| `/` | Home | Navigate to all sections |
| `/survey` | Survey Form | ⭐ NEW - Input responses with sliders |
| `/report` | Analytics | View charts and metrics |
| `/responses` | Data Table | Browse all responses |

## 🎛️ Form Fields

### Satisfaction Slider
- **Range**: 1-5
- **Labels**: Very Unsatisfied → Very Satisfied
- **Used For**: Overall satisfaction rating

### NPS Slider
- **Range**: 0-10
- **Classification**: 
  - 0-6 = Detractor
  - 7-8 = Passive
  - 9-10 = Promoter
- **Used For**: Likelihood to recommend

### Category Selector
- **Options**: Electronics, Clothing, Home, Other
- **Type**: Button group (single selection)
- **Used For**: Product category analysis

### Delivery Toggle
- **Options**: Yes or No
- **Used For**: On-time delivery tracking

### Feedback Textarea
- **Type**: Free text input
- **Optional**: Yes
- **Used For**: Qualitative feedback

## 📊 Dashboard Metrics

| Metric | Source | Calculation |
|--------|--------|-------------|
| Total Responses | Count | Sum of all responses |
| Avg Satisfaction | Mean | Average of satisfaction scores |
| Avg NPS | Mean | Average of NPS scores |
| On-Time Delivery % | Percentage | (Yes count / Total) × 100 |

## 💾 Data Storage

```javascript
// Data saved in browser localStorage
localStorage.getItem("survey-responses")  // Manual responses
localStorage.getItem("survey-sensum-responses")  // Synthetic data

// Response structure
{
  id: 1,
  satisfaction: 4,
  nps: 8,
  category: "Electronics",
  delivery: "Yes",
  feedback: "Great product!"
}
```

## 🎨 Key Files

| File | Purpose | Status |
|------|---------|--------|
| `pages/survey.tsx` | Form page | ⭐ NEW |
| `pages/report.tsx` | Analytics | Modified |
| `pages/responses.tsx` | Data table | Modified |
| `pages/index.tsx` | Home | Modified |
| `DEPLOYMENT.md` | Deploy guide | ⭐ NEW |
| `SURVEY_GUIDE.md` | User guide | ⭐ NEW |
| `SUMMARY.md` | Overview | ⭐ NEW |

## 🔧 Common Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Create production build
npm run start        # Run production build
npm run lint         # Check code quality

# Git
git add .
git commit -m "message"
git push origin main  # Deploy to Vercel
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `npx kill-port 3000` or use `npm run dev -- -p 3001` |
| Module not found | Run `npm install` again |
| Data not saving | Check browser localStorage permissions |
| Build errors | Clear `.next` folder and rebuild |

## 📱 Responsive Breakpoints

- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 320px - 767px

All pages fully responsive across all sizes.

## 🎯 Next Actions

- [ ] Test form locally: `npm run dev`
- [ ] Submit test responses
- [ ] View report and responses
- [ ] Push to GitHub
- [ ] Deploy to Vercel
- [ ] Share survey link with users
- [ ] Collect feedback

## 📞 Documentation Links

- **Full Deployment Guide**: `DEPLOYMENT.md`
- **User Guide**: `SURVEY_GUIDE.md`
- **Project Summary**: `SUMMARY.md`

## ✨ Features Summary

✅ Interactive sliders (satisfaction, NPS)
✅ Category selection
✅ Delivery status toggle
✅ Feedback input
✅ Real-time metrics
✅ localStorage persistence
✅ Analytics dashboard
✅ Response browsing
✅ Responsive design
✅ Production-ready

## 📈 Data Collection Best Practices

1. Add at least 20 responses for meaningful analysis
2. Try different categories
3. Mix on-time and late deliveries
4. Vary satisfaction levels
5. Include qualitative feedback

---

**Status**: ✅ Ready for Vercel Deployment  
**Last Build**: Successful (6 pages generated)  
**Bundle Size**: ~2MB uncompressed, optimized for Vercel

