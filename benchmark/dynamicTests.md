# Отдача динамического документа напрямую через gunicorn

    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient).....done


    Server Software:        gunicorn
    Server Hostname:        127.0.0.1
    Server Port:            8000

    Document Path:          /
    Document Length:        104753 bytes

    Concurrency Level:      1
    Time taken for tests:   5.264 seconds
    Complete requests:      100
    Failed requests:        0
    Total transferred:      10505100 bytes
    HTML transferred:       10475300 bytes
    Requests per second:    19.00 [#/sec] (mean)
    Time per request:       52.641 [ms] (mean)
    Time per request:       52.641 [ms] (mean, across all concurrent requests)
    Transfer rate:          1948.83 [Kbytes/sec] received

    Connection Times (ms)
                min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:    47   53   6.3     52      83
    Waiting:       47   52   6.3     51      83
    Total:         47   53   6.3     52      83

    Percentage of the requests served within a certain time (ms)
    50%     52
    66%     53
    75%     54
    80%     55
    90%     58
    95%     64
    98%     82
    99%     83
    100%     83 (longest request)


# Отдача динамического документа через проксирование запроса с nginx на gunicorn

    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient).....done


    Server Software:        nginx/1.26.0
    Server Hostname:        127.0.0.1
    Server Port:            80

    Document Path:          /
    Document Length:        104753 bytes

    Concurrency Level:      1
    Time taken for tests:   5.308 seconds
    Complete requests:      100
    Failed requests:        0
    Total transferred:      10505500 bytes
    HTML transferred:       10475300 bytes
    Requests per second:    18.84 [#/sec] (mean)
    Time per request:       53.078 [ms] (mean)
    Time per request:       53.078 [ms] (mean, across all concurrent requests)
    Transfer rate:          1932.85 [Kbytes/sec] received

    Connection Times (ms)
                min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:    47   53   3.5     53      64
    Waiting:       47   53   3.4     53      64
    Total:         47   53   3.5     53      64

    Percentage of the requests served within a certain time (ms)
    50%     53
    66%     55
    75%     56
    80%     56
    90%     57
    95%     58
    98%     59
    99%     64
    100%     64 (longest request)


# Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэширование ответа на nginx (proxy cache)

    This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient).....done


    Server Software:        nginx/1.26.0
    Server Hostname:        127.0.0.1
    Server Port:            80

    Document Path:          /
    Document Length:        104753 bytes

    Concurrency Level:      1
    Time taken for tests:   0.089 seconds
    Complete requests:      100
    Failed requests:        0
    Total transferred:      10505500 bytes
    HTML transferred:       10475300 bytes
    Requests per second:    1118.29 [#/sec] (mean)
    Time per request:       0.894 [ms] (mean)
    Time per request:       0.894 [ms] (mean, across all concurrent requests)
    Transfer rate:          114728.78 [Kbytes/sec] received

    Connection Times (ms)
                min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     0    1   8.4      0      84
    Waiting:        0    1   8.4      0      84
    Total:          0    1   8.4      0      84

    Percentage of the requests served within a certain time (ms)
    50%      0
    66%      0
    75%      0
    80%      0
    90%      0
    95%      0
    98%      0
    99%     84
    100%     84 (longest request)
