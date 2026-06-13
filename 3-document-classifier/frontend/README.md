# Document Classifier Frontend

HTML/JS UI for document classification. Sends descriptions to backend, displays results with confidence scores.

## Quick Start

No build required. Just open in browser or deploy to Vercel.

```bash
# Local development
cd frontend
python3 -m http.server 8000
# Open http://localhost:8000
```

## Features

- **Real-time Classification** — Submit description, get instant results
- **Confidence Display** — Shows % for doc_type, name, DOB
- **Action Highlights** — Color-coded (approve=green, needs_review=yellow, decline=red)
- **Raw JSON** — View full response for debugging
- **Mobile Responsive** — Works on phone/tablet/desktop
- **Error Handling** — Shows clear error messages

## UI

┌─────────────────────────────────────┐
│     Document Classifier             │
│  Classify Indian KYC documents      │
├─────────────────────────────────────┤
│                                     │
│  [Textarea: Describe document...]   │
│  [Classify Document Button]         │
│                                     │
├─────────────────────────────────────┤
│  RESULTS                            │
│  ┌──────────────┬──────────────┐    │
│  │ Doc Type     │ Name         │    │
│  │ passport 95% │ John Doe 95% │    │
│  ├──────────────┼──────────────┤    │
│  │ DOB          │ Action       │    │
│  │ 15-05-1990   │ APPROVE ✅   │    │
│  │ 95%          │              │    │
│  └──────────────┴──────────────┘    │
│                                     │
│  [Raw JSON dropdown]                │
└─────────────────────────────────────┘

## Configuration

Update backend URL in `app.js`:

```javascript
const API_BASE = 'https://ai-projects-production-f96b.up.railway.app';
// Change this to your Railway backend URL
```

## Files

- **`index.html`** — Structure, form, result containers
- **`app.js`** — API integration, DOM updates, error handling
- **`styles.css`** — Responsive design, animations

## How It Works

### 1. User Input

```html
<textarea id="description" placeholder="Describe the document..."></textarea>
```

### 2. Form Submit

```javascript
form.addEventListener('submit', async (e) => {
    const description = descriptionInput.value.trim();
    
    const response = await fetch(`${API_BASE}/classify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description })
    });
    
    const data = await response.json();
});
```

### 3. Display Result

```javascript
function displayResult(data) {
    document.getElementById('docType').textContent = data.doc_type;
    document.getElementById('docTypeConf').textContent = `(${(data.doc_type_confidence * 100).toFixed(0)}%)`;
    // ... repeat for name, dob, action
    resultDiv.classList.remove('hidden');
}
```

### 4. Show Action with Color

```javascript
const actionEl = document.getElementById('action');
actionEl.textContent = data.action.toUpperCase();
actionEl.className = `value action ${data.action}`;
// CSS: .action.approve { background: #d4edda; color: #155724; }
```

## Styling

**Color Scheme:**
- **Approve (green)** — `#d4edda` background, `#155724` text
- **Needs Review (yellow)** — `#fff3cd` background, `#856404` text
- **Decline (red)** — `#f8d7da` background, `#721c24` text

**Layout:**
- Gradient background (purple)
- 2-column grid for results (responsive to 1-column on mobile)
- Smooth transitions and hover effects

## Deployment (Vercel)

```bash
# One-click deploy
# 1. Push frontend/ folder to GitHub
# 2. Go to vercel.com → New Project → Import Git Repo
# 3. Select repository
# 4. Deploy
```

Or use Vercel CLI:

```bash
npm i -g vercel
vercel
```

## Error Handling

**Network Error:**
"Application failed to respond"

**Validation Error:**
"Classification validation failed: value is not a valid number"

**Missing Field:**
"Missing 'description' field"

## Testing Locally

```bash
# Start simple HTTP server
python3 -m http.server 8000

# Open http://localhost:8000
# Try: "Valid passport with my name John Doe, DOB 15-05-1990"
```

## Performance

- **Load Time:** <500ms (static HTML/JS)
- **Classification Latency:** 2-3 seconds (backend + OpenAI)
- **No build step:** Just HTML/JS/CSS

## Accessibility

- Semantic HTML (`<label>`, `<form>`, `<button>`)
- Color contrast (WCAG AA)
- Keyboard navigation (Tab, Enter)
- Error messages clear and visible

## Mobile Responsive

**Desktop (600px+):**
- 2-column grid for results
- Wider textarea

**Mobile (<600px):**
- 1-column grid (stacked)
- Full-width inputs
- Touch-friendly buttons

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

(Requires `fetch` API and modern CSS Grid)

## Future Enhancements

- Image upload (send to OCR before classification)
- Real-time form validation
- Offline mode (cache previous results)
- Dark mode toggle
- Multi-language support (Hindi, regional languages)

## Files Structure
frontend/
├── index.html      # Form + result containers
├── app.js          # API integration logic
├── styles.css      # Responsive design
└── README.md       # This file

## Code Example

**Classify a document:**

```html
<textarea>Passport with name John Doe, DOB 15-05-1990, valid until 2030</textarea>
<button>Classify Document</button>

<!-- Result appears here -->
<div id="result">
  <div>Document Type: passport (95%)</div>
  <div>Name: John Doe (95%)</div>
  <div>DOB: 15-05-1990 (95%)</div>
  <div>Action: APPROVE ✅</div>
</div>
```

## Troubleshooting

**Blank screen:**
- Check browser console (F12) for errors
- Verify backend URL in `app.js`
- Check CORS headers from backend

**"Application failed to respond":**
- Backend is down or unreachable
- Check Railway deployment status
- Verify network in browser DevTools

**"Cannot read property 'success' of undefined":**
- Backend returned non-JSON response
- Check backend logs on Railway

## Support

1. Check browser console (F12 → Console tab)
2. Check backend logs: `railway logs --service 3-document-classifier`
3. Test backend directly: `curl https://your-backend/health`

---

