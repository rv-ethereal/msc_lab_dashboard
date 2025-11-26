# Free End-to-End Data Lakehouse

A fully free and open-source data lakehouse architecture running on Docker Compose. This project demonstrates a complete Bronze → Silver → Gold pipeline with automated orchestration, suitable for local development and learning.

## 🏗️ Architecture Overview

```
Raw Data → Spark (Bronze → Silver → Gold) → MinIO Storage → Trino SQL → Superset Dashboards
                         ↑
                    Airflow Orchestration
```

### Technology Stack

- **MinIO** – S3-compatible object storage
- **Apache Spark** – Data processing and ETL
- **Delta Lake** – ACID table format
- **Apache Airflow** – Workflow orchestration
- **Trino** – Distributed SQL query engine
- **Apache Superset** – Data visualization and dashboards
- **Docker Compose** – Container orchestration

### Storage Layers

- **Bronze**: Raw ingested data (as-is from source)
- **Silver**: Cleaned and validated data
- **Gold**: Aggregated analytical tables

## ✨ Features

- Complete lakehouse running on a single laptop
- Automated daily ETL pipelines via Airflow
- Delta Lake tables stored in MinIO
- SQL analytics through Trino
- Interactive dashboards with Superset
- One-command deployment: `docker compose up -d`

## 📋 Prerequisites

Before starting, ensure you have:

- **Docker Engine** (latest version)
- **Docker Compose** v2+
- **8 GB RAM minimum** available for containers
- **Optional**: AWS CLI for testing MinIO access

## 📁 Project Structure

```
lakehouse-project/
├── docker-compose.yml          # Container orchestration
├── data/
│   └── sample.csv             # Raw input data
├── spark/
│   ├── Dockerfile             # Custom Spark image (optional)
│   └── scripts/
│       ├── bronze_load.py     # Bronze layer ingestion
│       ├── silver_transform.py # Silver layer cleaning
│       └── gold_aggregate.py   # Gold layer aggregation
├── airflow/
│   └── dags/
│       └── lakehouse_dag.py   # ETL orchestration DAG
├── trino/
│   └── catalog/
│       └── hive.properties    # Trino catalog config
└── superset/                   # Dashboard configuration
```

## 🚀 Quick Start

### 1. Start All Services

```bash
docker compose up -d
```

### 2. Verify Services

Access the following interfaces:

| Service | URL | Credentials |
|---------|-----|-------------|
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| Airflow | http://localhost:8080 | Check docker-compose.yml |
| Trino | http://localhost:8081 | - |
| Superset | http://localhost:8088 | admin / admin (default) |
| Spark UI | http://localhost:4040 | (when job is running) |

### 3. Create MinIO Bucket

Via Console (http://localhost:9001):
1. Login with `minioadmin` / `minioadmin`
2. Create bucket: `minio-bucket`

Or via AWS CLI:
```bash
aws --endpoint-url http://localhost:9000 s3 mb s3://minio-bucket
```

### 4. Add Sample Data

Place your CSV file at:
```
data/sample.csv
```

### 5. Run ETL Pipeline

**Option A: Via Airflow (Recommended)**
1. Navigate to http://localhost:8080
2. Enable the `lakehouse_etl` DAG
3. Click "Trigger DAG"

**Option B: Manual Spark Submit**
```bash
docker exec spark /opt/spark/bin/spark-submit \
  --master local[*] \
  --packages io.delta:delta-core_2.12:2.4.0 \
  /opt/spark/scripts/bronze_load.py
```

## ⚙️ Configuration

### MinIO (Object Storage)

S3 configuration for Spark:
```python
spark.conf.set("fs.s3a.endpoint", "http://minio:9000")
spark.conf.set("fs.s3a.access.key", "minioadmin")
spark.conf.set("fs.s3a.secret.key", "minioadmin")
spark.conf.set("fs.s3a.path.style.access", "true")
```

### Spark with Delta Lake

Required package:
```bash
--packages io.delta:delta-core_2.12:2.4.0
```

### Trino Catalog

File: `trino/catalog/hive.properties`
```properties
connector.name=hive
hive.s3.aws-access-key=minioadmin
hive.s3.aws-secret-key=minioadmin
hive.s3.endpoint=http://minio:9000
hive.s3.path-style-access=true
```

### Superset Database Connection

Add Trino as a database:
```
trino://user@trino:8080/hive/default
```

## 📊 ETL Pipeline

### Bronze Layer (`bronze_load.py`)
- Reads raw CSV files
- Writes Delta tables to MinIO
- No transformations, preserves original data

### Silver Layer (`silver_transform.py`)
- Data cleaning and validation
- Type casting and standardization
- Handles missing values
- Deduplication

### Gold Layer (`gold_aggregate.py`)
- Business-level aggregations
- Creates analytical tables
- Optimized for dashboard queries

### Airflow DAG

Located at: `airflow/dags/lakehouse_dag.py`

Schedule: Daily at midnight
```
bronze_load → silver_transform → gold_aggregate
```

## 🔍 Querying Data

### Via Trino CLI

```bash
docker exec -it trino trino
```

Example queries:
```sql
SHOW TABLES FROM hive.default;

SELECT * FROM hive.default.daily_sales_delta LIMIT 10;

SELECT 
  date, 
  SUM(amount) as total_sales 
FROM hive.default.daily_sales_delta 
GROUP BY date 
ORDER BY date DESC;
```

### Via Superset

1. Navigate to http://localhost:8088
2. Add Trino database connection
3. Create dataset from Gold tables
4. Build charts and dashboards

## 🛠️ Troubleshooting

### Services Not Starting
```bash
# Check logs
docker compose logs -f [service_name]

# Restart specific service
docker compose restart [service_name]
```

### MinIO Connection Issues
- Verify bucket exists
- Check credentials in Spark/Trino configs
- Ensure `path.style.access=true` is set

### Spark Job Failures
```bash
# View Spark logs
docker logs spark

# Check Spark UI
http://localhost:4040
```

### Airflow DAG Not Running
- Verify DAG is enabled in UI
- Check scheduler logs: `docker logs airflow-scheduler`
- Ensure connections are configured

## 🧹 Maintenance

### Stop All Services
```bash
docker compose down
```

### Remove All Data (Clean Slate)
```bash
docker compose down -v
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f spark
```

## 📚 Next Steps

1. **Add More Data Sources**: Extend bronze layer to ingest from APIs, databases
2. **Implement Data Quality**: Add Great Expectations or similar
3. **Scale Processing**: Configure Spark cluster mode
4. **Add Security**: Implement authentication and encryption
5. **CI/CD**: Automate deployment and testing
6. **Monitoring**: Add Prometheus and Grafana

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## 📧 Support

For questions and support, please open an issue in the repository.

---

**Built with ❤️ for the data engineering community**