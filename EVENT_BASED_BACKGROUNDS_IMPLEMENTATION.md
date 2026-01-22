# EVENT-BASED BACKGROUND IMPLEMENTATION

## Overview
Implemented event-based background rules with dual-layer support (hero + scroll backgrounds) for wedding invitation platform.

## Implementation Details

### 1. Backend Changes

#### Models (`/app/backend/models.py`)
- **Updated `EventBackgroundConfig` model** to support dual-layer backgrounds:
  - `hero_background_id`: Background for hero/top section
  - `scroll_background_id`: Background for scroll/body section
  - Legacy fields maintained for backward compatibility

### 2. Frontend Configuration

#### New Configuration File (`/app/frontend/src/config/eventBackgroundConfig.js`)
Created comprehensive event background configuration with the following EVENT RULES:

**ENGAGEMENT:**
- Hero: Lord backgrounds (religious deities)
- Scroll: Rings & flowers backgrounds
- 4 lord options + 5 ring/flower options

**MARRIAGE:**
- Hero: Temple + Lord backgrounds
- Scroll: Same temple + lord (full coverage)
- 4 lord options for both layers

**RECEPTION:**
- Hero: Royal/classy backgrounds
- Scroll: Royal backgrounds OR optional lord backgrounds
- 4 royal options + lord options

**HALDI:**
- Hero: Trendy yellow backgrounds (NO lord allowed)
- Scroll: Trendy yellow backgrounds (NO lord allowed)
- 4 yellow-themed options (turmeric, bindelu, florals, abstract)

**MEHENDI:**
- Hero: Trendy green backgrounds (NO lord allowed)
- Scroll: Trendy green backgrounds (NO lord allowed)
- 4 green-themed options (mehendi patterns, leaves, paisley, abstract)

**Key Functions:**
- `getEventBackgroundConfig(eventType)`: Get configuration for specific event
- `getBackgroundById(backgroundId)`: Retrieve background asset by ID
- `allowsLordBackgrounds(eventType)`: Check if lord backgrounds allowed
- `prohibitsLordBackgrounds(eventType)`: Check if lord backgrounds prohibited
- `getDefaultBackgrounds(eventType)`: Get default background IDs

### 3. Admin UI Updates

#### ProfileForm Component (`/app/frontend/src/pages/ProfileForm.jsx`)
- **Updated imports** to use new `eventBackgroundConfig.js`
- **Replaced EventBackgroundSelector component** with enhanced dual-layer selector:
  - Displays hero and scroll background sections separately
  - Auto-enforces lord background rules (disabled for Haldi/Mehendi)
  - Visual distinction with colored bars (rose for hero, purple for scroll)
  - Preview info showing selected backgrounds
  - Lazy loading of background thumbnails

**UI Features:**
- Gradient background for the selector
- Separate cards for hero and scroll layers
- Check marks on selected backgrounds
- Descriptive labels and helper text
- Performance-safe with lazy loading

### 4. Public Invitation Updates

#### PublicInvitation Component (`/app/frontend/src/pages/PublicInvitation.jsx`)
- **Created DualLayerBackground component**:
  - Progressive image loading (thumbnail → full size)
  - Scroll-based opacity transitions
  - Hero background fades out as user scrolls
  - Scroll background fades in as user scrolls
  - WebP format support
  - Performance optimized with lazy loading

- **Maintained EventBackground component** for legacy support
- **Updated background rendering logic**:
  - Checks for dual-layer backgrounds first
  - Falls back to legacy single background
  - Falls back to deity background if no event background

**Performance Features:**
- Progressive image loading (thumbnail first)
- Lazy loading for scroll background
- Eager loading for hero background
- Smooth opacity transitions
- Mobile-responsive image selection
- Blur effect during loading

### 5. Event-Specific Rules Enforcement

**Automatic Rule Enforcement:**
1. **Engagement**: Requires lord at top, rings/flowers on scroll
2. **Marriage**: Same temple+lord for both layers (full coverage)
3. **Reception**: Royal backgrounds, lord optional
4. **Haldi**: NO lord allowed - yellow themes only
5. **Mehendi**: NO lord allowed - green themes only

**Admin UI Enforcement:**
- Lord selector automatically disabled for Haldi/Mehendi
- Visual indicators showing rule restrictions
- Helpful tooltips explaining restrictions

## File Structure

```
/app/backend/
  models.py                 # Updated EventBackgroundConfig model

/app/frontend/src/
  config/
    eventBackgroundConfig.js   # NEW: Event background configuration
  pages/
    ProfileForm.jsx            # Updated: Enhanced background selector
    PublicInvitation.jsx       # Updated: Dual-layer background rendering
  
/app/frontend/public/assets/
  backgrounds/               # Directory for background images
    engagement_*.webp
    haldi_*.webp
    mehendi_*.webp
    marriage_*.webp (uses deity images)
    reception_*.webp
```

