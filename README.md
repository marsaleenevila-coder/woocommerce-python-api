# \# Norevia WooCommerce Python API

# 

# A Python integration project that connects to a WooCommerce store using the WooCommerce REST API, HTTPX, and OAuth 1.0 authentication.

# 

# \## Features

# 

# \- Connect to WooCommerce REST API (`wc/v3`).

# \- Authenticate using OAuth 1.0 HMAC-SHA1.

# \- Load credentials securely from environment variables.

# \- Retrieve published products with pagination.

# \- Search published products by name.

# \- Search published products by SKU.

# \- Display product details, prices, SKU, stock quantity, and status.

# \- Handle connection errors, timeouts, authentication errors, and HTTP errors.

# 

# \## Technologies

# 

# \- Python

# \- HTTPX

# \- WooCommerce REST API

# \- OAuthLib

# \- python-dotenv

# 

# \## Project Structure

# 

# ```text

# woocommerce-API/

# │

# ├── api\_client.py       # HTTP client and OAuth authentication

# ├── config.py           # Environment configuration

# ├── products.py         # Product retrieval and search

# ├── orders.py           # Reserved for order functionality

# ├── main.py             # Application entry point

# │

# ├── postman/            # Postman workspace files

# │

# ├── .env.example        # Example environment configuration

# ├── .gitignore

# ├── requirements.txt

# └── README.md

# ```

# 

# \## Requirements

# 

# \- Python 3.10 or later

# \- A WordPress website with WooCommerce installed

# \- WooCommerce REST API credentials with read permissions

# 

# \## Installation

# 

# \### 1. Clone the repository

# 

# ```powershell

# git clone https://github.com/marsaleenevila-coder/woocommerce-python-api.git

# cd woocommerce-python-api

# ```

# 

# \### 2. Create a virtual environment

# 

# ```powershell

# python -m venv .venv

# ```

# 

# \### 3. Activate the virtual environment

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

# 

# \### 4. Install dependencies

# 

# ```powershell

# python -m pip install -r requirements.txt

# ```

# 

# \## Configuration

# 

# Create a `.env` file in the project root using `.env.example` as a template.

# 

# ```env

# WC\_STORE\_URL=http://localhost:8080

# WC\_CONSUMER\_KEY=your\_consumer\_key

# WC\_CONSUMER\_SECRET=your\_consumer\_secret

# WC\_API\_VERSION=wc/v3

# WC\_TIMEOUT=30

# ```

# 

# Replace the example credentials with your WooCommerce REST API credentials.

# 

# \*\*Security:\*\* Never commit your `.env` file or share your consumer secret. The `.gitignore` file excludes `.env` from Git.

# 

# \## Run the application

# 

# ```powershell

# python main.py

# ```

# 

# The application connects to WooCommerce, retrieves published products, and displays their details in the terminal.

# 

# \## Available product operations

# 

# The `products.py` module provides:

# 

# | Function | Description |

# |---|---|

# | `get\_products()` | Retrieves published products with pagination |

# | `display\_products()` | Displays product information |

# | `search\_products\_by\_name()` | Searches products by name |

# | `search\_products\_by\_sku()` | Searches products by SKU |

# 

# Example usage:

# 

# ```python

# from api\_client import WooCommerceClient

# from products import (

# &#x20;   get\_products,

# &#x20;   search\_products\_by\_name,

# &#x20;   search\_products\_by\_sku,

# )

# 

# client = WooCommerceClient()

# 

# \# Retrieve products

# products = get\_products(client)

# 

# \# Search by name

# results\_by\_name = search\_products\_by\_name(

# &#x20;   client,

# &#x20;   "Python Automation"

# )

# 

# \# Search by SKU

# results\_by\_sku = search\_products\_by\_sku(

# &#x20;   client,

# &#x20;   "PY-AUTO-001"

# )

# ```

# 

# \## API Endpoint

# 

# The project uses the WooCommerce REST API:

# 

# ```text

# /wp-json/wc/v3/

# ```

# 

# Example product endpoint:

# 

# ```text

# /wp-json/wc/v3/products

# ```

# 

# \## Current Project Status

# 

# \- \[x] WooCommerce API connection

# \- \[x] OAuth 1.0 authentication

# \- \[x] Environment-based configuration

# \- \[x] Product retrieval

# \- \[x] Product pagination

# \- \[x] Search by product name

# \- \[x] Search by SKU

# \- \[x] API error handling

# \- \[ ] Order retrieval

# \- \[ ] Order search and filtering

# \- \[ ] Automated API tests

# 

# \## Future Improvements

# 

# \- Implement WooCommerce order retrieval.

# \- Add order search and filtering.

# \- Add automated tests.

# \- Expand Postman API collections.

# \- Improve logging and reporting.

# 

# \## License

# 

# This project is intended for learning and WooCommerce API integration practice.

