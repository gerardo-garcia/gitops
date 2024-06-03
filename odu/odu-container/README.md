# ODU container

## Build and test docker images

```bash
docker build -t osm-odu:latest .
source test-environment.rc
docker run --env GIT_REPO="${GIT_REPO}" --env GIT_SSHKEY="${GIT_SSHKEY}" --env GIT_MANIFEST_FOLDER="${GIT_MANIFEST_FOLDER}" -it osm-odu:latest
```

```bash
docker build -t osm-odu:latest .
docker tag osm-odu:latest gerardogarcia/osm-odu:latest
docker push gerardogarcia/osm-odu:latest
```
