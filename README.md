## hbase install

1. download & unzip
    - wget ~
    - tar ~

2. .bashrc에 경로 설정
    - source .bashrc 와 echo 명령어로 환경설정 올바르게 되었는지 확인

3. $HBASE_HOME > conf > hbase-site.xml에 property추가

4. 서버 실행 및 web ui 접근
    - $HBASE_HOME/bin/start-hbase.sh
    - localhost:16010
        -  hadoop 실행중이여야 hbase도 실행됨
            - 하둡 실행 명령어: $HADOOP_HOME/sbin/start-all.sh > localhost:9870 접속하여 실행 여부 확인



 ## shell 실행 및 쿼리

1.shell 실행 (종료: ctrl+z)
   - $HBASE_HOME/bin/hbase shell

2. create table
```
create 'students', 'info'
```
3. list
- 테이블 조회
4. create
```
put 'students', '1', 'info:name', 'kim'
put 'students', '1', 'info:age', '10'
put 'students', '1', 'info:gender', 'M'

put 'students', '2', 'info:name', 'hong'
put 'students', '2', 'info:age', '20'
put 'students', '2', 'info:gender', 'F'
```
5. scan '테이블명'
- 해당 테이블에 있는 데이터를 출력

6. get
```
get 'students', '1' # <- id? value?
```
7. update
```
`put` 'students', '1', 'info:age', '100'
```
8. delete
```
`delete` 'students', '1', 'info:locaion'
```
9. delete all
```
deleteall 'students', '2'
```
10. drop table
```
disable 'students'
drop 'students'
```


## localhost:8000 docs 접속

- 설치
    - pip3 install fastapi
    - pip3 install uvicorn
    - pip3 install happybase

- main.py 형태

```
from fastapi import FastAPI

app = FastAPI() #fastapi = django와 같이 기능함

@app.get("/") # urls.py와 같이 기능
def read_root(): #views.py와 같이 기능
    return {"Hello": "World"} #context 넣어서 return하는 것과 같이 기능
```

- thrift start
```
$HBASE_HOME/bin/hbase thrift start
```

- run server
```
uvicorn main:app --reload
```