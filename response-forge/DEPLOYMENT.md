# Response Forge - Survey Form Frontend

A beautiful, fully-responsive Next.js frontend for collecting and analyzing survey responses. Deploy on Vercel with one click.

## Features

### 📝 Manual Survey Input
- **Satisfaction Slider**: 1-5 scale with labels
- **NPS Slider**: 0-10 scale with Promoter/Passive/Detractor classification
- **Category Selector**: Choose from Electronics, Clothing, Home, or Other
- **Delivery Toggle**: Yes/No selection
- **Feedback Textarea**: Open-ended comments

### 📊 Analytics & Reporting
- Real-time dashboard with aggregated metrics
- Interactive charts using Recharts
- Response filtering and search
- Summary statistics
- Responsive data tables

### 🎨 Modern UI/UX
- Glass-morphism design
- Dark theme optimized for readability
- Smooth animations and transitions
- Mobile-responsive layout
- Accessible form controls

## Getting Started

### Prerequisites
- Node.js 18.x or higher
- npm or yarn package manager

### Local Development

```bash
cd response-forge

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Pages

- **Home** (`/`): Generate synthetic responses or navigate to other sections
- **Survey Form** (`/survey`): Manually add survey responses with sliders and input fields
- **Report** (`/report`): View aggregated analytics and interactive charts
- **Responses** (`/responses`): Browse all collected responses in a table

## Data Storage

Survey responses are stored in browser `localStorage` for instant access without a backend:

- `survey-responses`: Manually entered responses
- `survey-sensum-responses`: Synthetically generated responses

## Deployment on Vercel

### Option 1: One-Click Deploy

1. Push your code to GitHub
2. Visit [https://vercel.com/new](https://vercel.com/new)
3. Select "Import Git Repository"
4. Choose your repository
5. Click "Deploy"

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project directory
vercel
```

### Option 3: Manual GitHub Integration

1. Go to [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New..."
3. Select "Project"
4. Select your GitHub repository
5. Configure if needed
6. Click "Deploy"

## Environment Setup

No environment variables needed for basic functionality. The app works entirely client-side.

## Building for Production

```bash
npm run build
npm run start
```

## Project Structure

```
response-forge/
├── pages/
│   ├── _app.tsx          # App wrapper with global styles
│   ├── index.tsx         # Home page with generator
│   ├── survey.tsx        # Manual survey form page
│   ├── report.tsx        # Analytics and charts
│   └── responses.tsx     # Response table browser
├── lib/
│   └── generator.ts      # Synthetic data generation logic
├── styles/
│   └── globals.css       # Global styling
├── package.json
├── next.config.mjs
└── tsconfig.json
```

## Technologies Used

- **Next.js 14**: React framework with built-in optimizations
- **React 18**: UI component library
- **TypeScript**: Type-safe JavaScript
- **Recharts**: React charting library
- **Lucide React**: Icon library
- **CSS Grid/Flexbox**: Responsive layout

## Features Breakdown

### Survey Form (`/survey`)
- Satisfaction slider with descriptive labels
- NPS slider with NPS classification display
- Category selection with visual button states
- Delivery status toggle
- Feedback textarea with placeholder
- Real-time response count display
- Quick summary statistics

### Analytics Report (`/report`)
- Total responses and key metrics
- Category distribution pie chart
- Delivery reliability pie chart
- Satisfaction distribution bar chart
- All charts are interactive and responsive

### Response Browser (`/responses`)
- Full response table with sorting
- Search/filter functionality
- Handles both synthetic and manual responses
- Shows all response fields with detailed information

## Usage Examples

### Adding Responses Manually
1. Go to `/survey`
2. Adjust sliders for Satisfaction and NPS
3. Select product category
4. Choose delivery status
5. Add optional feedback
6. Click "Add Response"
7. View summary statistics

### Viewing Analytics
1. Go to `/report`
2. See aggregated metrics at the top
3. Explore interactive charts
4. Drill down into specific categories or metrics

### Searching Responses
1. Go to `/responses`
2. Use search box to filter by category, feedback, etc.
3. Click column headers to sort (if enabled)
4. View raw response data

## API Integration (Future)

To connect to a backend:

1. Create API routes in `pages/api/`
2. Update form submission in `/survey` to POST to your API
3. Replace localStorage with API calls in other pages
4. Add authentication if needed

Example POST endpoint:

```typescript
// pages/api/responses.ts
export default async function handler(req, res) {
  if (req.method === 'POST') {
    // Save to database
    return res.status(201).json({ success: true });
  }
}
```

## Performance Optimizations

- Server-side rendering (SSR) for fast initial loads
- Static generation where possible
- Image optimization via Next.js Image component
- Code splitting and lazy loading
- CSS-in-JS with global styles
- Minimal bundle size

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Data not persisting?
- Check browser localStorage settings
- Ensure cookies/storage are enabled
- Try clearing cache and reloading

### Charts not showing?
- Verify Recharts is installed: `npm install recharts`
- Check console for errors
- Ensure data exists before viewing report

### Build failing on Vercel?
- Check Node.js version compatibility
- Verify all dependencies are in package.json
- Review build logs in Vercel dashboard

## License

MIT

## Support

For issues or questions:
1. Check the code comments
2. Review Next.js documentation
3. Check Recharts documentation
4. Open an issue in the repository

---

Made with ✨ for e-commerce survey analysis.
