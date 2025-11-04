# How to Use German Learning Cards

## Starting the Application

1. **Start the server**:
   ```bash
   uv run python main.py
   ```

   Or with auto-reload during development:
   ```bash
   uv run uvicorn main:app --reload
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

## Using the Web Interface

### Card Interaction
1. **First click on card**: Flips the card to reveal the translation
2. **Second click on card**: Loads the next random card

### Buttons
- **Skip Card**: Load a new card without revealing the answer
- **Reload Deck**: Refresh cards from Google Sheets (useful if you update the spreadsheet)

## How It Works

### Frontend (templates/index.html)
- **Pure HTML + CSS**: No JavaScript frameworks, just vanilla JS
- **Tailwind CSS**: Utility-first CSS loaded via CDN
- **HTMX**: Loaded but minimal usage (mostly vanilla JS for simplicity)
- **Responsive Design**: Works on mobile and desktop
- **3D Flip Animation**: CSS-based card flip effect

### Backend (main.py)
- **FastAPI**: Serves both HTML and JSON API endpoints
- **Jinja2 Templates**: Server-side HTML rendering
- **Google Sheets Integration**: Fetches cards from public spreadsheet
- **Caching**: Cards cached in memory for performance

## Code Review Guide

### HTML Structure (templates/index.html)

**CSS Classes (Tailwind)**:
```html
<!-- Container classes -->
bg-gray-100        → Light gray background
min-h-screen       → Minimum 100% viewport height
flex items-center  → Flexbox with vertical centering
p-4                → Padding: 1rem (16px)

<!-- Text classes -->
text-4xl           → Font size: 2.25rem
font-bold          → Font weight: 700
text-gray-800      → Dark gray color

<!-- Button classes -->
bg-blue-600        → Blue background
hover:bg-blue-700  → Darker blue on hover
rounded-lg         → Large border radius
shadow-md          → Medium shadow
```

**Card Flip Mechanism**:
1. `.card-container` - Creates 3D perspective
2. `.card` - The rotating element
3. `.card.flipped` - Adds 180° rotation
4. `.card-face` - Both front and back faces
5. `backface-visibility: hidden` - Hides the back when facing away

**JavaScript Functions**:
```javascript
handleCardClick()  // Handles both flip and next card
loadNewCard()      // Fetches new card from API
reloadCards()      // Reloads deck from Google Sheets
showStatus()       // Displays temporary status messages
```

### API Endpoints (main.py)

```python
GET  /              # HTML page (Jinja2 template)
GET  /api           # API info (JSON)
GET  /card          # Random card (JSON)
POST /cards/reload  # Reload from sheets (JSON)
```

## Customization

### Change Card Colors
Edit the gradients in `templates/index.html`:

```css
/* Front side (German) */
.card-front {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Back side (Translation) */
.card-back {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

### Change Card Size
Adjust the height in CSS:

```css
.card {
    height: 400px;  /* Desktop */
}

@media (max-width: 640px) {
    .card {
        height: 300px;  /* Mobile */
    }
}
```

### Change Flip Animation Speed
Adjust the transition duration:

```css
.card {
    transition: transform 0.6s;  /* 0.6 seconds */
}
```

## Troubleshooting

### "Failed to fetch card" Error
- Check that the backend server is running
- Verify `.env` has correct `GOOGLE_SHEET_URL`
- Ensure the Google Sheet is public (anyone with link can view)

### Card Not Flipping
- Check browser console for JavaScript errors
- Ensure you're clicking on the card itself, not around it
- Try refreshing the page

### Styles Not Loading
- Check your internet connection (Tailwind loads from CDN)
- Clear browser cache
- Check browser console for network errors

## Mobile Usage

The app is fully responsive:
- **Portrait mode**: Recommended for best experience
- **Landscape mode**: Also works, but portrait is better
- **Touch friendly**: Large tap targets for easy mobile use
- **No zoom needed**: Text sized appropriately for mobile

## Browser Compatibility

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

Requires modern browser with CSS transforms and fetch API support.
