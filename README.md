## საყურადღებო ამბები

 ძალიან დიდი იმიჯია და პირველ compose-ს დიდი დრო დასჭირდება და გაითვალისწინეთ. საკმაოდ resource intensive-ც შეიძლება იყოს.
 
---
**გაშვება**

ამ repo-ში გვაქვს Airflow-ის ორნაირი executor-ი (local, sequential) და გვაქვს სამი docker compose ფაილიც.

**_Sequential_**

აქ პარალელიზმი არ იქნება და პროექტშიც წესით არ გამოგადგებათ. თუმცა ამ ვერსიის გასაშვებად უნდა მოიქცეთ ასე:

 - ამ რეპოზიტორის დირექტორიაში (სადაც _**docker_compose_sequential_build_needed.yml**_) ფაილია უშვებთ:
      **docker-compose up --build**__ (ბოლოში -d ლოგებმა რომ არ შეგაწუხოთ) ან **docker-compose -f docker_compose_sequential_build_needed.yml up --build**

**_Local_**

აქ პარალელიზმი გექნებათ და უფრო რეკომენდირებულია Local Executor-ის გამოყენება. აქ გვაქვს ორი docker-compose:

**1. prebuilt ვერსია - *docker_compose_local_prebuilt.yml***
ამ ვარიანტში Airflow+Spark-ის ნაწილი ჩვენ მიერ წინასწარ არის დაბილდული და Dockerhub-ზე ატვირთული. გირჩევთ, ეს ვერსია გამოიყენოთ, ვინაიდან build-ს საკმაოდ დიდი დრო სჭირდება.

ამ ვერსიის გასაშვებად ფაქტობრივად მხოლოდ docker_compose_local_prebuilt.yml ფაილი გჭირდებათ. ამ ფაილის დირექტორიაში უშვებთ:

**docker-compose -f docker_compose_local_prebuilt.yml up**

image-ების დაპულვას ცოტა დრო დასჭირდება და ამის შემდეგ კონტეინერების აწევას, განსაკუთრებით Airflow-სას, მიახლოებით 1 წუთამდე უნდა დასჭირდეს.

**2. დასა-build ვერსია - *docker_compose_local_build_needed.yml***

ეს ვერსია ამ რეპოზიტორიაში არსებული DockerFile, entrypoint და სხვა რესურსების გამოყენებით ბილდავს იმიჯს, რასაც საკმაო დრო (30წთ+) სჭირდება. იმ შემთხვევაში გირჩევთ ამ ვერსიის გამოყენებას, თუ Dockerfile-ის ან თუნდაც entrypoint ფაილების შეცვლა გჭირდებათ. მაგალითად, შეიძლება ახალი requirement-ების დამატება გჭირდებოდეთ. თუ მსგავსი სიტუაცია არაა, მაშინ უმჯობესია prebuilt ვარიანტის გამოყენება. 

 ამ ვერსიის დასაბილდად გაუშვით:
      **docker-compose -f docker_compose_local_build_needed.yml up --build**

ბოლოში --build აუცილებელია.

თუ შეამჩნევთ, რომ ეარფლოუს კონტეინერ(ებ)ი  წამდაუწუმ რესტარტდება, დოკერის ინტერფეისიდან წაშალეთ ეგ კონტეინერები ერთიანად და გაიმეორეთ docker-compose ... [build].

