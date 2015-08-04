# haproxy-marathon

[![Join the chat at https://gitter.im/mesoscloud/haproxy-marathon](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/mesoscloud/haproxy-marathon?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Generate HAProxy configuration (using Marathon as a data source)

See https://github.com/mesoscloud/haproxy

## Ubuntu

[![](https://badge.imagelayers.io/mesoscloud/haproxy-marathon:0.1.0-ubuntu-14.04.svg)](https://imagelayers.io/?images=mesoscloud/haproxy-marathon:0.1.0-ubuntu-14.04)

e.g.

```
docker run -d
-e MARATHON=node-1:8080
-e ZK=node-1:2181
--name=haproxy --net=host --restart=always mesoscloud/haproxy-marathon:0.1.0-ubuntu-14.04
```
