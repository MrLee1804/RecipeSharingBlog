# Recipe Sharing Blog

A modern web application for sharing and discovering recipes, built with Flask and Bootstrap.

## Features

- User authentication (login/register)
- View all recipes
- Add new recipes
- View recipe details
- Responsive design
- Modern UI with animations
- Image preview for recipes

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RecipeSharingBlog
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Default Admin Account

- Username: admin
- Password: admin123

## Project Structure

```
recipe-sharing-blog/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── css/
│   │   └── style.css  # Custom CSS styles
│   └── js/
│       └── main.js    # Custom JavaScript
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── recipe_detail.html
│   └── add_recipe.html
└── data/             # Data storage
    ├── recipes.csv   # Recipe data
    └── users.csv     # User data
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
