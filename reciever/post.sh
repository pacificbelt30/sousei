#curl -X POST -H "Content-Type: application/json" -d '{"kamoku":"M1", "kaisu":3, "csv":"S002,遅刻\nS022,遅刻\nS007,遅刻"}' http://localhost/csv/
#curl -X POST -H "Content-Type: application/json" -d '{"kamoku":"M1", "kaisu":3, "csv":"S002,遅刻\nS022,遅刻\nS007,遅刻"}' http://localhost:5000/csv/
#curl -X POST -d 'csv=10,20,40&kamoku=F1' http://localhost/edit/
curl -X POST -d 'id=P001&password=df1e40051eff4bcf9b4ebc93083bfcad7f5195746b3e657de6b72bf3cb8897c3' http://localhost/auth/
