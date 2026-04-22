# Architectural Directives for Jules

1. **Aesthetic Protocol:** All frontend work must strictly utilize Tailwind CSS to achieve a "Liquid Glass" (Glassmorphism) design. Use semi-transparent panels, `backdrop-blur`, and a professional dark slate/civic blue color palette. Absolutely no chaotic, "cringe," or cyberpunk themes.
2. **Backend Protocol:** All backend logic must use Python and FastAPI. Strict type validation via Pydantic is mandatory for all endpoints.
3. **Security Protocol:** Assume all user input is malicious. Implement strict sanitization before passing data to any Google APIs.
4. **Constraint:** The final repository must remain under 10 MB. Rely on CDNs for static assets and fonts.
