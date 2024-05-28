# Отдача статического документа напрямую через nginx

    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 100 requests
    Completed 200 requests
    Completed 300 requests
    Completed 400 requests
    Completed 500 requests
    Completed 600 requests
    Completed 700 requests
    Completed 800 requests
    Completed 900 requests
    Completed 1000 requests
    Finished 1000 requests


    Server Software:        nginx/1.26.0
    Server Hostname:        127.0.0.1
    Server Port:            80

    Document Path:          /static/images/default_avatar.jpg
    Document Length:        88006 bytes

    Concurrency Level:      1
    Time taken for tests:   0.049 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      88335000 bytes
    HTML transferred:       88006000 bytes
    Requests per second:    20377.80 [#/sec] (mean)
    Time per request:       0.049 [ms] (mean)
    Time per request:       0.049 [ms] (mean, across all concurrent requests)
    Transfer rate:          1757884.14 [Kbytes/sec] received

    Connection Times (ms)
                min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     0    0   0.0      0       0
    Waiting:        0    0   0.0      0       0
    Total:          0    0   0.0      0       0

    Percentage of the requests served within a certain time (ms)
    50%      0
    66%      0
    75%      0
    80%      0
    90%      0
    95%      0
    98%      0
    99%      0
    100%      0 (longest request)


# Отдача статического документа напрямую через gunicorn

    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 100 requests
    Completed 200 requests

    ~ 
    ❯ ab -n 1000 http://127.0.0.1:8000/static/images/default_avatar.jpg
    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 100 requests
    Completed 200 requests
    Completed 300 requests
    Completed 400 requests
    Completed 500 requests
    Completed 600 requests
    Completed 700 requests
    Completed 800 requests
    Completed 900 requests
    Completed 1000 requests
    Finished 1000 requests


    Server Software:        gunicorn
    Server Hostname:        127.0.0.1
    Server Port:            8000

    Document Path:          /static/images/default_avatar.jpg
    Document Length:        88006 bytes

    Concurrency Level:      1
    Time taken for tests:   0.471 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      88381000 bytes
    HTML transferred:       88006000 bytes
    Requests per second:    2124.84 [#/sec] (mean)
    Time per request:       0.471 [ms] (mean)
    Time per request:       0.471 [ms] (mean, across all concurrent requests)
    Transfer rate:          183393.90 [Kbytes/sec] received

    Connection Times (ms)
                min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     0    0   0.1      0       3
    Waiting:        0    0   0.1      0       1
    Total:          0    0   0.1      0       3

    Percentage of the requests served within a certain time (ms)
    50%      0
    66%      0
    75%      0
    80%      0
    90%      1
    95%      1
    98%      1
    99%      1
    100%      3 (longest request)