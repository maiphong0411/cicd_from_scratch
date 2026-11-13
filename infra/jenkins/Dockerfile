FROM jenkins/jenkins:lts-jdk21
# shortcut: Jenkins runs as root so it can use the host docker socket, fine on a laptop; use build agents when this is shared
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-coverage unzip \
 && rm -rf /var/lib/apt/lists/*
# the tools the pipeline shells out to (amd64 builds)
RUN curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-27.5.1.tgz | tar -xz -C /usr/local/bin --strip-components=1 docker/docker \
 && curl -fsSL https://get.helm.sh/helm-v4.3.2-linux-amd64.tar.gz | tar -xz -C /usr/local/bin --strip-components=1 linux-amd64/helm \
 && curl -fsSL -o /tmp/scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-8.4.0.16527.zip \
 && unzip -q /tmp/scanner.zip -d /opt && rm /tmp/scanner.zip \
 && ln -s /opt/sonar-scanner-8.4.0.16527/bin/sonar-scanner /usr/local/bin/sonar-scanner \
 && git config --system --add safe.directory '*'
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt
