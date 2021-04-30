FROM centos:latest

EXPOSE 80 443

RUN yum install python3 python3-mod_wsgi git mesa-libGL.x86_64 mod_ssl httpd -y &&  useradd -ms /bin/bash prathamesh && rm -rf /etc/httpd/conf.d/ssl.conf && yum clean all

USER prathamesh
WORKDIR /home/prathamesh

RUN git clone https://github.com/gitwit-mistry/Fire-Smoke-Detection-WebApp.git

WORKDIR Fire-Smoke-Detection-WebApp

RUN python3 -m venv env2 3.6 && source env2/bin/activate && pip3 install --upgrade pip && pip3 install --upgrade setuptools && pip3 install -r requirements.txt --no-cache-dir
USER root

COPY config.json /etc/config.json
COPY server_files/ssl_domain-name.com.conf /etc/httpd/conf.d/ssl_domain-name.com.conf
COPY server_files/server_ssl_key.pem /etc/pki/tls/private/server_ssl_key.pem
COPY server_files/full-chain.pem /etc/pki/tls/certs/full-chain.pem
COPY server_files/domain-name.com.conf /etc/httpd/conf.d/domain-name.com.conf

RUN chown -R :apache /home/prathamesh && chmod -R 775 /home/prathamesh

CMD ["/bin/bash"]
