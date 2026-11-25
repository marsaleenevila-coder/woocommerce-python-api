# Norevia WooCommerce Python API

A Python-based integration project that connects to WooCommerce using its REST API and Store API. Built with HTTPX, OAuth 1.0 authentication, and Python, this project demonstrates product management, order management, customer operations, shopping cart functionality, and checkout integration.

## Features

### WooCommerce REST API Integration

- Connect to the WooCommerce REST API (`wc/v3`).
- Authenticate using OAuth 1.0 HMAC-SHA1.
- Load API credentials securely from environment variables.
- Retrieve published products with pagination.
- Search products by name and SKU.
- Retrieve orders with pagination.
- Retrieve individual orders by ID.
- Filter orders by status.
- Retrieve customer information.
- Search customers by email.
- Create, update, and delete customers.
- Retrieve store configuration, currency, country, and enabled payment gateways.

### WooCommerce Store API Integration

- Connect to the WooCommerce Store API (`wc/store/v1`).
- Retrieve shopping cart information.
- Add products to the cart.
- Update cart item quantities.
- Remove cart items.
- Apply discount coupons.
- Retrieve checkout information.
- Update billing and shipping addresses.
- Retrieve and select available payment methods.
- Validate checkout information.
- Submit checkout and create WooCommerce orders.
- Maintain cart tokens and nonces during API requests.

**Important:** Submitting checkout creates an actual WooCommerce order. Use a test environment when experimenting with checkout and payment functionality.

### Error Handling

- Connection errors.
- Request timeouts.
- Authentication failures.
- API permission errors.
- HTTP errors.
- Invalid JSON responses.
- Invalid API response structures.

### Automated Testing

- Pytest-based automated tests.
- Mocked HTTP requests.
- OAuth signing verification.
- Product pagination tests.
- Product search validation.
- API error-handling tests.

## Technologies

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| Python                | Application development             |
| HTTPX                 | HTTP requests and API communication |
| WooCommerce REST API  | Store management                    |
| WooCommerce Store API | Cart and checkout                   |
| OAuthLib              | OAuth 1.0 authentication            |
| python-dotenv         | Environment configuration           |
| pytest                | Automated testing                   |

## Project Structure

```text
woocommerce-API/
│
├── api_client.py           # WooCommerce REST API client
├── store_api_client.py     # WooCommerce Store API client
│
├── config.py               # Environment configuration
│
├── products.py             # Product retrieval and search
├── orders.py               # Order retrieval and filtering
├── customers.py            # Customer management
├── store_config.py         # Store configuration
│
├── cart.py                 # Shopping cart operations
├── checkout.py             # Checkout and order submission
│
├── create_test_order.py    # Test order utility
├── main.py                 # Terminal application entry point
│
├── tests/
│   ├── test_api_client.py  # API client tests
│   └── test_products.py    # Product operation tests
│
├── postman/                # Postman workspace files
│
├── .env                    # Local environment variables
├── .env.example            # Example environment configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or later.
- WordPress website with WooCommerce installed.
- WooCommerce REST API credentials.
- WooCommerce Store API enabled.
- Git.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/marsaleenevila-coder/woocommerce-python-api.git

cd woocommerce-python-api
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root using `.env.example` as a template.

```env
WC_STORE_URL=http://localhost:8080
WC_CONSUMER_KEY=your_consumer_key
WC_CONSUMER_SECRET=your_consumer_secret
WC_API_VERSION=wc/v3
WC_TIMEOUT=30
```

Replace the example values with your WooCommerce store URL and API credentials.

### WooCommerce API Credentials

Generate REST API credentials from:

**WordPress Admin → WooCommerce → Settings → Advanced → REST API**

Choose the appropriate permissions:

- Read: retrieve store information.
- Read/Write: retrieve and modify store information, including customer management.

The Store API uses its own cart token and nonce mechanism for cart and checkout requests.

### Security

- Never commit your `.env` file.
- Never expose your consumer secret.
- Keep API credentials out of source code.
- Use appropriate API key permissions.
- Use a test store for checkout and order-creation experiments.

## Run the Application

Start the terminal application:

```powershell
python main.py
```

The application connects to WooCommerce and displays an interactive menu.

### Available Terminal Operations

| Option | Operation                    |
| ------ | ---------------------------- |
| 1      | Retrieve products            |
| 2      | Retrieve all orders          |
| 3      | Retrieve order by ID         |
| 4      | Search orders by status      |
| 5      | Retrieve all customers       |
| 6      | Retrieve customer by ID      |
| 7      | Search customers by email    |
| 8      | Retrieve store configuration |
| 9      | Exit                         |

## API Endpoints

### WooCommerce REST API

Base endpoint:

```text
/wp-json/wc/v3/
```

Examples:

| Operation        | Endpoint                          |
| ---------------- | --------------------------------- |
| Products         | `/wp-json/wc/v3/products`         |
| Orders           | `/wp-json/wc/v3/orders`           |
| Customers        | `/wp-json/wc/v3/customers`        |
| General Settings | `/wp-json/wc/v3/settings/general` |
| Payment Gateways | `/wp-json/wc/v3/payment_gateways` |

### WooCommerce Store API

Base endpoint:

```text
/wp-json/wc/store/v1/
```

Examples:

| Operation        | Endpoint                                 |
| ---------------- | ---------------------------------------- |
| Cart             | `/wp-json/wc/store/v1/cart`              |
| Add Cart Item    | `/wp-json/wc/store/v1/cart/add-item`     |
| Update Cart Item | `/wp-json/wc/store/v1/cart/update-item`  |
| Remove Cart Item | `/wp-json/wc/store/v1/cart/remove-item`  |
| Apply Coupon     | `/wp-json/wc/store/v1/cart/apply-coupon` |
| Checkout         | `/wp-json/wc/store/v1/checkout`          |

## Automated Testing

The project uses pytest to test API client and product functionality without making live WooCommerce requests.

Run all automated tests:

```powershell
python -m pytest -v
```

Run API client tests:

```powershell
python -m pytest tests/test_api_client.py -v
```

Run product tests:

```powershell
python -m pytest tests/test_products.py -v
```

### Current Test Results

| Test Module        |  Tests |
| ------------------ | -----: |
| API Client         |      9 |
| Product Operations |      8 |
| **Total**          | **17** |

All 17 automated tests have passed.

## Current Project Status

- [x] WooCommerce REST API connection
- [x] OAuth 1.0 HMAC-SHA1 authentication
- [x] Environment-based configuration
- [x] Product retrieval and pagination
- [x] Product search by name
- [x] Product search by SKU
- [x] API error handling
- [x] Order retrieval and pagination
- [x] Order lookup by ID
- [x] Order filtering by status
- [x] Customer retrieval
- [x] Customer search by email
- [x] Customer creation, updating, and deletion
- [x] Store configuration retrieval
- [x] WooCommerce Store API integration
- [x] Shopping cart operations
- [x] Checkout functionality
- [x] Automated API and product tests

## Future Improvements

- Expand automated tests for orders and customers.
- Add automated tests for cart and checkout operations.
- Expand Postman collections and environment configuration.
- Improve application logging and reporting.
- Add additional input validation.
- Expand terminal menu functionality for product search and cart operations.

## License

This project is intended for learning, development, and WooCommerce API integration practice.
