# Docker搭建Jellyfin

来源：https://docs.linuxserver.io/images/docker-jellyfin#environment-variables-e
```dockerfile
docker run -d \
  --name=jellyfin \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Aisa/Shanghai \
  -p 8096:8096 \
  -p 8920:8920 `#optional` \
  -p 7359:7359/udp `#optional` \
  -p 1900:1900/udp `#optional` \
  -v /userdatas/Sandisk/Jellyfin/config:/config \
  -v /userdatas/Sandisk/Jellyfin/tvseries:/data/tvshows `#optional` \ 
  -v /userdatas/Sandisk/Jellyfin/movies:/data/movies `#optional` \
  --restart unless-stopped \
  ghcr.io/linuxserver/jellyfin
```
