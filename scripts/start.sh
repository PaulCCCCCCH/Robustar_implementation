# Start NGINX server for frontend
service nginx restart

# Start backend server
cd back-end
python3.9 server.py