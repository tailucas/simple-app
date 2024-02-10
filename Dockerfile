FROM tailucas/base-app:20240210
# for system/site packages
USER root
# generate correct locales
ARG LANG
ENV LANG=$LANG
ARG LANGUAGE
ENV LANGUAGE=$LANGUAGE
ARG LC_ALL
ENV LC_ALL=$LC_ALL
ARG ENCODING
ENV ENCODING=$ENCODING
RUN localedef -i ${LANGUAGE} -c -f ${ENCODING} -A /usr/share/locale/locale.alias ${LANG}
# system setup
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        html-xml-utils
# user scripts
COPY simplejob.sh .
# cron jobs
RUN rm -f ./config/cron/simplejob
COPY config/cron/simplejob ./config/cron/
# apply override
RUN /opt/app/app_setup.sh
# application
COPY ./target/*-jar-with-dependencies.jar ./app.jar
# switch to user
USER app
# override configuration
COPY config/app.conf ./config/app.conf
COPY poetry.lock pyproject.toml ./
RUN /opt/app/python_setup.sh
# add the project application
COPY app/ ./app/
# override entrypoint
COPY app_entrypoint.sh .
CMD ["/opt/app/entrypoint.sh"]