---
# **Airflow:**
  - **პორტი**: http://localhost:8080/
  - **default credentials:**
  
        **username**: airflow
    
        **password**: airflow
        
  - Spark-ის ჯობების გასაშვებად ვებსერვერიდან უნდა შეხვიდეთ _**Admin -> Connections**_. ჩამონათვალში უნდა მოძებნოთ _spark_default_ და შეავსოთ ასე: 
  
      **Host**-ში:     _local_
      
      
      **Extra**-ში:   _{ "deploy_mode": "client", "spark.root.logger": "ALL", "verbose": "true"}_
      
  - თქვენ მიერ შექმნილი dag-ები შეგიძლიათ docker cp-ით ატვირთოთ airflow-ის კონტეინერში, მაგრამ უფრო მარტივია, თუ წინასწარ ჩვენ მიერ და-mount-ებულ დირექტორიებს გამოიყენებთ.
  Default-ად _**D:\BigDataPlayground**_ მისამართზე შეიქმნება ეს ფოლდერები. ცალკე ფოლდერებია dag-ებისთვის, job-ებისა და data-სათვის. სურვილისამებრ შეგიძლიათ გამოიყენოთ.
  აქვე შეინახება გარკვეული კონტეინერების მიერ დაგენერირებული მონაცემებიც და იმ შემთხვევაშიც კი, თუ კონტეინერის წაშლა/თავიდან შექმნა მოგიწევთ, დიდი ნაწილი მაინც შეგენახებათ    (Hive metastore-ა გამონაკლისი). თუ default მისამართზე არ გაწყობთ ამ ფოლდერების არსებობა, Dockerfile-ში მოძებნეთ ეს მისამართი და სურვილისამებრ შეცვალეთ docker compose-მდე.
  Executor-ის ტიპის მიხედვით, ორი ცალ-ცალკე compose ფაილი გვაქვს და BigDataPlayground-შიც შესაბამისად ორი ქვე-დირექტორია იქნება: local ან/და sequential. 
  თქვენთვის ყველაზე მეტად საჭირო დირექტორიები იქნება dags, jobs და data. აქ ჩაყრით თქვენს დაგებსა და საჭირო ფაილებს. ამ სამ ფოლდერში ფაილების განაწილების და ამ ფოლდერებიდან წაკითხვის მაგალითები ნახეთ examples-ში. ასევე იმასაც ნახავთ, თუ როგორ დაუკავშირდეთ HDFS-ს სპარკიდან.

  - Dag-ების ვებსერვერზე გამოჩენას შეიძლება რამდენიმე წუთიც დასჭირდეს და ნორმალურია ეგ.


# **Jupyter:**
  - **პორტი** - http://localhost:8282/ (შეიცვალა წინა იმიჯთან შედარებით)
  
  - მოითხოვს პაროლს ან ტოკენს. ტოკენია: **token** ზოგადად, ტოკენის გასაგებად კონტეინერის კონსოლში უნდა გაუშვათ _**jupyter notebook list**_. აქიდან შეგიძლიათ პირდაპირ ლინკი დააკოპიროთ, localhost:8282 ჩაუწეროთ დასაწყისში 0.0.0.0:8888-ის ნაცვლად და ისე გაიაროთ ავტორიზაცია, ან ტოკენი გადმოაკოპიროთ და ტოკენით შეხვიდეთ, ან ტოკენი შეცვალოთ სასურველი password-ით.

  - დაგხვდებათ სპარკის 2.4 ვერსია.

  - _**D:/BigDataPlayground/local(ან sequential)/notebooks**_ დირექტორიაში შეინახება თქვენ მიერ შექმნილი ნოუთბუქები.


# **Hue:**
  - **პორტი** - http://localhost:8888/

  - _**D:/BigDataPlayground/local(ან sequential)/namenode ან datanode**_ დირექტორებში შეინახება თქვენ მიერ HDFS-ზე ატვირთული დატა (ოღონდ FsImage და EditLog სახით).


# სხვა:

  სპარკის ვერსია არის 2.4. ზოგადად შეცვლა შეგიძლიათ, დოკერჰაბში ნახავთ შესაძლებელი ვერსიების tab-ებს და იმით ჩაანაცვლებთ დოკერფაილში. თუმცა საბოლოო პროექტისთვის ეს ვერსია გვინდა.

## Important Note: 
 არა-Windows user-ებმა დამაუნთებული დირექტორიების Path-ები compose.yml ფაილებში უნდა შეასწოროთ თქვენი ოპერაციული სისტემის შესაბამისად.


---
# Airflow Pipeline Docker Image Set-up

