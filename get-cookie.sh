curl -c dokemon-cookie.txt -X POST http://192.168.1.2:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"userName": "admin", "password": "vyrenaball"}'
curl -b dokemon-cookie.txt http://192.168.1.2:9090/api/v1/nodes/1

