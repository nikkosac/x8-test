#使用官方发布的镜像
 FROM apache/airflow:2.4.2

 # 安装软件的时候要用root权限
 USER root
 RUN apt-get update \
   && apt-get install -y --no-install-recommends \
          vim \
   && apt-get autoremove -yqq --purge \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver for SQL Server 
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18

# On mac it's xxx-18.1.so.1.1, Linux xxx-18.1.so.2.1
RUN ln -sf /opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.1.so.2.1 /usr/lib/libmsodbcsql-18.so

COPY --chown=airflow:root dags/* /opt/airflow/dags/

 # pip安装用airflow用户
 USER airflow
 COPY requirements.txt /tmp/requirements.txt

 RUN pip install -r /tmp/requirements.txt
 # 一个用pip安装指定包的例子
 #RUN pip install --no-cache-dir apache-airflow-providers-docker==2.5.1
 # 拷贝DAG文件，并且设置权限给airflow
 # COPY --chown=airflow:root BY02_AirflowTutorial.py /opt/airflow/dags
 # COPY src/data.sqlite /opt/airflow/data.sqlite
 #建立一个可以写的文件夹，这里的~指的是主目录
 # RUN umask 0002; \
     # mkdir -p ~/writeable_directory

#  Microsoft ODBC Driver
# -----This line doesn't work
 RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