## Image Requirements

All background images should be in **WebP format** with three sizes:
- `*_thumb.webp` - Thumbnail (200x113px) for quick loading
- `*_mobile.webp` - Mobile (800x450px) for mobile devices
- `*_desktop.webp` - Desktop (1920x1080px) for desktop devices

### Required Image Files

**Engagement (5 ring/flower options):**
- engagement_rings_gold_*.webp
- engagement_rings_diamond_*.webp
- engagement_flowers_pink_*.webp
- engagement_flowers_white_*.webp
- engagement_flowers_mixed_*.webp

**Haldi (4 yellow options):**
- haldi_turmeric_*.webp
- haldi_bindelu_*.webp
- haldi_yellow_florals_*.webp
- haldi_yellow_abstract_*.webp

**Mehendi (4 green options):**
- mehendi_pattern_intricate_*.webp
- mehendi_green_leaves_*.webp
- mehendi_paisley_*.webp
- mehendi_green_abstract_*.webp

**Reception (4 royal options):**
- reception_royal_gold_*.webp
- reception_royal_purple_*.webp
- reception_classy_silver_*.webp
- reception_classy_champagne_*.webp

**Marriage:** Uses existing deity images from `/app/frontend/public/assets/deities/`

## Key Features Implemented

✅ Dual-layer background system (hero + scroll)
✅ Event-specific background rules
✅ Auto-enforcement of lord background restrictions
✅ Progressive image loading (thumbnail → full)
✅ Scroll-based opacity transitions
✅ WebP format for performance
✅ Lazy loading for scroll backgrounds
✅ Mobile-responsive image selection
✅ Backward compatibility with legacy backgrounds
✅ Clean, non-duplicate layouts
✅ No hardcoded images (all from configuration)
✅ Performance-safe implementation

## Testing Checklist

### Admin Panel Testing
- [ ] Create/edit event with each event type
- [ ] Verify Haldi shows only yellow backgrounds (no lord option)
- [ ] Verify Mehendi shows only green backgrounds (no lord option)
- [ ] Verify Engagement shows lord options for hero, rings/flowers for scroll
- [ ] Verify Marriage shows lord options for both layers
- [ ] Verify Reception shows royal backgrounds with optional lord for scroll
- [ ] Verify background selection saves correctly
- [ ] Verify UI displays selected backgrounds with check marks

### Public Invitation Testing
- [ ] View engagement invitation - lord at top, rings/flowers on scroll
- [ ] View marriage invitation - temple+lord full coverage
- [ ] View reception invitation - royal background displays correctly
- [ ] View haldi invitation - yellow background displays, no lord
- [ ] View mehendi invitation - green background displays, no lord
- [ ] Test scroll behavior - hero fades out, scroll fades in
- [ ] Test on mobile devices - correct image sizes load
- [ ] Test progressive loading - thumbnail → full image
- [ ] Verify legacy events still work with old background format

### Performance Testing
- [ ] Verify images load progressively (thumbnail first)
- [ ] Verify scroll backgrounds lazy load
- [ ] Verify no layout shift during image loading
- [ ] Verify smooth scroll transitions
- [ ] Test on slow network connection

## Notes

1. **Image Assets**: Actual background images need to be added to `/app/frontend/public/assets/backgrounds/` directory. Currently using placeholder paths.

2. **Backward Compatibility**: System maintains support for legacy single-background events via the `EventBackground` component.

3. **Performance**: Implemented multiple optimizations:
   - Progressive loading (thumbnail first)
   - Lazy loading for scroll backgrounds
   - WebP format (smaller file sizes)
   - Scroll-based opacity (smooth transitions)

4. **No Duplicate Layouts**: All backgrounds are rendered using the same fixed positioning strategy, avoiding layout duplication.

5. **No Hardcoded Images**: All image paths come from the configuration file, making it easy to update or add new backgrounds.

## Future Enhancements

1. Add image upload functionality for custom backgrounds
2. Implement background preview in admin panel
3. Add background image optimization/compression
4. Support for animated backgrounds (with performance guards)
5. Background color overlay controls
6. Parallax scrolling effects (optional)

## Status

✅ Backend models updated
✅ Frontend configuration created
✅ Admin UI implemented with rule enforcement
✅ Public invitation dual-layer rendering implemented
✅ Progressive loading and lazy loading implemented
✅ Services restarted successfully
⏳ Background image assets need to be added

**Implementation Complete - Ready for Testing**
