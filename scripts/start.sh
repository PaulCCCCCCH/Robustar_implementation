# Start NGINX server for frontend
service nginx restart

# Start backend server
cd back-end

# nohup nginx -g "daemon off;" & gunicorn -b 0.0.0.0:8000 --workers=2 "server:create_app()" "$1" 
python3.9 server.py