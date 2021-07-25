#ab -n 1000 -c 50 http://localhost/kamoku/F1?kyoin=P011
#ab -n 1000 -c 50 http://localhost/kamoku/M1?kyoin=P011
#ab -n 100 -c 50 http://localhost/user?kyoin=P011
#ab -n 1000 -c 50 http://localhost:5000/kamoku/F1?kyoin=P011
#ab -n 1000 -c 10 http://localhost:5002/kamoku/F1?kyoin=P011
#ab -n 1000 -c 50 http://localhost:2000/kamoku/F1?kyoin=P011
#ab -n 1000 -c 60 http://localhost/bench/F1
ab -n 1000 -c 60 http://192.168.1.8:13431/bench/F1
#ab -n 1000 -c 60 http://localhost/
#ab -n 1000 -c 50 http://localhost/bench/F2

#loginpage
#ab -n 1000 -c 50 http://localhost/auth

#csv
#ab -n 1000 -c 50 http://localhost/csv?kamoku=F1
#ab -n 1000 -c 50 http://localhost:2000/csv?kamoku=F1
