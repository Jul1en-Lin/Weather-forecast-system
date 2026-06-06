# Design Spec: Tarot Mystical Background Patterns

## Goal
Enhance the visual aesthetics of the Weather Oracle frontend by adding theme-appropriate mystical background patterns (tarot, constellations, sacred geometry), matching the design intent of the concept maps (`Divinatio-concept-map-lightmode.png` and `Divination-concept-map-darkmode.png`).

## Proposed Assets
We will generate two seamless tileable background textures and save them in the `public/` directory:

1. **Dark Mode Background (`public/mystical_bg_dark.png`)**
   - **Visuals**: Deep dark indigo/obsidian texture with very subtle golden/white constellation lines, stars, and alchemy symbols.
   - **Generation Prompt**: `mystical dark celestial tarot card background pattern, seamless tileable, subtle gold stars, constellations, alchemy lines, sacred geometry, low contrast, deep blue and black obsidian, premium clean texture, flat design, no frame, no device mockups`

2. **Light Mode Background (`public/mystical_bg_light.png`)**
   - **Visuals**: Warm vintage parchment/cream texture with delicate sepia/bronze astrological lines, stars, and tarot symbols.
   - **Generation Prompt**: `mystical light celestial tarot card background pattern, seamless tileable, subtle sepia stars, constellations, alchemy lines, sacred geometry, low contrast, warm parchment cream color, premium clean texture, flat design, no frame, no device mockups`

## Frontend Implementation

### 1. Theme CSS Updates (`src/styles/oracle-theme.css`)
We will define the background pattern assets as CSS variables and apply them to the `.oracle-layout` container.

```css
:root {
  /* ... existing variables ... */
  --oracle-bg-pattern: url('/mystical_bg_dark.png');
}

[data-oracle-theme='light'] {
  /* ... existing variables ... */
  --oracle-bg-pattern: url('/mystical_bg_light.png');
}
```

### 2. Readability & Smooth Transition
To ensure that background details do not interfere with text readability, we will apply the background pattern to a pseudo-element (`::after`) with low opacity (`0.12` for dark mode, `0.08` for light mode). This technique places the pattern on a separate layer above the solid background but below all content.

```css
.oracle-layout {
  min-height: 100vh;
  color: var(--oracle-text);
  position: relative;
  isolation: isolate;
  background: var(--oracle-bg-deep); /* Pure background color */
  display: flex;
  flex-direction: column;
}

.oracle-layout::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image: var(--oracle-bg-pattern);
  background-repeat: repeat;
  background-size: 360px; /* Scale of the tiling pattern */
  opacity: 0.12; /* Default dark mode opacity */
  transition: opacity 0.5s ease, background-image 0.5s ease;
}

[data-oracle-theme='light'] .oracle-layout::after {
  opacity: 0.08; /* Light mode opacity */
}
```

## Verification Plan
1. **Asset Generation**: Confirm that the generated image files are valid, seamless, and correctly placed in `public/`.
2. **Text Readability**: Verify on `/oracle` under both dark and light modes that text, icons, and cards remain clearly readable.
3. **Theme Switch**: Confirm that switching themes fades the background pattern and background colors smoothly.
