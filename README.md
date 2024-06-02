
Auction Platform API
This project is a RESTful API built using Django Rest Framework (DRF) for managing various product auctions. It includes features such as registration/login functionality,
real-time bidding using WebSockets, and email notifications for auction winners. The platform utilizes Django Channels for WebSocket functionality, Docker for containerization,
JWT authentication for user authentication, and PostgreSQL as the database. Additionally, an external email service is used for sending email notifications.

Features
User Authentication: Users can register and log in to the platform using JWT authentication.
Product Auctions: Administrators can add new products and open auctions for them. Each auction has a predetermined time, minimum bid, and timer.
Real-time Bidding: Logged-in users can bid on auctions in real-time using WebSockets. The bidding system includes a timer that resets when a new bid is placed within 1 minute.
Email Notifications: When an auction ends, the winner is sent an email notification containing details about the winning product.

Endpoints:
User Management:
POST /api/users/: Register a new user.
GET /api/users/: Retrieve a list of users.

Authentication:
POST /api/token/: Obtain JWT token for authentication.
POST /api/token/refresh/: Refresh JWT token.

Product Management:
GET /products/: Retrieve a list of products and create a new product.
GET /products/<int:pk>/: Retrieve, update, or delete a specific product.

Bidding:
POST /products/<int:product_id>/bids/: Place a bid on a specific product.

Technologies Used:
Django Rest Framework (DRF)
Django Channels
Docker
PostgreSQL
JWT Authentication
External Email Service

Setup Instructions:

Clone the repository:

git clone 
https://github.com/Jekmen1/Auction_Platform_Api.git

Navigate to the project directory:
cd Auction_Platform_API

Set up Docker and Docker Compose.
Create a .env file based on the provided .env.example file and fill in the necessary environment variables.

Build and run the Docker containers:
docker-compose up --build

Access the API at http://localhost:8000/.
