# Project Directory Structure

```plaintext
project_root/
│
├── main.py                 # Main script to generate reports
├── data.json               # JSON file containing all municipality data
├── gemeentegrenzen2.json   # GeoJSON file with municipality boundaries
│
├── data_processors.py      # Contains functions for processing data
├── graph_generators.py     # Contains functions for generating graphs
├── utils.py                # Contains utility functions like color generation
│
├── templates/
│   ├── base.html           # Base HTML template
│   └── rapport_template.html  # Specific template for municipality reports
│
├── static/
│   ├── css/
│   │   └── styles.css      # Main CSS file for styling
│   │
│   └── js/
│       ├── map.js          # JavaScript for handling map functionality
│       ├── scroll-effects.js  # JavaScript for scroll effects
│       └── animations.js   # JavaScript for animations
│
└── output/                 # Directory where generated reports are saved
    ├── report_[Municipality].html  # Generated HTML reports
    └── static/             # Copied static files for the reports
        ├── css/
        │   └── styles.css
        └── js/
            ├── map.js
            ├── scroll-effects.js
            └── animations.js
