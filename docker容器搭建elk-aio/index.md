# Docker容器搭建ELK AIO

## 镜像地址
https://hub.docker.com/r/sebp/elk
## 参数说明
`docker run -itd -p 5601:5601 -p 9200:9200 -p 5044:5044 --name=elk -e TZ="Asia/Shanghai" sebp/elk`



- `TZ`: 时区 (这里查看 [可用时区参数](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)), 例如 `Asia/Shanghai`、`America/Los_Angeles` (default is `Etc/UTC`, i.e. UTC).
    
- `ES_HEAP_SIZE`: Elasticsearch heap size，内存占用？ (default is 256MB min, 1G max)
    
    Specifying a heap size – e.g. `2g` – will set both the min and max to the provided value. To set the min and max values separately, see the `ES_JAVA_OPTS` below.
    
- `ES_JAVA_OPTS`: additional Java options for Elasticsearch (default: `""`)
    
    For instance, to set the min and max heap size to 512MB and 2G, set this environment variable to `-Xms512m -Xmx2g`.
    
- `ES_CONNECT_RETRY`: number of seconds to wait for Elasticsearch to be up before starting Logstash and/or Kibana (default: `30`)
    
- `ES_PROTOCOL`: protocol to use to ping Elasticsearch's JSON interface URL (default: `http`)
    
    Note that this variable is only used to test if Elasticsearch is up when starting up the services. It is not used to update Elasticsearch's URL in Logstash's and Kibana's configuration files.
    
- `CLUSTER_NAME`: the name of the Elasticsearch cluster (default: automatically resolved when the container starts if Elasticsearch requires no user authentication).
    
    The name of the Elasticsearch cluster is used to set the name of the Elasticsearch log file that the container displays when running. By default the name of the cluster is resolved automatically at start-up time (and populates `CLUSTER_NAME`) by querying Elasticsearch's REST API anonymously. However, when Elasticsearch requires user authentication (as is the case by default when running X-Pack for instance), this query fails and the container stops as it assumes that Elasticsearch is not running properly. Therefore, the `CLUSTER_NAME` environment variable can be used to specify the name of the cluster and bypass the (failing) automatic resolution.
    
- `LS_HEAP_SIZE`: Logstash heap size (default: `"500m"`)
    
- `LS_OPTS`: Logstash options (default: `"--auto-reload"` in images with tags `es231_l231_k450` and `es232_l232_k450`, `""` in `latest`; see [Breaking changes](https://elk-docker.readthedocs.io/#breaking-changes))
    
- `NODE_OPTIONS`: Node options for Kibana (default: `"--max-old-space-size=250"`)
    
- `MAX_MAP_COUNT`: limit on mmap counts (default: system default)
    
    **Warning** – This setting is system-dependent: not all systems allow this limit to be set from within the container, you may need to set this from the host before starting the container (see [Prerequisites](https://elk-docker.readthedocs.io/#prerequisites)).
    
- `MAX_OPEN_FILES`: maximum number of open files (default: system default; Elasticsearch needs this amount to be equal to at least 65536)
    
- `KIBANA_CONNECT_RETRY`: number of seconds to wait for Kibana to be up before running the post-hook script (see [Pre-hooks and post-hooks](https://elk-docker.readthedocs.io/#pre-post-hooks)) (default: `30`)
    
- `ES_HEAP_DISABLE` and `LS_HEAP_DISABLE`: disable `HeapDumpOnOutOfMemoryError` for Elasticsearch and Logstash respectively if non-zero (default: `HeapDumpOnOutOfMemoryError` is enabled).
    
    Setting these environment variables avoids potentially large heap dumps if the services run out of memory.


## 镜像使用手册文档
https://elk-docker.readthedocs.io
