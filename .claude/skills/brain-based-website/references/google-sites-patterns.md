# Google Sites Editing via Playwright — Pattern Reference

## Text Entry
- Use `pressSequentially` (slowly=true) to type text, NOT `fill()` which replaces all content
- After pressing Enter in a Title field, style auto-switches to "Normal text"
- Styles dropdown has TWO nested listboxes — always click `.nth(1)` for the inner one
- Style options: Normal text, Title, Heading, Subheading, Small text

## Inserting Content
- "Text box" menuitem in Insert panel adds a new section with a text box
- "Three column image and captions" layout adds 3 columns with image placeholder + 2 text fields each
- Content placeholder buttons open image picker (Upload, Select image, From Drive, Google Images, Photos)
- Image picker is inside a nested iframe at `docs.google.com/picker` — access via `page.frames().find(f => f.url().includes('picker'))`
- "Add Footer" button at bottom of article adds a footer section

## Clicking Issues & Workarounds
- Many elements have overlays that intercept clicks — use `{force: true}` with Playwright code
- After exiting preview, "Edit Page" menuitem overlay blocks clicks — click it first to re-enter edit mode
- For three-column layout text: `page.locator('p:text-is("Click to edit text"):visible').nth(0).click({force: true})`
- Theme cards: `page.locator('text=ThemeName').first().click({force: true})`

## Themes & Styling
- Themes: Simple, Aristotle, Diplomat, Vision, Level, Impression
- Each theme has color variants (radio buttons) and Font style options (Classic, Light, Heavy, etc.)
- **This project uses:** Diplomat theme, Dark Blue color, Light font style
- Section colors button: Style 1 (default), Style 2 (light tinted), Style 3 (dark accent), Image
- Alternate section backgrounds for visual rhythm

## Font Size
- Font size input: `page.locator('input[aria-label="Font size"]').last()`
- Triple-click to select, fill new value, press Enter

## Alignment
- Align dropdown is a listbox with options: Left, Center, Right, Justify
- Click the Align listbox `.nth(1)` then click the desired option

## Page Management
- Pages tab shows page tree with "New page" button
- "New page" button opens a submenu — click it twice (once to expand, once for "New page" option)
- New page dialog has Name textbox and Done button

## Preview
- Preview button opens preview in an iframe
- Preview has Phone/Tablet/Large screen tabs
- "Exit preview" button returns to editor
- Scrolling in preview: access the preview iframe via `page.frames().find(f => f.url().includes('preview'))`
