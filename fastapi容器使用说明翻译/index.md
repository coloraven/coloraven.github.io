# FastAPI容器使用说明翻译

官方说明：https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/blob/master/README.md
## 环境变量
有多个环境变量可供设置，如果不指定，则会使用默认值。
### `MODULE_NAME`——指定要运行的主文件文件名（Python中也叫模块名）

Python "module" (文件) Gunicorn, this module would contain the actual application in a variable.

默认为:

* `app.main`——如果主文件路径为 `/app/app/main.py`
或者
* `main`——如果主文件路径为 `/app/main.py`

打个比方, 如果主文件路径为 `/app/custom_app/custom_main.py`, 那么你需要设置成这样:

```bash
docker run -d -p 80:80 -e MODULE_NAME="custom_app.custom_main" myimage
```

### `VARIABLE_NAME`——指定主文件中`FastAPI()`对象的变量名称

默认是:

* `app`

举个例子, 如果你的主文件是这样的:
```Python
from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def read_root():
    return {"message": "Hello world!"}
```

在上面的例子中,`FastAPI()`对象的变量名为`api` ，那么你需要这样设置:

```bash
docker run -d -p 80:80 -e VARIABLE_NAME="api" myimage
```

### `APP_MODULE`——这个环境变量可以直接实现上面两个环境变量的作用
```bash
docker run -d -p 80:80 -e APP_MODULE="custom_app.custom_main:api" myimage
```

### `GUNICORN_CONF`——指定GUNICORN配置文件路径

默认为:

* `/app/gunicorn_conf.py` 如果在该路径存在则使用此处的
* `/app/app/gunicorn_conf.py` 如果在该路径存在则使用此处的
* `/gunicorn_conf.py` (容器作者在此处放入了默认配置文件)

你可以这样设置:

```bash
docker run -d -p 80:80 -e GUNICORN_CONF="/app/custom_gunicorn_conf.py" myimage
```

You can use the [config file](https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/gunicorn_conf.py) from this image as a starting point for yours.

### `WORKERS_PER_CORE`——指定每个CPU核心的线程数

This image will check how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

默认为:

* `1`

你可以这样设置:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="3" myimage
```

If you used the value `3` in a server with 2 CPU cores, it would run 6 worker processes.

You can use floating point values too.

So, for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have an ASGI application that you know won't need high performance. And you don't want to waste server resources. You could make it use `0.5` workers per CPU core. For example:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="0.5" myimage
```

In a server with 8 CPU cores, this would make it start only 4 worker processes.

**Note**: 默认为, if `WORKERS_PER_CORE` is `1` and the server has only 1 CPU core, instead of starting 1 single worker, it will start 2. This is to avoid bad performance and blocking applications (server application) on small machines (server machine/cloud/etc). This can be overridden using `WEB_CONCURRENCY`.

### `MAX_WORKERS`

Set the maximum number of workers to use.

You can use it to let the image compute the number of workers automatically but making sure it's limited to a maximum.

This can be useful, for example, if each worker uses a database connection and your database has a maximum limit of open connections.

默认为 it's not set, meaning that it's unlimited.

你可以这样设置:

```bash
docker run -d -p 80:80 -e MAX_WORKERS="24" myimage
```

This would make the image start at most 24 workers, independent of how many CPU cores are available in the server.

### `WEB_CONCURRENCY`

Override the automatic definition of number of workers.

默认为:

* Set to the number of CPU cores in the current server multiplied by the environment variable `WORKERS_PER_CORE`. So, in a server with 2 cores, 默认为 it will be set to `2`.

你可以这样设置:

```bash
docker run -d -p 80:80 -e WEB_CONCURRENCY="2" myimage
```

This would make the image start 2 worker processes, independent of how many CPU cores are available in the server.

### `HOST`——指定监听地址，可限制请求地址

The "host" used by Gunicorn, the IP where Gunicorn will listen for requests.

It is the host inside of the container.

因此, 如果你设置成 `127.0.0.1`, 那么将只能在容器中访问`FastAPI`服务.

默认为:

* `0.0.0.0`

### `PORT` ——指定监听端口，貌似可以更改暴露端口，默认为`80`

The port the container should listen on.

If you are running your container in a restrictive environment that forces you to use some specific port (like `8080`) you can set it with this variable.

默认为:

* `80`

你可以这样设置:

```bash
docker run -d -p 80:8080 -e PORT="8080" myimage
```

### `BIND`——直接实现上面两个参数的效果

The actual host and port passed to Gunicorn.

默认为, set based on the variables `HOST` and `PORT`.

So, if you didn't change anything, it will be set 默认为 to:

* `0.0.0.0:80`

你可以这样设置:

```bash
docker run -d -p 80:8080 -e BIND="0.0.0.0:8080" myimage
```

### `LOG_LEVEL`——指定`Gunicorn`日志的级别

The log level for Gunicorn.

One of:

* `debug`
* `info`
* `warning`
* `error`
* `critical`

默认为`info`.

If you need to squeeze more performance sacrificing logging, set it to `warning`, for example:

你可以这样设置:

```bash
docker run -d -p 80:8080 -e LOG_LEVEL="warning" myimage
```

### `WORKER_CLASS`

The class to be used by Gunicorn for the workers.

默认为, set to `uvicorn.workers.UvicornWorker`.

The fact that it uses Uvicorn is what allows using ASGI applications like FastAPI and Starlette, and that is also what provides the maximum performance.

You probably shouldn't change it.

But if for some reason you need to use the alternative Uvicorn worker: `uvicorn.workers.UvicornH11Worker` you can set it with this environment variable.

你可以这样设置:

```bash
docker run -d -p 80:8080 -e WORKER_CLASS="uvicorn.workers.UvicornH11Worker" myimage
```

### `TIMEOUT`——超时时间，默认为`120`.

Workers silent for more than this many seconds are killed and restarted.

Read more about it in the [Gunicorn docs: timeout](https://docs.gunicorn.org/en/stable/settings.html#timeout).

Notice that Uvicorn and ASGI frameworks like FastAPI and Starlette are async, not sync. So it's probably safe to have higher timeouts than for sync workers.

你可以这样设置:

```bash
docker run -d -p 80:8080 -e TIMEOUT="20" myimage
```

### `KEEP_ALIVE`——保持连接时间，默认为`2`.

The number of seconds to wait for requests on a Keep-Alive connection.

Read more about it in the [Gunicorn docs: keepalive](https://docs.gunicorn.org/en/stable/settings.html#keepalive).

你可以这样设置:

```bash
docker run -d -p 80:8080 -e KEEP_ALIVE="20" myimage
```

### `GRACEFUL_TIMEOUT`

Timeout for graceful workers restart.

Read more about it in the [Gunicorn docs: graceful-timeout](https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout).

默认为, set to `120`.

你可以这样设置:

```bash
docker run -d -p 80:8080 -e GRACEFUL_TIMEOUT="20" myimage
```

### `ACCESS_LOG`——访问日志的记录方式和保存位置，默认为 `"-"`，输出到容器日志中。

如果你想禁用访问日志，将其设置为空值即可:

```bash
docker run -d -p 80:8080 -e ACCESS_LOG= myimage
```

### `ERROR_LOG`——错误日志，默认为 `"-"`，输出到容器日志中。

如果你想禁用错误日志，将其设置为空值即可:

```bash
docker run -d -p 80:8080 -e ERROR_LOG= myimage
```