![CI Status](https://img.shields.io/github/workflow/status/dsaidgovsg/airflow-pipeline/CI/master?label=CI&logo=github&style=for-the-badge)

This repo is a GitHub Actions build matrix set-up to generate Docker images of
[Airflow](https://airflow.incubator.apache.org/), and other major applications
as below:

- Airflow
- Spark
- Hadoop integration with Spark
- Python
- SQL Alchemy

Additionally, `poetry` is used to perform all Python related installations at a
predefined global project directory, so that it is easy to add on new packages
without conflicting dependency package versions, which raw `pip` cannot achieve.
See
<https://github.com/dsaidgovsg/spark-k8s-addons#how-to-properly-manage-pip-packages>
for more information.

For builds involving Airflow v2 onwards, note that `poetry` is not officially
supported as an installation tool, but it is used anyway to make sure dependencies
are compatible and tested to work across multiple builds with different versions.

See <https://github.com/apache/airflow/issues/13149> for a related discussion
and how to resolve possible conflicts when installing packages on top of this
base image.

## Entrypoint

Also, for convenience, the current version runs both the `webserver` and
`scheduler` together in the same instance by the default entrypoint, with the
`webserver` being at the background and `scheduler` at the foreground. All the
convenient environment variables only works on the basis that the entrypoint is
used without any extra command.

If there is a preference to run the various Airflow CLI services separately,
you can simply pass the full command into the Docker command, but it will no
longer trigger any of the convenient environment variables / functionalities.

The above convenience functionalities include:

1. Discovering if database (`sqlite` and `postgres`) is ready
2. Automatically running `airflow db init` and `airflow db upgrade`
3. Easy creation of Airflow Web UI admin user by simple env vars.

See [`entrypoint.sh`](entrypoint.sh) for more details
and the list of convenient environment variables.

Also note that the command that will be run will also be run as `airflow`
user/group, unless the host overrides the user/group to run the Docker
container.

## Running locally

You will need `docker-compose` and `docker` command installed.

### Default Combined Airflow Webserver and Scheduler

```bash
docker-compose up --build
```

Navigate to `http://localhost:8080/`, and log in using the following RBAC
credentials to try out the DAGs:

- Username: `admin`
- Password: `Password123`

Note that the `webserver` logs are suppressed by default.

`CTRL-C` to gracefully terminate the services.

### Separate Airflow Webserver and Scheduler

```bash
docker-compose -f docker-compose.split.yml up --build
```

Navigate to `http://localhost:8080/` to try out the DAGs.

Both `webserver` and `scheduler` logs are shown separately.

`CTRL-C` to gracefully terminate the services.

## Versioning

Starting from Docker tags that give self-version `v1`, any Docker image usage
related breaking change will generate a new self-version so that this will
minimize any impact on the user-facing side trying to use the most updated
image.

These are considered breaking changes:

- Change of Linux distro, e.g. Alpine <-> Debian. This will automatically lead
  to a difference in the package management tool used such as `apk` vs `apt`.
  Note that however this does not include upgrading of Linux distro that may
  affect the package management, e.g. `alpine:3.9` vs `alpine:3.10`.
- Removal of advertized installed CLI tools that is not listed within the
  Docker tag. E.g. Spark and Hadoop are part of the Docker tag, so they are not
  part of the advertized CLI tools.
- Removal of advertized environment variables
- Change of any environment variable value

In the case where a CLI tool is known to perform a major version upgrade, this
set-up will try to also release a new self-version number. But note that this is
at a best effort scale only because most of the tools are inherited upstream,
or simply unable / undesirable to specify the version to install.

## Airflow provider packages

Airflow provider packages have been removed from the image from version `v8`
onwards and users will have to manually install them instead. Note that
provider packages follow their own versioning independent of Airflow's.

See <https://airflow.apache.org/docs/apache-airflow/2.1.0/backport-providers.html#backport-providers>
for more details.

```
# Airflow V2
poetry add apache-airflow-provider-apache-spark==1.0.3

# Airflow V1
poetry add apache-airflow[spark]==1.10.z
```

## Changelogs

All self-versioned change logs are listed in [`CHANGELOG.md`](CHANGELOG.md).

The advertized CLI tools and env vars are also listed in the detailed change
logs.

## How to Manually Build Docker Image

Example build command:

```bash
AIRFLOW_VERSION=1.10
SPARK_VERSION=3.0.0
HADOOP_VERSION=3.2.0
SCALA_VERSION=2.12
PYTHON_VERSION=3.6
SQLALCHEMY_VERSION=1.3
docker build -t airflow-pipeline \
  --build-arg "AIRFLOW_VERSION=${AIRFLOW_VERSION}" \
  --build-arg "SPARK_VERSION=${SPARK_VERSION}" \
  --build-arg "HADOOP_VERSION=${HADOOP_VERSION}" \
  --build-arg "SCALA_VERSION=${SCALA_VERSION}" \
  --build-arg "PYTHON_VERSION=${PYTHON_VERSION}" \
  --build-arg "SQLALCHEMY_VERSION=${SQLALCHEMY_VERSION}" \
  .
```

You may refer to the [vars.yml](templates/vars.yml) to have a sensing of all the
possible build arguments to combine.

## Caveat

Because this image is based on Spark with Kubernetes compatible image, which
always generates Debian based Docker images, the images generated from this
repository are likely to stay Debian based as well. But note that there is no
guarantee that this is always true, but such changes are always marked with
Docker image release tag.

Also, currently the default entrypoint without command logic assumes that
a Postgres server will always be used (the default `sqlite` can work as an
alternative). As such, when using in this mode, an external Postgres server
has to be made available for Airflow services to access.
