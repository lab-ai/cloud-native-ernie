# Paddle Serving

``` bash
docker pull hub.baidubce.com/paddlepaddle/serving:latest
docker run -p 9292:9292 --name test -dit hub.baidubce.com/paddlepaddle/serving:latest
docker exec -it test bash
```

``` bash
pip install paddle-serving-client==0.3.2 
pip install paddle-serving-server==0.3.2 # CPU
```

simple example:

​	one terminal: 

``` bash
python -m paddle_serving_server.serve --model uci_housing_model --thread 10 --port 9292 --name uci
```

​	another terminal:

``` bash
curl -H "Content-Type:application/json" -X POST -d '{"feed":[{"x": [0.0137, -0.1136, 0.2553, -0.0692, 0.0582, -0.0727, -0.1583, -0.0584, 0.6283, 0.4919, 0.1856, 0.0795, -0.0332]}], "fetch":["price"]}' http://127.0.0.1:9292/uci/prediction
```

