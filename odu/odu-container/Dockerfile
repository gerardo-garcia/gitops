#######################################################################################
# Copyright ETSI Contributors and Others.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#######################################################################################
# FROM alpine:latest
FROM alpine:3.19.1
RUN apk -u add \
    bash \
    git \
    kustomize \
    openssh-client \
    sshpass

# RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
RUN addgroup -g 10000 -S app && \
    adduser -h /app -s /bin/false -D -u 10000 -S -G app app

USER app
WORKDIR /app

COPY --chown=app:app scripts /app/scripts
# cloud-native-osm/osm-gitops-operations/scripts/library/helper-functions.rc
# cloud-native-osm/osm-gitops-operations/scripts/library/krm-functions.rc

ENV GIT_REPO ""
ENV GIT_USER ""
ENV GIT_PASSWORD ""
ENV GIT_SSHKEY ""

CMD ["/app/scripts/source.sh"]

